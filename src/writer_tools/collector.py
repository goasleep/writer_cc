#!/usr/bin/env python3
"""
article_collector.py - 单文章采集脚本
"""

import os
import re
import hashlib
from datetime import datetime
from urllib.parse import urlparse
import requests
import trafilatura
from markdownify import markdownify as md
from bs4 import BeautifulSoup

class ArticleCollector:
    def __init__(self, output_dir="./articles"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 配置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_url(self, url):
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_with_trafilatura(self, url, html=None):
        """使用trafilatura提取内容"""
        if html is None:
            html = self.fetch_url(url)

        if not html:
            return None

        # 提取内容
        result = trafilatura.extract(
            html,
            url=url,
            output_format='markdown',
            include_comments=False,
            include_tables=True,
            include_images=True,
            include_links=True,
            deduplicate=True
        )

        # 提取元数据
        metadata_doc = trafilatura.extract_metadata(html, default_url=url)
        metadata = metadata_doc.as_dict() if metadata_doc else {}

        return {
            'content': result,
            'metadata': metadata
        }

    def extract_with_readability(self, url, html=None):
        """备用：使用readability-lxml提取"""
        from readability import Document

        if html is None:
            html = self.fetch_url(url)

        if not html:
            return None

        doc = Document(html)
        title = doc.title()
        content_html = doc.summary()
        content_md = md(content_html, heading_style="ATX")

        return {
            'content': content_md,
            'metadata': {
                'title': title,
                'url': url
            }
        }

    def generate_filename(self, metadata, url):
        """生成安全的文件名"""
        title = metadata.get('title', '') if metadata else ''

        if title:
            # 清理标题中的非法字符
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
            safe_title = safe_title[:100]  # 限制长度
            filename = f"{safe_title}.md"
        else:
            # 使用URL的hash作为文件名
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"article_{url_hash}.md"

        return filename

    def save_article(self, url, method='trafilatura'):
        """保存文章到文件"""
        print(f"Processing: {url}")

        # 提取内容
        if method == 'trafilatura':
            result = self.extract_with_trafilatura(url)
        else:
            result = self.extract_with_readability(url)

        if not result or not result['content']:
            print(f"Failed to extract content from {url}")
            return None

        # 生成文件名
        filename = self.generate_filename(result['metadata'], url)
        filepath = os.path.join(self.output_dir, filename)

        # 检查文件是否已存在
        if os.path.exists(filepath):
            print(f"File already exists: {filepath}")
            return filepath

        # 构建frontmatter
        frontmatter = self.build_frontmatter(result['metadata'], url)

        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write("\n\n")
            f.write(result['content'])

        print(f"Saved: {filepath}")
        return filepath

    def build_frontmatter(self, metadata, url):
        """构建YAML frontmatter"""
        from .frontmatter import create_frontmatter
        from datetime import datetime

        meta = {}

        title = metadata.get('title', '') if metadata else ''
        if title:
            meta['title'] = title

        meta['url'] = url

        author = metadata.get('author', '') if metadata else ''
        if author:
            meta['author'] = author

        date = metadata.get('date', '') if metadata else ''
        if date:
            meta['date'] = date
        else:
            meta['date'] = datetime.now().strftime('%Y-%m-%d')

        meta['collected_at'] = datetime.now().isoformat()

        sitename = metadata.get('sitename', '') if metadata else ''
        if sitename:
            meta['source'] = sitename

        description = metadata.get('description', '') if metadata else ''
        if description:
            meta['description'] = description[:200]

        tags = metadata.get('tags', []) if metadata else []
        if tags:
            meta['tags'] = tags[:10]

        return create_frontmatter(meta, style='compact')


# 使用示例
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Collect article from URL')
    parser.add_argument('url', help='URL to collect')
    parser.add_argument('-o', '--output', default='./articles', help='Output directory')

    args = parser.parse_args()

    collector = ArticleCollector(output_dir=args.output)
    collector.save_article(args.url)
