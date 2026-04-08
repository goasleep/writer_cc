"""
writer_tools - 个人写作库工具集

为 Obsidian Vault 设计的文章采集、清理、frontmatter 生成工具包。
可直接作为 Python 包导入，也可被注册为 Claude Code skills 调用。
"""

from .fetcher import fetch_html, fetch_with_playwright, is_content_valid, FetchError
from .extractor import extract_with_trafilatura, extract_with_readability, clean_markdown_content
from .pipeline import collect_article, CollectResult
from .frontmatter import create_frontmatter, FrontmatterBuilder

# 旧版兼容导出
from .collector import ArticleCollector
from .claude_collector import ClaudeArticleCollector, collect_article as legacy_collect_article, collect_articles
from .batch_collector import BatchCollector
from .cleaner import MarkdownCleaner, create_default_cleaner

__version__ = "0.1.0"
__all__ = [
    # fetch
    "fetch_html",
    "fetch_with_playwright",
    "is_content_valid",
    "FetchError",
    # extract
    "extract_with_trafilatura",
    "extract_with_readability",
    "clean_markdown_content",
    # pipeline
    "collect_article",
    "CollectResult",
    # frontmatter
    "create_frontmatter",
    "FrontmatterBuilder",
    # legacy
    "ArticleCollector",
    "ClaudeArticleCollector",
    "BatchCollector",
    "MarkdownCleaner",
    "create_default_cleaner",
    "legacy_collect_article",
    "collect_articles",
]
