#!/usr/bin/env python3
"""
extractor.py - HTML 内容提取工具

核心原则：只做 HTML → Markdown 的结构化提取，不走 LLM。
"""

import re
from typing import Optional

import trafilatura
from markdownify import markdownify as md


def extract_with_trafilatura(html: str, url: str, include_images: bool = True) -> Optional[dict]:
    """
    使用 trafilatura 提取正文和元数据

    Returns:
        {"content": str, "metadata": dict} 或 None
    """
    try:
        content = trafilatura.extract(
            html,
            url=url,
            output_format="markdown",
            include_comments=False,
            include_tables=True,
            include_images=include_images,
            include_links=True,
            deduplicate=True,
        )

        metadata_doc = trafilatura.extract_metadata(html, default_url=url)
        metadata = metadata_doc.as_dict() if metadata_doc else {}

        if not content:
            return None

        return {"content": content, "metadata": metadata}
    except Exception:
        return None


def extract_with_readability(html: str, url: str) -> Optional[dict]:
    """
    使用 readability-lxml + markdownify 提取正文和元数据

    Returns:
        {"content": str, "metadata": dict} 或 None
    """
    try:
        from readability import Document

        doc = Document(html)
        title = doc.title()
        content_html = doc.summary()

        # 使用 markdownify 将 HTML 转换为 markdown
        # markdownify 默认会将 <img> 转换为 ![alt](src) 格式
        content_md = md(content_html, heading_style="ATX")

        if not content_md or len(content_md.strip()) < 50:
            return None

        return {
            "content": content_md,
            "metadata": {
                "title": title,
                "url": url,
            },
        }
    except Exception:
        return None


def clean_markdown_content(content: str) -> str:
    """
    清理提取后的 Markdown 内容中的常见垃圾文本
    """
    replacements = [
        ("Doubao\nEdit in Doubao\n", ""),
        ("Edit in Doubao", ""),
        ("\n\n\n", "\n\n"),
    ]
    for old, new in replacements:
        content = content.replace(old, new)

    # 清理过长的连续空白行
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()
