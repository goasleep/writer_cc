#!/usr/bin/env python3
"""
fetcher.py - 原始内容获取工具

核心原则：只做网络请求和 HTML 获取，不做任何 LLM 相关的理解或判断。
"""

import asyncio
import re
from typing import Optional
from urllib.parse import urljoin, urlparse

import httpx


class FetchError(Exception):
    """获取失败异常"""
    pass


def fetch_html(url: str, timeout: float = 30.0) -> dict:
    """
    使用 HTTP 获取原始 HTML

    Returns:
        {"html": str, "final_url": str, "method": "http"}
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return {
                "html": response.text,
                "final_url": str(response.url),
                "method": "http",
            }
    except Exception as exc:
        raise FetchError(f"HTTP fetch failed for {url}: {exc}") from exc


def fetch_with_playwright(url: str, timeout: float = 30.0) -> dict:
    """
    使用 Playwright 渲染页面获取 HTML

    Returns:
        {"html": str, "final_url": str, "method": "playwright"}
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise FetchError("Playwright not installed") from exc

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    )
                )
                page.goto(url, timeout=int(timeout * 1000), wait_until="networkidle")
                page.wait_for_timeout(2000)
                html = page.content()
                final_url = page.url
            finally:
                browser.close()

        return {
            "html": html,
            "final_url": final_url,
            "method": "playwright",
        }
    except Exception as exc:
        raise FetchError(f"Playwright fetch failed for {url}: {exc}") from exc


def is_content_valid(content: str) -> bool:
    """
    启发式内容有效性校验（零 LLM 成本）

    规则：
    - < 200 字符：无效（可能是骨架屏/导航/广告）
    - >= 1500 字符：有效
    - 中间长度：检查段落数和句子数密度
    """
    stripped = content.strip()
    if len(stripped) < 200:
        return False
    if len(stripped) >= 1500:
        return True

    paragraphs = [p for p in stripped.split("\n\n") if len(p.strip()) > 50]
    sentences = re.split(r"[。！？.!?]", stripped)
    valid_sentences = [s for s in sentences if s.strip()]
    return len(paragraphs) >= 2 and len(valid_sentences) >= 5


async def fetch_with_playwright_cdp(url: str, timeout: float = 30.0) -> dict:
    """
    使用 Playwright 的 CDP 功能获取 HTML 并下载图片

    通过拦截网络响应中的图片数据，绕过防盗链限制

    Returns:
        {
            "html": str,
            "final_url": str,
            "method": "playwright+cdp",
            "images": [
                {
                    "url": str,
                    "buffer": bytes,
                    "content_type": str
                },
                ...
            ]
        }
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise FetchError("Playwright not installed") from exc

    downloaded_images = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()

            # 监听网络请求，拦截图片
            # 使用 dict 按 URL 去重，保留最大的 buffer（避免同一图片的不同尺寸版本）
            _downloaded_by_url: dict[str, dict] = {}

            async def handle_response(response):
                try:
                    # 获取headers
                    headers = await response.all_headers()
                    content_type = headers.get("content-type", "")

                    if not content_type or not content_type.startswith("image/"):
                        return

                    url = response.url

                    # 过滤掉微信系统资源和非内容图片
                    skip_patterns = [
                        "favicon", "logo", "icon", "avatar", "banner",
                        "ad.", "tracking", "pixel", "spacer", "blank", "1x1", "beacon",
                        "wx_profile", "profile_photo", "headimg"
                    ]
                    lower_url = url.lower()
                    if any(p in lower_url for p in skip_patterns):
                        return

                    # 过滤微信系统资源域名
                    if "res.wx.qq.com" in lower_url:
                        return

                    # 获取图片二进制数据
                    buffer = await response.body()

                    # 跳过过小或过大的图片
                    # 小图 (< 3KB) 通常是图标、头像、tracking pixel
                    # 大图 (> 10MB) 可能是视频或其他媒体
                    if len(buffer) < 3 * 1024 or len(buffer) > 10 * 1024 * 1024:
                        return

                    # 同一URL只保留最大的版本（避免头像小图被优先匹配）
                    if url not in _downloaded_by_url or len(buffer) > len(_downloaded_by_url[url]["buffer"]):
                        _downloaded_by_url[url] = {
                            "url": url,
                            "buffer": buffer,
                            "content_type": content_type,
                        }

                except Exception:
                    pass  # 忽略错误

            page.on("response", lambda response: asyncio.create_task(handle_response(response)))

            try:
                await page.goto(url, timeout=int(timeout * 1000), wait_until="networkidle")
                await page.wait_for_timeout(2000)  # 等待动态内容加载

                # 滚动页面触发懒加载图片（微信公众号等使用 data-src 懒加载）
                # 分多次小步滚动，确保图片逐步加载
                for _ in range(15):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(0.3)
                # 滚动回顶部，给顶部图片加载时间
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.5)
                # 再次滚动到底部，确保所有图片都被触发
                for _ in range(15):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(0.2)

                html = await page.content()
                final_url = page.url
            finally:
                await browser.close()

        # 将按URL去重的图片转换为列表
        downloaded_images = list(_downloaded_by_url.values())

        return {
            "html": html,
            "final_url": final_url,
            "method": "playwright+cdp",
            "images": downloaded_images,
        }

    except Exception as exc:
        raise FetchError(f"Playwright CDP fetch failed for {url}: {exc}") from exc


def fetch_with_playwright_cdp_sync(url: str, timeout: float = 30.0) -> dict:
    """
    同步包装器，用于从同步代码调用 async 的 Playwright CDP 函数
    """
    return asyncio.run(fetch_with_playwright_cdp(url, timeout))
