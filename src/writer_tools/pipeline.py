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
from .fetcher import FetchError, fetch_html, fetch_with_playwright, is_content_valid


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

    Returns:
        [(absolute_url, alt_text), ...]
    """
    img_pattern = r'<img[^>]*?src=["\']([^"\']+)["\'][^>]*?>'
    alt_pattern = r'<img[^>]*?alt=["\']([^"\']*)["\'][^>]*?>'

    results = []
    seen = set()

    for match in re.finditer(img_pattern, html, re.IGNORECASE):
        raw_src = match.group(1).strip()
        if not raw_src or raw_src.startswith("data:"):
            continue

        # 解析 alt
        img_tag = match.group(0)
        alt_match = re.search(alt_pattern, img_tag, re.IGNORECASE)
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
    """
    for absolute_url, alt_text, filename in image_mappings:
        local_path = f"{assets_rel_path}/{filename}"

        # 替换 markdown 图片语法: ![alt](url)
        escaped_url = re.escape(absolute_url)
        md_pattern = rf"!\[([^\]]*)\]\({escaped_url}\)"
        md_replacement = rf"![{alt_text}]\({local_path}\)"
        content = re.sub(md_pattern, md_replacement, content)

        # 替换裸 URL（trafilatura 有时会直接输出图片 URL）
        content = content.replace(absolute_url, local_path)

    return content


def _download_and_replace_images(
    content: str,
    html: str,
    base_url: str,
    assets_dir: Path,
    assets_rel_path: str,
) -> str:
    """
    提取图片、下载到本地、替换 markdown 链接
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
        content = _replace_image_links(content, image_mappings, assets_rel_path)

    return content


def collect_article(
    url: str,
    include_images: bool = True,
    raw_dir: Optional[Path] = None,
) -> CollectResult:
    """
    采集单篇文章，执行完整的 fetch → extract → validate → fallback 管道

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

    # Step 1: HTTP fetch
    try:
        fetch_result = fetch_html(url)
    except FetchError as exc:
        return CollectResult(success=False, error=str(exc))

    html = fetch_result["html"]
    final_url = fetch_result["final_url"]

    # Step 2: Trafilatura extract
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

    # Step 3: Fallback to Playwright + readability
    try:
        pw_result = fetch_with_playwright(url)
    except FetchError:
        # Playwright 也失败了，如果之前 trafilatura 有结果，返回它（保底）
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
            error=f"HTTP fetch succeeded but extraction failed, and Playwright fallback also failed for {url}",
        )

    # Step 4: Readability extract from Playwright HTML
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

    # Step 5: 最终保底
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

    if pw_extracted:
        content = clean_markdown_content(pw_extracted["content"])
        if include_images:
            content = _download_and_replace_images(
                content, pw_html, pw_url, assets_dir, assets_rel_path
            )
        return CollectResult(
            success=True,
            content=content,
            metadata=pw_extracted["metadata"],
            final_url=pw_url,
            method="playwright+readability(fallback)",
            assets_dir=str(assets_dir) if include_images else "",
        )

    return CollectResult(
        success=False,
        error=f"All extraction methods failed for {url}",
    )
