#!/usr/bin/env python3
"""
pipeline.py - 文章采集管道编排器

核心原则：
1. fetch 和 extract 不走 LLM
2. 自动 fallback：http → trafilatura → 校验失败 → playwright → readability → 校验
3. 图片下载到本地 raw/assets/<url_hash>/，替换 markdown 中的链接为本地相对路径
"""

import hashlib
import mimetypes
import os
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx

from .extractor import clean_markdown_content, extract_with_readability, extract_with_trafilatura
from .fetcher import FetchError, fetch_html, fetch_with_playwright, fetch_with_playwright_cdp_sync, is_content_valid


class CollectResult:
    """采集结果容器"""

    def __init__(
        self,
        success: bool,
        content: str = "",
        metadata: dict = None,
        final_url: str = "",
        method: str = "",
        error: str = "",
        assets_dir: str = "",
    ):
        self.success = success
        self.content = content
        self.metadata = metadata or {}
        self.final_url = final_url
        self.method = method
        self.error = error
        self.assets_dir = assets_dir

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "content": self.content,
            "metadata": self.metadata,
            "final_url": self.final_url,
            "method": self.method,
            "error": self.error,
            "assets_dir": self.assets_dir,
        }


def _url_hash(url: str) -> str:
    """为 URL 生成稳定的 8 位 hash 作为 assets 文件夹名"""
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:8]


def _extract_image_urls(html: str, base_url: str) -> list[tuple[str, str]]:
    """
    从 HTML 中提取图片 URL 和 alt 文本

    支持 src 和 data-src（微信公众号等懒加载机制）
    优先使用 data-src（懒加载的真实图片地址），因为 src 可能是占位图

    Returns:
        [(absolute_url, alt_text), ...]
    """
    results = []
    seen = set()

    # 先匹配所有 img 标签，再在每个标签内优先查找 data-src
    img_tag_pattern = r'<img[^>]*?>'

    for tag_match in re.finditer(img_tag_pattern, html, re.IGNORECASE):
        img_tag = tag_match.group(0)

        # 优先匹配 data-src，其次 src（避免 src 是懒加载占位图）
        raw_src = ""
        for attr in ["data-src", "src"]:
            attr_match = re.search(rf'{attr}=["\']([^"\']+)["\']', img_tag, re.IGNORECASE)
            if attr_match:
                raw_src = attr_match.group(1).strip()
                break

        if not raw_src or raw_src.startswith("data:"):
            continue

        # 解析 alt
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag, re.IGNORECASE)
        alt_text = alt_match.group(1) if alt_match else ""

        absolute_url = urljoin(base_url, raw_src)
        if absolute_url in seen:
            continue
        seen.add(absolute_url)

        # 过滤掉常见非内容图片
        skip_patterns = [
            r"favicon",
            r"logo",
            r"icon",
            r"avatar",
            r"banner",
            r"ad\.",
            r"tracking",
            r"pixel",
            r"spacer",
            r"blank",
            r"1x1",
            r"beacon",
            r"wx_profile",
            r"profile_photo",
            r"headimg",
        ]
        lower_url = absolute_url.lower()
        if any(p in lower_url for p in skip_patterns):
            continue

        results.append((absolute_url, alt_text))

    return results


def _download_image(client: httpx.Client, image_url: str, referer: str) -> Optional[bytes]:
    """下载单张图片，返回二进制内容或 None"""
    try:
        resp = client.get(
            image_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Referer": referer,
            },
            timeout=30,
            follow_redirects=True,
        )
        resp.raise_for_status()
        data = resp.content
        # 跳过过小或过大的图片
        if len(data) < 1024 or len(data) > 10 * 1024 * 1024:
            return None
        return data
    except Exception:
        return None


def _ext_from_response(url: str, content_type: str) -> str:
    """从响应头或 URL 推断图片扩展名"""
    mime_map = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
    }

    if content_type:
        for mime, ext in mime_map.items():
            if mime in content_type:
                return ext

    parsed = urlparse(url)
    path = parsed.path.lower()
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]:
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext

    return ".jpg"


def _replace_image_links(
    content: str,
    image_mappings: list[tuple[str, str, str]],
    assets_rel_path: str,
) -> str:
    """
    将 markdown 内容中的图片链接替换为本地相对路径

    image_mappings: [(absolute_url, alt_text, local_filename), ...]

    Returns:
        更新后的 content
    """
    replaced_urls = set()

    for absolute_url, alt_text, filename in image_mappings:
        local_path = f"{assets_rel_path}/{filename}"

        # 策略1: 精确匹配 markdown 图片语法: ![alt](url)
        escaped_url = re.escape(absolute_url)
        md_pattern = rf"!\[([^\]]*)\]\({escaped_url}\)"
        md_replacement = rf"![{alt_text}]\({local_path}\)"

        if re.search(md_pattern, content):
            content = re.sub(md_pattern, md_replacement, content)
            replaced_urls.add(absolute_url)
            continue

        # 策略2: 替换裸 URL（trafilatura 有时会直接输出图片 URL）
        if absolute_url in content:
            content = content.replace(absolute_url, local_path)
            replaced_urls.add(absolute_url)
            continue

        # 策略3: 标准化URL后匹配（处理fragment、HTML实体等差异）
        normalized_url = _normalize_image_url(absolute_url)
        if normalized_url != absolute_url:
            escaped_norm = re.escape(normalized_url)
            norm_md_pattern = rf"!\[([^\]]*)\]\({escaped_norm}[^)]*\)"
            if re.search(norm_md_pattern, content):
                content = re.sub(norm_md_pattern, md_replacement, content)
                replaced_urls.add(absolute_url)
                continue

            if normalized_url in content:
                content = content.replace(normalized_url, local_path)
                replaced_urls.add(absolute_url)
                continue

        # 策略4: 基础路径匹配（忽略查询参数差异，只匹配 scheme://host/path）
        parsed = urlparse(absolute_url)
        base_path = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if base_path in content:
            # 使用正则替换包含该基础路径的完整URL
            escaped_base = re.escape(base_path)
            # 匹配 markdown 中该基础路径开头的完整URL（包含查询参数）
            loose_md_pattern = rf"!\[([^\]]*)\]\({escaped_base}[^)]*\)"
            if re.search(loose_md_pattern, content):
                content = re.sub(loose_md_pattern, md_replacement, content)
                replaced_urls.add(absolute_url)
                continue

    # 返回更新后的内容和未替换的图片映射
    return content


def _insert_missing_images(
    content: str,
    image_mappings: list[tuple[str, str, str]],
    assets_rel_path: str,
) -> str:
    """
    在 markdown 内容中插入缺失的图片引用

    对于已下载但 markdown 中没有引用的图片，智能地插入到合适位置：
    - 如果文章很短（<500字符），插入到末尾
    - 否则，尝试在相关段落附近插入

    image_mappings: [(absolute_url, alt_text, local_filename), ...]
    """
    if not image_mappings:
        return content

    # 检查哪些图片已经被引用（原始URL或本地路径）
    referenced_images = set()
    for abs_url, _, filename in image_mappings:
        local_path = f"{assets_rel_path}/{filename}"
        # 检查原始 URL 或本地路径是否已在 content 中
        escaped_url = re.escape(abs_url)
        if (
            re.search(rf"!\[.*\]\({escaped_url}\)", content)
            or abs_url in content
            or local_path in content
        ):
            referenced_images.add(abs_url)

    # 找出未引用的图片
    missing_images = [
        (abs_url, alt, filename)
        for abs_url, alt, filename in image_mappings
        if abs_url not in referenced_images
    ]

    if not missing_images:
        return content

    # 计算插入位置
    content_length = len(content.strip())
    lines = content.split("\n")
    paragraph_count = len([l for l in lines if l.strip() and not l.strip().startswith("#")])

    # 只有在内容足够长、段落足够多、图片数量也足够时，才在段落间插入
    # 否则在文章末尾添加
    should_distribute = (
        content_length >= 300
        and paragraph_count >= 5
        and len(missing_images) >= 3
    )

    if not should_distribute:
        # 在文章末尾添加图片
        image_section = "\n\n" + "\n\n".join(
            f"![{alt}]({assets_rel_path}/{filename})"
            for _, alt, filename in missing_images
        )
        return content + image_section

    # 对于长文章，尝试在段落间插入
    # 找到段落结束的位置（空行）
    blank_indices = [i for i, line in enumerate(lines) if line.strip() == ""]

    if not blank_indices:
        # 没有找到合适的插入位置，在末尾添加
        image_section = "\n\n" + "\n\n".join(
            f"![{alt}]({assets_rel_path}/{filename})"
            for _, alt, filename in missing_images
        )
        return content + image_section

    # 尽量在文章的前2/3部分均匀分布图片
    end_index = len(blank_indices) * 2 // 3
    usable_positions = blank_indices[:end_index]

    if len(usable_positions) <= 1:
        # 可用位置太少，在末尾添加
        image_section = "\n\n" + "\n\n".join(
            f"![{alt}]({assets_rel_path}/{filename})"
            for _, alt, filename in missing_images
        )
        return content + image_section

    # 计算均匀分布的间隔
    if len(missing_images) == 1:
        insert_positions = [usable_positions[len(usable_positions) // 2]]
    else:
        interval = len(usable_positions) / len(missing_images)
        insert_positions = [
            usable_positions[int(i * interval)]
            for i in range(len(missing_images))
        ]

    # 如果没找到合适的插入位置，就在末尾添加
    if not insert_positions:
        image_section = "\n\n" + "\n\n".join(
            f"![{alt}]({assets_rel_path}/{filename})"
            for _, alt, filename in missing_images
        )
        return content + image_section

    # 在找到的位置插入图片
    result_lines = lines.copy()
    for idx, (abs_url, alt, filename) in enumerate(missing_images):
        if idx < len(insert_positions):
            insert_at = insert_positions[idx] + idx * 2  # 考虑已插入的行
            result_lines.insert(
                insert_at,
                f"\n![{alt}]({assets_rel_path}/{filename})"
            )
            result_lines.insert(insert_at + 1, "")  # 空行

    return "\n".join(result_lines)


def _normalize_image_url(url: str) -> str:
    """
    标准化图片URL，用于匹配

    处理：
    1. 移除fragment (#imgIndex=0)
    2. 解码HTML实体 (&amp; -> &)
    3. 移除常见查询参数中的噪音
    """
    from urllib.parse import unquote, urlparse, parse_qs, urlunparse

    # 移除fragment
    if "#" in url:
        url = url.split("#")[0]

    # 解码HTML实体
    url = url.replace("&amp;", "&")

    return url


def _find_matching_cdp_image(html_url: str, cdp_images: list[dict]) -> Optional[dict]:
    """
    为HTML中的图片URL找到匹配的CDP下载图片

    匹配策略：
    1. 标准化后精确匹配
    2. 基础路径匹配（忽略查询参数差异）
    3. 文件名匹配
    """
    from urllib.parse import urlparse

    normalized_html = _normalize_image_url(html_url)
    parsed_html = urlparse(normalized_html)

    # 尝试精确匹配
    for img_data in cdp_images:
        cdp_url = img_data["url"]
        if _normalize_image_url(cdp_url) == normalized_html:
            return img_data

    # 尝试基础路径匹配（忽略查询参数）
    html_base = f"{parsed_html.scheme}://{parsed_html.netloc}{parsed_html.path}"
    for img_data in cdp_images:
        cdp_url = img_data["url"]
        parsed_cdp = urlparse(cdp_url)
        cdp_base = f"{parsed_cdp.scheme}://{parsed_cdp.netloc}{parsed_cdp.path}"
        if html_base == cdp_base:
            return img_data

    # 尝试文件名匹配
    html_filename = parsed_html.path.split("/")[-1]
    for img_data in cdp_images:
        cdp_url = img_data["url"]
        parsed_cdp = urlparse(cdp_url)
        cdp_filename = parsed_cdp.path.split("/")[-1]
        if html_filename and cdp_filename and html_filename == cdp_filename:
            return img_data

    return None


def _download_and_replace_images_from_cdp(
    content: str,
    cdp_images: list[dict],
    assets_dir: Path,
    assets_rel_path: str,
    html: str = "",
    base_url: str = "",
) -> str:
    """
    从 CDP 下载的图片保存到本地并替换/插入 markdown 链接

    Args:
        content: markdown 内容
        cdp_images: CDP 下载的图片列表 [{"url": str, "buffer": bytes, "content_type": str}, ...]
        assets_dir: assets 目录路径
        assets_rel_path: assets 相对路径
        html: 原始 HTML（用于确定图片在文档中的出现顺序）
        base_url: 基础 URL

    Returns:
        更新后的 content
    """
    if not cdp_images:
        return content

    assets_dir.mkdir(parents=True, exist_ok=True)

    # 从HTML中提取图片URL（按出现顺序）
    html_image_urls = []
    if html:
        html_image_urls = [url for url, _ in _extract_image_urls(html, base_url)]

    # 按HTML中的出现顺序匹配并保存图片
    # 使用 dict 按 filename 去重，避免同一张图片产生多个映射导致重复插入
    image_mappings: list[tuple[str, str, str]] = []
    used_cdp_images = set()
    seen_filenames = set()

    for idx, html_url in enumerate(html_image_urls, start=1):
        # 找到匹配的CDP图片
        matched_idx = -1
        for i, img_data in enumerate(cdp_images):
            if i in used_cdp_images:
                continue
            if _find_matching_cdp_image(html_url, [img_data]):
                matched_idx = i
                break

        if matched_idx == -1:
            continue

        img_data = cdp_images[matched_idx]
        used_cdp_images.add(matched_idx)

        buffer = img_data["buffer"]
        content_type = img_data["content_type"]
        cdp_url = img_data["url"]

        # 获取扩展名
        ext = _ext_from_response(cdp_url, content_type)
        filename = f"image_{idx:02d}{ext}"

        # 跳过已处理过的 filename（防止重复）
        if filename in seen_filenames:
            continue
        seen_filenames.add(filename)

        # 保存图片
        filepath = assets_dir / filename
        with open(filepath, "wb") as f:
            f.write(buffer)

        # 只添加一个映射：优先使用HTML URL（markdown中提取器更可能保留此URL）
        # 如果markdown中确实使用了CDP URL，_replace_image_links 中的裸URL替换会处理
        image_mappings.append((html_url, "", filename))

    if image_mappings:
        # 先尝试替换已有的图片引用
        content = _replace_image_links(content, image_mappings, assets_rel_path)
        # 再插入缺失的图片引用
        content = _insert_missing_images(content, image_mappings, assets_rel_path)

    return content


def _download_and_replace_images(
    content: str,
    html: str,
    base_url: str,
    assets_dir: Path,
    assets_rel_path: str,
) -> str:
    """
    提取图片、下载到本地、替换/插入 markdown 链接

    注意：这是从HTML提取URL并下载的fallback方法，
    优先使用 _download_and_replace_images_from_cdp
    """
    image_urls = _extract_image_urls(html, base_url)
    if not image_urls:
        return content

    assets_dir.mkdir(parents=True, exist_ok=True)

    image_mappings: list[tuple[str, str, str]] = []

    with httpx.Client(timeout=30, follow_redirects=True) as client:
        for idx, (image_url, alt_text) in enumerate(image_urls, start=1):
            data = _download_image(client, image_url, referer=base_url)
            if data is None:
                continue

            # 获取 content-type
            try:
                head_resp = client.head(image_url, headers={"Referer": base_url}, timeout=10)
                content_type = head_resp.headers.get("content-type", "")
            except Exception:
                content_type = ""

            ext = _ext_from_response(image_url, content_type)
            filename = f"image_{idx:02d}{ext}"

            filepath = assets_dir / filename
            with open(filepath, "wb") as f:
                f.write(data)

            image_mappings.append((image_url, alt_text, filename))

    if image_mappings:
        # 先尝试替换已有的图片引用
        content = _replace_image_links(content, image_mappings, assets_rel_path)
        # 再插入缺失的图片引用
        content = _insert_missing_images(content, image_mappings, assets_rel_path)

    return content


def collect_article(
    url: str,
    include_images: bool = True,
    raw_dir: Optional[Path] = None,
) -> CollectResult:
    """
    采集单篇文章，执行完整的 fetch → extract → validate → fallback 管道

    优先使用 Playwright+CDP 以获取完整的图片数据

    Args:
        url: 文章 URL
        include_images: 是否下载图片到本地并替换链接
        raw_dir: raw/articles 目录路径，用于计算 assets 相对位置

    Returns:
        CollectResult
    """
    url_hash = _url_hash(url)

    if raw_dir is None:
        raw_dir = Path(__file__).parent.parent.parent / "raw"

    assets_dir = raw_dir / "assets" / url_hash
    assets_rel_path = f"../assets/{url_hash}"

    # 清理旧的 assets 避免残留（同一URL重复采集时）
    if include_images and assets_dir.exists():
        for old_file in assets_dir.iterdir():
            if old_file.is_file():
                old_file.unlink()

    # Step 1: 优先使用 Playwright+CDP（获取完整HTML和图片）
    try:
        cdp_result = fetch_with_playwright_cdp_sync(url)
        cdp_html = cdp_result["html"]
        cdp_url = cdp_result["final_url"]
        cdp_images = cdp_result.get("images", [])

        # 使用 readability-lxml 提取正文（自动移除侧边栏等非正文内容）
        cdp_extracted = extract_with_readability(cdp_html, cdp_url)

        if cdp_extracted:
            content = clean_markdown_content(cdp_extracted["content"])
            if is_content_valid(content):
                # 如果有CDP下载的图片，优先使用
                if include_images and cdp_images:
                    content = _download_and_replace_images_from_cdp(
                        content, cdp_images, assets_dir, assets_rel_path, cdp_html, cdp_url
                    )
                elif include_images:
                    # Fallback: 从HTML提取URL下载
                    content = _download_and_replace_images(
                        content, cdp_html, cdp_url, assets_dir, assets_rel_path
                    )

                return CollectResult(
                    success=True,
                    content=content,
                    metadata=cdp_extracted["metadata"],
                    final_url=cdp_url,
                    method="playwright+cdp+readability",
                    assets_dir=str(assets_dir) if include_images else "",
                )
    except FetchError:
        # CDP失败，继续尝试其他方法
        pass
    except Exception:
        # 其他异常，继续尝试其他方法
        pass

    # Step 2: Fallback to HTTP fetch + trafilatura
    try:
        fetch_result = fetch_html(url)
    except FetchError as exc:
        return CollectResult(success=False, error=str(exc))

    html = fetch_result["html"]
    final_url = fetch_result["final_url"]

    # Step 3: Trafilatura extract
    extracted = extract_with_trafilatura(html, final_url, include_images=include_images)

    if extracted:
        content = clean_markdown_content(extracted["content"])
        if is_content_valid(content):
            if include_images:
                content = _download_and_replace_images(
                    content, html, final_url, assets_dir, assets_rel_path
                )
            return CollectResult(
                success=True,
                content=content,
                metadata=extracted["metadata"],
                final_url=final_url,
                method="http+trafilatura",
                assets_dir=str(assets_dir) if include_images else "",
            )

    # Step 4: Fallback to Playwright (非CDP) + readability
    try:
        pw_result = fetch_with_playwright(url)
        pw_html = pw_result["html"]
        pw_url = pw_result["final_url"]
        pw_extracted = extract_with_readability(pw_html, pw_url)

        if pw_extracted:
            content = clean_markdown_content(pw_extracted["content"])
            if is_content_valid(content):
                metadata = extracted["metadata"] if extracted else {}
                if not metadata.get("title") and pw_extracted["metadata"].get("title"):
                    metadata["title"] = pw_extracted["metadata"]["title"]
                if include_images:
                    content = _download_and_replace_images(
                        content, pw_html, pw_url, assets_dir, assets_rel_path
                    )
                return CollectResult(
                    success=True,
                    content=content,
                    metadata=metadata,
                    final_url=pw_url,
                    method="playwright+readability",
                    assets_dir=str(assets_dir) if include_images else "",
                )
    except FetchError:
        pass

    # Step 5: 最终保底 - 返回任何可用的结果
    if extracted:
        content = clean_markdown_content(extracted["content"])
        if include_images:
            content = _download_and_replace_images(
                content, html, final_url, assets_dir, assets_rel_path
            )
        return CollectResult(
            success=True,
            content=content,
            metadata=extracted["metadata"],
            final_url=final_url,
            method="http+trafilatura(fallback)",
            assets_dir=str(assets_dir) if include_images else "",
        )

    return CollectResult(
        success=False,
        error=f"All extraction methods failed for {url}",
    )
