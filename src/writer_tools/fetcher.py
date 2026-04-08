#!/usr/bin/env python3
"""
fetcher.py - 原始内容获取工具

核心原则：只做网络请求和 HTML 获取，不做任何 LLM 相关的理解或判断。
"""

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
