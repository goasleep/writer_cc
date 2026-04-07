"""
writer_tools - 个人写作库工具集

为 Obsidian Vault 设计的文章采集、清理、frontmatter 生成工具包。
可直接作为 Python 包导入，也可被注册为 Claude Code skills 调用。
"""

from .collector import ArticleCollector
from .claude_collector import (
    ClaudeArticleCollector,
    collect_article,
    collect_articles,
)
from .batch_collector import BatchCollector
from .cleaner import MarkdownCleaner, create_default_cleaner
from .frontmatter import FrontmatterBuilder, create_frontmatter

__version__ = "0.1.0"
__all__ = [
    "ArticleCollector",
    "ClaudeArticleCollector",
    "BatchCollector",
    "MarkdownCleaner",
    "create_default_cleaner",
    "FrontmatterBuilder",
    "create_frontmatter",
    "collect_article",
    "collect_articles",
]
