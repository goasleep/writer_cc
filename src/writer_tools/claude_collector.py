#!/usr/bin/env python3
"""
claude_article_collector.py - Claude Code集成文章采集脚本
专为Claude Code环境优化的文章采集工具
"""

import os
import re
import json
import hashlib
from datetime import datetime
from urllib.parse import urlparse

import requests
import trafilatura


class ClaudeArticleCollector:
    """Claude Code优化的文章采集器"""

    def __init__(self, output_dir="./collected_articles"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def collect(self, url, options=None):
        """
        采集文章并返回Markdown格式

        Args:
            url: 文章URL
            options: 配置选项
                - include_metadata: 是否包含元数据 (默认True)
                - include_images: 是否包含图片 (默认True)
                - output_format: 输出格式 'markdown' 或 'json' (默认'markdown')
                - save_to_file: 是否保存到文件 (默认True)

        Returns:
            采集结果字典
        """
        options = options or {}
        include_metadata = options.get('include_metadata', True)
        include_images = options.get('include_images', True)
        output_format = options.get('output_format', 'markdown')
        save_to_file = options.get('save_to_file', True)

        print(f"🔍 Collecting: {url}")

        # 获取网页内容
        html = self._fetch_url(url)
        if not html:
            return {'success': False, 'error': 'Failed to fetch URL'}

        # 提取内容
        result = self._extract_content(html, url, include_images)

        if not result or not result.get('content'):
            return {'success': False, 'error': 'Failed to extract content'}

        # 构建输出
        output = self._build_output(result, url, include_metadata)

        # 保存到文件
        if save_to_file:
            filepath = self._save_to_file(output, result['metadata'], url)
            output['filepath'] = filepath

        output['success'] = True
        return output

    def _fetch_url(self, url):
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Error fetching URL: {e}")
            return None

    def _extract_content(self, html, url, include_images=True):
        """提取文章内容"""
        try:
            # 使用trafilatura提取
            content = trafilatura.extract(
                html,
                url=url,
                output_format='markdown',
                include_comments=False,
                include_tables=True,
                include_images=include_images,
                include_links=True,
                deduplicate=True
            )

            # 提取元数据
            metadata_doc = trafilatura.extract_metadata(html, default_url=url)
            metadata = metadata_doc.as_dict() if metadata_doc else {}

            # 降级策略：内容太少时尝试用 Playwright 获取
            if not content or len(content.replace('\n', '').replace(' ', '')) < 100:
                print(f"⚠️ Trafilatura extracted too little content ({len(content or '')} chars), trying Playwright fallback...")
                pw_result = self._extract_with_playwright(url)
                if pw_result:
                    return pw_result

            return {
                'content': content,
                'metadata': metadata
            }
        except Exception as e:
            print(f"❌ Error extracting content: {e}")
            return None

    def _extract_with_playwright(self, url):
        """使用 Playwright 作为降级策略提取 JS 渲染页面内容"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("⚠️ Playwright not installed, skipping fallback")
            return None

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000, wait_until='networkidle')
                # 等待主要内容加载
                page.wait_for_timeout(2000)

                # 尝试获取标题
                title = page.title()

                # 尝试获取正文内容
                selectors = [
                    'article',
                    '[class*="doc-content"]',
                    '[class*="document-content"]',
                    '[class*="editor-content"]',
                    '[class*="rich-text"]',
                    '[class*="prose"]',
                    'main',
                    '.content',
                    '[role="main"]'
                ]
                content = ''
                for sel in selectors:
                    el = page.locator(sel).first
                    if el.count() > 0:
                        text = el.inner_text(timeout=5000)
                        if len(text) > 200:
                            content = text
                            break

                if not content:
                    content = page.locator('body').inner_text(timeout=5000)

                # 清理常见 UI 文本
                content = content.replace('Doubao\nEdit in Doubao\n', '')
                content = content.replace('Edit in Doubao', '')

                browser.close()

                if len(content.replace('\n', '').replace(' ', '')) < 100:
                    print("⚠️ Playwright fallback also extracted too little content")
                    return None

                print(f"✅ Playwright fallback succeeded ({len(content)} chars)")
                return {
                    'content': content,
                    'metadata': {
                        'title': title,
                        'sitename': 'Web',
                    }
                }
        except Exception as e:
            print(f"❌ Playwright fallback failed: {e}")
            return None

    def _build_output(self, result, url, include_metadata=True):
        """构建输出内容"""
        content = result['content']
        metadata = result['metadata']

        if include_metadata:
            frontmatter = self._build_frontmatter(metadata, url)
            full_content = f"{frontmatter}\n\n{content}"
        else:
            full_content = content

        return {
            'content': full_content,
            'metadata': {
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'date': metadata.get('date', ''),
                'url': url,
                'sitename': metadata.get('sitename', ''),
                'description': metadata.get('description', '')
            }
        }

    def _build_frontmatter(self, metadata, url):
        """构建YAML frontmatter"""
        from .frontmatter import create_frontmatter

        meta = {
            'type': 'source',
            'source_url': url,
            'collected_at': datetime.now().isoformat(),
            'status': 'raw',
        }

        title = metadata.get('title', '')
        if title:
            meta['title'] = title

        author = metadata.get('author', '')
        if author:
            meta['author'] = author

        date = metadata.get('date', '')
        if date:
            meta['published_date'] = date

        sitename = metadata.get('sitename', '')
        if sitename:
            meta['source'] = sitename

        description = metadata.get('description', '')
        if description:
            meta['description'] = description[:200]

        tags = metadata.get('tags', [])
        if tags:
            meta['tags'] = tags[:10]

        categories = metadata.get('categories', [])
        if categories:
            meta['categories'] = categories[:5]

        return create_frontmatter(meta, style='compact')

    def _save_to_file(self, output, metadata, url):
        """保存到文件"""
        # 生成文件名
        title = metadata.get('title', '')
        if title:
            safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
            safe_title = safe_title[:80]
            filename = f"{safe_title}.md"
        else:
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"article_{url_hash}.md"

        filepath = os.path.join(self.output_dir, filename)

        # 检查文件是否已存在
        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1

        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output['content'])

        print(f"✅ Saved: {filepath}")
        return filepath

    def batch_collect(self, urls, options=None):
        """批量采集"""
        results = []

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing...")
            result = self.collect(url, options)
            results.append(result)

        # 统计
        success = sum(1 for r in results if r.get('success'))
        print(f"\n📊 Batch complete: {success}/{len(urls)} successful")

        return results


# Claude Code便捷函数
def collect_article(url, **options):
    """
    便捷函数：采集单篇文章

    使用示例:
        result = collect_article("https://example.com/article")
        print(result['content'])
    """
    collector = ClaudeArticleCollector()
    return collector.collect(url, options)


def collect_articles(urls, **options):
    """
    便捷函数：批量采集文章

    使用示例:
        urls = ["https://example.com/1", "https://example.com/2"]
        results = collect_articles(urls)
    """
    collector = ClaudeArticleCollector()
    return collector.batch_collect(urls, options)


# 如果直接运行此脚本
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Collect articles and convert to Markdown')
    parser.add_argument('url', help='URL to collect')
    parser.add_argument('-o', '--output', default='./collected_articles', help='Output directory')
    parser.add_argument('--no-metadata', action='store_true', help='Skip metadata')

    args = parser.parse_args()

    collector = ClaudeArticleCollector(output_dir=args.output)
    result = collector.collect(
        args.url,
        options={'include_metadata': not args.no_metadata}
    )

    if result['success']:
        print(f"\n✅ Article collected successfully!")
        print(f"📄 File: {result.get('filepath', 'N/A')}")
        print(f"📝 Title: {result['metadata'].get('title', 'N/A')}")
    else:
        print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
