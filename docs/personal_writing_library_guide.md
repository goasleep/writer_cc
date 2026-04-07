# 个人写作库系统：文章收集与Markdown整理完整方案

## 目录
1. [网页转Markdown工具推荐](#1-网页转markdown工具推荐)
2. [自动化采集方案](#2-自动化采集方案)
3. [Markdown标准化处理](#3-markdown标准化处理)
4. [Claude Code集成采集脚本](#4-claude-code集成采集脚本)
5. [Frontmatter字段规范](#5-frontmatter字段规范)

---

## 1. 网页转Markdown工具推荐

### 1.1 浏览器插件（手动采集）

#### 推荐插件对比

| 插件名称 | 特点 | 价格 | 适用场景 |
|---------|------|------|---------|
| **Save** (savemarkdown.co) | AI驱动提取，支持YouTube字幕、Twitter线程 | 免费3次/月 | 高质量内容提取 |
| **MarkDownload** | 开源免费，使用Readability算法 | 免费 | 日常文章保存 |
| **Webpage to Markdown** | 本地处理，100%隐私保护 | 免费 | 隐私敏感用户 |
| **cpdown** | 显示token数量，适合LLM工作流 | 免费 | AI/LLM用户 |
| **Plain Markdown** | 实时编辑器，自动保存 | 免费 | 需要编辑的用户 |

#### 推荐安装

**首选：MarkDownload（免费开源）**
- Chrome: https://chrome.google.com/webstore/detail/markdownload/
- Firefox: https://addons.mozilla.org/firefox/addon/markdownload/

**备选：cpdown（适合AI工作流）**
- GitHub: https://github.com/ysm-dev/cpdown

### 1.2 Python库（自动化采集）

#### 核心库对比

| 库名称 | 功能 | 优势 | 适用场景 |
|-------|------|------|---------|
| **trafilatura** | 内容提取+元数据 | 学术级精度，ACL 2021论文 | 高质量内容提取 |
| **markdownify** | HTML转Markdown | 简单易用，格式保留好 | HTML到Markdown转换 |
| **readability-lxml** | 内容提取 | Mozilla算法，成熟稳定 | 快速内容提取 |
| **html2text** | HTML转Markdown | 轻量级，无依赖 | 简单转换任务 |
| **newspaper3k** | 新闻提取 | 专为新闻优化 | 新闻文章采集 |

#### 安装命令

```bash
# 核心推荐组合
pip install trafilatura markdownify requests beautifulsoup4 lxml

# 完整安装（包含所有可选依赖）
pip install trafilatura[all] markdownify requests beautifulsoup4 lxml html2text

# 如果需要浏览器渲染支持
pip install playwright
playwright install chromium
```

### 1.3 命令行工具

#### trafilatura CLI

```bash
# 安装
pip install trafilatura

# 基本使用
trafilatura https://example.com/article

# 输出为Markdown
trafilatura --format markdown https://example.com/article

# 包含元数据
trafilatura --format markdown --url https://example.com/article

# 批量处理
for url in $(cat urls.txt); do
    trafilatura --format markdown --url "$url" > "$(echo $url | md5sum | cut -d' ' -f1).md"
done
```

#### md-fetch（推荐CLI工具）

```bash
# 安装
npm install -g md-fetch

# 使用
md-fetch https://example.com/article

# 输出到文件
md-fetch https://example.com/article -o article.md
```

---

## 2. 自动化采集方案

### 2.1 单URL采集脚本

```python
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
        metadata = trafilatura.extract_metadata(html, url=url)

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
        from datetime import datetime

        fm = ["---"]

        # 标题
        title = metadata.get('title', '') if metadata else ''
        if title:
            fm.append(f'title: "{title}"')

        # URL
        fm.append(f'url: "{url}"')

        # 作者
        author = metadata.get('author', '') if metadata else ''
        if author:
            fm.append(f'author: "{author}"')

        # 日期
        date = metadata.get('date', '') if metadata else ''
        if date:
            fm.append(f'date: "{date}"')
        else:
            fm.append(f'date: "{datetime.now().strftime("%Y-%m-%d")}"')

        # 采集日期
        fm.append(f'collected_at: "{datetime.now().isoformat()}"')

        # 站点名称
        sitename = metadata.get('sitename', '') if metadata else ''
        if sitename:
            fm.append(f'source: "{sitename}"')

        # 描述
        description = metadata.get('description', '') if metadata else ''
        if description:
            fm.append(f'description: "{description[:200]}"')

        # 标签
        tags = metadata.get('tags', []) if metadata else []
        if tags:
            tags_str = ', '.join([f'"{tag}"' for tag in tags[:10]])
            fm.append(f'tags: [{tags_str}]')

        fm.append("---")

        return "\n".join(fm)


# 使用示例
if __name__ == "__main__":
    collector = ArticleCollector(output_dir="./my_articles")

    # 采集单个URL
    url = "https://example.com/article"
    collector.save_article(url)
```

### 2.2 批量采集脚本

```python
#!/usr/bin/env python3
"""
batch_collector.py - 批量文章采集脚本
"""

import os
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from article_collector import ArticleCollector

class BatchCollector:
    def __init__(self, output_dir="./articles", max_workers=5):
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.collector = ArticleCollector(output_dir)
        self.results = []

    def from_file(self, filepath):
        """从文件读取URL列表"""
        urls = []

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)

        return self.process_urls(urls)

    def from_csv(self, filepath, url_column='url'):
        """从CSV文件读取URL"""
        urls = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if url_column in row and row[url_column]:
                    urls.append(row[url_column])

        return self.process_urls(urls)

    def from_json(self, filepath):
        """从JSON文件读取URL列表"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        urls = []
        if isinstance(data, list):
            urls = [item.get('url', item) if isinstance(item, dict) else item for item in data]
        elif isinstance(data, dict) and 'urls' in data:
            urls = data['urls']

        return self.process_urls(urls)

    def process_urls(self, urls):
        """并行处理多个URL"""
        print(f"Processing {len(urls)} URLs with {self.max_workers} workers...")

        completed = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.collector.save_article, url): url 
                for url in urls
            }

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        self.results.append({
                            'url': url,
                            'status': 'success',
                            'filepath': result
                        })
                        completed += 1
                    else:
                        self.results.append({
                            'url': url,
                            'status': 'failed',
                            'error': 'No content extracted'
                        })
                        failed += 1
                except Exception as e:
                    self.results.append({
                        'url': url,
                        'status': 'error',
                        'error': str(e)
                    })
                    failed += 1

                # 进度报告
                total = completed + failed
                if total % 10 == 0:
                    print(f"Progress: {total}/{len(urls)} (Success: {completed}, Failed: {failed})")

        print(f"\nCompleted: {completed}, Failed: {failed}")
        return self.results

    def save_report(self, filepath="collection_report.json"):
        """保存采集报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"Report saved: {filepath}")


# 使用示例
if __name__ == "__main__":
    batch = BatchCollector(output_dir="./articles", max_workers=3)

    # 从文本文件批量采集
    # batch.from_file("urls.txt")

    # 从CSV批量采集
    # batch.from_csv("articles.csv", url_column="url")

    # 直接传入URL列表
    urls = [
        "https://example.com/article1",
        "https://example.com/article2",
    ]
    batch.process_urls(urls)
    batch.save_report()
```

### 2.3 URL列表文件格式

```
# urls.txt - 每行一个URL，支持注释
https://example.com/article1
https://example.com/article2
# 这是注释，会被忽略
https://example.com/article3
```

```json
// urls.json
{
  "urls": [
    "https://example.com/article1",
    "https://example.com/article2"
  ]
}
```

```csv
// articles.csv
url,category,priority
https://example.com/article1,tech,high
https://example.com/article2,design,medium
```

---

## 3. Markdown标准化处理

### 3.1 格式清理脚本

```python
#!/usr/bin/env python3
"""
markdown_cleaner.py - Markdown标准化清理脚本
"""

import re
import os
from pathlib import Path

class MarkdownCleaner:
    def __init__(self):
        self.rules = []

    def clean(self, content):
        """执行所有清理规则"""
        for rule_name, rule_func in self.rules:
            content = rule_func(content)
        return content

    def add_rule(self, name, func):
        """添加清理规则"""
        self.rules.append((name, func))

    @staticmethod
    def remove_excessive_blank_lines(content):
        """移除多余的空行"""
        # 将3个或更多连续空行替换为2个
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content

    @staticmethod
    def normalize_headings(content):
        """标准化标题格式"""
        # 确保标题前后有空行
        lines = content.split('\n')
        result = []

        for i, line in enumerate(lines):
            if re.match(r'^#{1,6}\s', line):
                # 标题前加空行（如果不是第一行且前一行不是空行）
                if i > 0 and result and result[-1].strip():
                    result.append('')
                result.append(line)
                # 标题后加空行
                result.append('')
            else:
                result.append(line)

        return '\n'.join(result)

    @staticmethod
    def normalize_code_blocks(content):
        """标准化代码块"""
        # 确保代码块标记前后有空行
        lines = content.split('\n')
        result = []
        in_code_block = False

        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_code_block:
                    # 代码块开始
                    if result and result[-1].strip():
                        result.append('')
                    in_code_block = True
                else:
                    # 代码块结束
                    in_code_block = False
                result.append(line)
                result.append('')
            else:
                result.append(line)

        return '\n'.join(result)

    @staticmethod
    def fix_image_paths(content, base_path=''):
        """修复图片路径"""
        # 将相对路径转换为绝对路径
        if base_path:
            content = re.sub(
                r'!\[(.*?)\]\((?!http)(.*?)\)',
                rf'![\1]({base_path}/\2)',
                content
            )
        return content

    @staticmethod
    def remove_html_comments(content):
        """移除HTML注释"""
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        return content

    @staticmethod
    def normalize_lists(content):
        """标准化列表格式"""
        lines = content.split('\n')
        result = []

        for line in lines:
            # 统一无序列表符号为 -
            line = re.sub(r'^[\*•]\s', '- ', line)
            result.append(line)

        return '\n'.join(result)

    @staticmethod
    def remove_tracking_links(content):
        """移除追踪参数"""
        # 移除常见的追踪参数
        tracking_params = [
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
            'fbclid', 'gclid', 'ref', 'source'
        ]

        for param in tracking_params:
            content = re.sub(rf'[?&]{param}=[^&\s]*', '', content)

        # 清理空的查询字符串
        content = re.sub(r'\?&', '?', content)
        content = re.sub(r'\?$', '', content)

        return content


def create_default_cleaner():
    """创建默认的清理器"""
    cleaner = MarkdownCleaner()

    cleaner.add_rule('remove_html_comments', MarkdownCleaner.remove_html_comments)
    cleaner.add_rule('normalize_headings', MarkdownCleaner.normalize_headings)
    cleaner.add_rule('normalize_code_blocks', MarkdownCleaner.normalize_code_blocks)
    cleaner.add_rule('normalize_lists', MarkdownCleaner.normalize_lists)
    cleaner.add_rule('remove_tracking_links', MarkdownCleaner.remove_tracking_links)
    cleaner.add_rule('remove_excessive_blank_lines', MarkdownCleaner.remove_excessive_blank_lines)

    return cleaner


# 使用示例
if __name__ == "__main__":
    cleaner = create_default_cleaner()

    # 清理单个文件
    with open('article.md', 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = cleaner.clean(content)

    with open('article_cleaned.md', 'w', encoding='utf-8') as f:
        f.write(cleaned)
```

### 3.2 图片处理脚本

```python
#!/usr/bin/env python3
"""
image_processor.py - Markdown图片处理脚本
"""

import os
import re
import hashlib
import requests
from urllib.parse import urlparse, urljoin
from pathlib import Path

class ImageProcessor:
    def __init__(self, output_dir="./images", download_images=True):
        self.output_dir = output_dir
        self.download_images = download_images
        os.makedirs(output_dir, exist_ok=True)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def extract_images(self, content):
        """提取Markdown中的所有图片"""
        pattern = r'!\[(.*?)\]\((.*?)\)'
        return re.findall(pattern, content)

    def download_image(self, url, article_url=None):
        """下载图片"""
        if not url.startswith('http'):
            if article_url:
                url = urljoin(article_url, url)
            else:
                return None

        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # 确定文件扩展名
            content_type = response.headers.get('content-type', '')
            ext = self._get_extension(content_type, url)

            # 生成文件名
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            filename = f"{url_hash}{ext}"
            filepath = os.path.join(self.output_dir, filename)

            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filepath
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
            return None

    def _get_extension(self, content_type, url):
        """获取文件扩展名"""
        ext_map = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg'
        }

        for mime, ext in ext_map.items():
            if mime in content_type:
                return ext

        # 从URL获取扩展名
        parsed = urlparse(url)
        path = parsed.path
        if '.' in path:
            return path[path.rfind('.'):]

        return '.jpg'  # 默认

    def process_markdown(self, content, article_url=None, image_base_path="images"):
        """处理Markdown中的图片"""
        images = self.extract_images(content)

        for alt_text, img_url in images:
            old_ref = f'![{alt_text}]({img_url})'

            if img_url.startswith('http') and self.download_images:
                # 下载远程图片
                local_path = self.download_image(img_url, article_url)
                if local_path:
                    new_ref = f'![{alt_text}]({image_base_path}/{os.path.basename(local_path)})'
                    content = content.replace(old_ref, new_ref)
            elif img_url.startswith('data:'):
                # 处理base64图片
                print(f"Skipping base64 image: {alt_text}")

        return content

    def generate_image_report(self, content):
        """生成图片报告"""
        images = self.extract_images(content)

        report = {
            'total': len(images),
            'remote': 0,
            'local': 0,
            'base64': 0,
            'images': []
        }

        for alt_text, img_url in images:
            img_info = {
                'alt': alt_text,
                'url': img_url[:100] + '...' if len(img_url) > 100 else img_url
            }

            if img_url.startswith('http'):
                report['remote'] += 1
                img_info['type'] = 'remote'
            elif img_url.startswith('data:'):
                report['base64'] += 1
                img_info['type'] = 'base64'
            else:
                report['local'] += 1
                img_info['type'] = 'local'

            report['images'].append(img_info)

        return report


# 使用示例
if __name__ == "__main__":
    processor = ImageProcessor(output_dir="./article_images")

    with open('article.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 处理图片
    processed = processor.process_markdown(content, article_url="https://example.com")

    # 生成报告
    report = processor.generate_image_report(content)
    print(f"Images found: {report['total']}")
    print(f"  Remote: {report['remote']}")
    print(f"  Local: {report['local']}")
    print(f"  Base64: {report['base64']}")
```

---

## 4. Claude Code集成采集脚本

### 4.1 完整集成脚本

```python
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
import subprocess
import sys

# 检查并安装依赖
def ensure_dependencies():
    """确保所有依赖已安装"""
    required = ['requests', 'trafilatura', 'markdownify', 'beautifulsoup4']

    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

ensure_dependencies()

import requests
import trafilatura
from markdownify import markdownify as md
from bs4 import BeautifulSoup


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
            metadata = trafilatura.extract_metadata(html, url=url)

            return {
                'content': content,
                'metadata': metadata
            }
        except Exception as e:
            print(f"❌ Error extracting content: {e}")
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
        fm_lines = ["---"]

        # 标题
        title = metadata.get('title', '')
        if title:
            fm_lines.append(f'title: "{self._escape_yaml(title)}"')

        # URL
        fm_lines.append(f'source_url: "{url}"')

        # 作者
        author = metadata.get('author', '')
        if author:
            fm_lines.append(f'author: "{self._escape_yaml(author)}"')

        # 发布日期
        date = metadata.get('date', '')
        if date:
            fm_lines.append(f'published_date: "{date}"')

        # 采集日期
        fm_lines.append(f'collected_at: "{datetime.now().isoformat()}"')

        # 站点名称
        sitename = metadata.get('sitename', '')
        if sitename:
            fm_lines.append(f'source: "{self._escape_yaml(sitename)}"')

        # 描述
        description = metadata.get('description', '')
        if description:
            fm_lines.append(f'description: "{self._escape_yaml(description[:200])}"')

        # 标签
        tags = metadata.get('tags', [])
        if tags:
            tags_str = ', '.join([f'"{tag}"' for tag in tags[:10]])
            fm_lines.append(f'tags: [{tags_str}]')

        # 分类
        categories = metadata.get('categories', [])
        if categories:
            cat_str = ', '.join([f'"{cat}"' for cat in categories[:5]])
            fm_lines.append(f'categories: [{cat_str}]')

        fm_lines.append("---")

        return "\n".join(fm_lines)

    def _escape_yaml(self, text):
        """转义YAML特殊字符"""
        return text.replace('"', '\"').replace('\n', ' ').replace('\r', '')

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
```

### 4.2 Claude Code MCP工具配置

```json
{
  "mcpServers": {
    "article-collector": {
      "command": "python",
      "args": ["claude_article_collector.py"],
      "env": {
        "OUTPUT_DIR": "./collected_articles"
      }
    }
  }
}
```

### 4.3 使用示例

```python
# 在Claude Code中使用

# 1. 采集单篇文章
result = collect_article("https://example.com/article")
print(result['content'])

# 2. 批量采集
urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
]
results = collect_articles(urls)

# 3. 自定义选项
result = collect_article(
    "https://example.com/article",
    include_metadata=True,
    include_images=True,
    save_to_file=True
)

# 4. 查看元数据
print(f"Title: {result['metadata']['title']}")
print(f"Author: {result['metadata']['author']}")
print(f"Date: {result['metadata']['date']}")
```

---

## 5. Frontmatter字段规范

### 5.1 推荐字段列表

```yaml
---
# ===== 基本信息 =====
title: "文章标题"                    # 文章标题（必需）
slug: "article-slug"                 # URL友好的标识符

# ===== 来源信息 =====
source_url: "https://example.com"    # 原始URL（必需）
source: "Example Site"               # 来源站点名称
canonical_url: "https://example.com" # 规范URL（如有）

# ===== 作者信息 =====
author: "作者名称"                    # 作者
author_url: "https://author.com"     # 作者链接
translator: "译者名称"                # 译者（翻译文章）

# ===== 时间信息 =====
published_date: "2024-01-15"         # 发布日期
date: "2024-01-15"                   # 别名
modified_date: "2024-01-16"          # 修改日期
collected_at: "2024-01-20T10:30:00"  # 采集时间（自动生成）

# ===== 分类与标签 =====
category: "技术"                      # 主分类
categories: ["技术", "编程"]          # 多分类
tags: ["python", "markdown", "tutorial"]  # 标签

# ===== 内容描述 =====
description: "文章摘要"               # 简短描述
excerpt: "文章摘录"                   # 详细摘录
summary: "内容总结"                   # 内容总结

# ===== 状态与权限 =====
status: "published"                  # 状态: draft, published, archived
draft: false                         # 是否为草稿
featured: false                      # 是否推荐
private: false                       # 是否私有
license: "CC BY 4.0"                 # 许可证

# ===== 媒体信息 =====
cover_image: "https://example.com/cover.jpg"  # 封面图
image: "https://example.com/og.jpg"           # Open Graph图片

# ===== 技术信息 =====
language: "zh-CN"                    # 语言
lang: "zh"                           # 语言简写
reading_time: 5                      # 预计阅读时间（分钟）
word_count: 1200                     # 字数统计

# ===== 关联信息 =====
series: "系列名称"                    # 所属系列
series_order: 1                      # 系列中的顺序
related: ["other-article-slug"]      # 相关文章

# ===== 自定义字段 =====
priority: 1                          # 优先级
rating: 5                            # 评分
notes: "个人笔记"                     # 个人笔记
---
```

### 5.2 最小化Frontmatter模板

```yaml
---
title: "文章标题"
source_url: "https://example.com/article"
date: "2024-01-15"
tags: []
---
```

### 5.3 完整Frontmatter模板

```yaml
---
title: "文章标题"
slug: "article-slug"
source_url: "https://example.com/article"
source: "Example Site"
author: "作者名称"
author_url: "https://author.com"
published_date: "2024-01-15"
modified_date: "2024-01-16"
collected_at: "2024-01-20T10:30:00"
category: "技术"
categories: ["技术", "编程"]
tags: ["python", "markdown", "tutorial"]
description: "文章简短描述"
excerpt: "文章详细摘录，用于预览"
status: "published"
draft: false
featured: false
license: "CC BY 4.0"
cover_image: "https://example.com/cover.jpg"
language: "zh-CN"
reading_time: 5
word_count: 1200
series: "系列名称"
series_order: 1
related: []
notes: ""
---
```

### 5.4 Frontmatter生成工具

```python
#!/usr/bin/env python3
"""
frontmatter_builder.py - Frontmatter生成工具
"""

from datetime import datetime
from typing import List, Optional

class FrontmatterBuilder:
    """Frontmatter构建器"""

    def __init__(self):
        self.fields = {}

    def set(self, key: str, value):
        """设置字段"""
        self.fields[key] = value
        return self

    def build(self, style='compact') -> str:
        """
        构建frontmatter

        Args:
            style: 'minimal', 'compact', 'full'
        """
        if style == 'minimal':
            return self._build_minimal()
        elif style == 'compact':
            return self._build_compact()
        else:
            return self._build_full()

    def _build_minimal(self) -> str:
        """最小化模板"""
        lines = ["---"]

        essential = ['title', 'source_url', 'date']
        for key in essential:
            if key in self.fields:
                lines.append(self._format_field(key, self.fields[key]))

        if 'tags' in self.fields:
            lines.append(self._format_field('tags', self.fields['tags']))

        lines.append("---")
        return "\n".join(lines)

    def _build_compact(self) -> str:
        """紧凑模板"""
        lines = ["---"]

        compact_fields = [
            'title', 'source_url', 'source', 'author',
            'published_date', 'collected_at',
            'category', 'tags', 'description'
        ]

        for key in compact_fields:
            if key in self.fields:
                lines.append(self._format_field(key, self.fields[key]))

        lines.append("---")
        return "\n".join(lines)

    def _build_full(self) -> str:
        """完整模板"""
        lines = ["---"]

        # 按类别组织字段
        categories = {
            '基本信息': ['title', 'slug'],
            '来源信息': ['source_url', 'source', 'canonical_url'],
            '作者信息': ['author', 'author_url', 'translator'],
            '时间信息': ['published_date', 'modified_date', 'collected_at'],
            '分类标签': ['category', 'categories', 'tags'],
            '内容描述': ['description', 'excerpt', 'summary'],
            '状态权限': ['status', 'draft', 'featured', 'license'],
            '媒体信息': ['cover_image', 'image'],
            '技术信息': ['language', 'reading_time', 'word_count'],
            '关联信息': ['series', 'series_order', 'related'],
        }

        for cat_name, cat_fields in categories.items():
            has_fields = any(f in self.fields for f in cat_fields)
            if has_fields:
                lines.append(f"# {cat_name}")
                for key in cat_fields:
                    if key in self.fields:
                        lines.append(self._format_field(key, self.fields[key]))
                lines.append("")

        lines.append("---")
        return "\n".join(lines)

    def _format_field(self, key: str, value) -> str:
        """格式化字段"""
        if value is None:
            return f"{key}:"

        if isinstance(value, bool):
            return f"{key}: {str(value).lower()}"

        if isinstance(value, (list, tuple)):
            if not value:
                return f"{key}: []"
            items = ', '.join([f'"{self._escape(str(v))}"' for v in value])
            return f"{key}: [{items}]"

        if isinstance(value, str):
            # 检查是否需要引号
            if self._needs_quotes(value):
                return f'{key}: "{self._escape(value)}"'
            return f"{key}: {value}"

        return f"{key}: {value}"

    def _needs_quotes(self, value: str) -> bool:
        """检查值是否需要引号"""
        # 包含特殊字符
        special_chars = [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '\`']
        if any(c in value for c in special_chars):
            return True

        # 以特殊字符开头
        if value and value[0] in ['*', '&', '!', '?', '|', '-', '>', '%', '@', '\`']:
            return True

        # 看起来像数字但实际是字符串
        if value.isdigit():
            return True

        # 包含换行
        if '\n' in value or '\r' in value:
            return True

        return False

    def _escape(self, value: str) -> str:
        """转义字符串"""
        return value.replace('"', '\"').replace('\n', ' ').replace('\r', '')


# 便捷函数
def create_frontmatter(metadata: dict, style='compact') -> str:
    """
    从元数据字典创建frontmatter

    使用示例:
        fm = create_frontmatter({
            'title': '文章标题',
            'source_url': 'https://example.com',
            'author': '作者',
            'tags': ['python', 'tutorial']
        })
    """
    builder = FrontmatterBuilder()
    for key, value in metadata.items():
        builder.set(key, value)
    return builder.build(style)


if __name__ == "__main__":
    # 示例
    metadata = {
        'title': 'Python Markdown Tutorial',
        'source_url': 'https://example.com/tutorial',
        'author': 'John Doe',
        'published_date': '2024-01-15',
        'tags': ['python', 'markdown', 'tutorial'],
        'category': 'Programming'
    }

    print("=== Minimal ===")
    print(create_frontmatter(metadata, 'minimal'))

    print("\n=== Compact ===")
    print(create_frontmatter(metadata, 'compact'))

    print("\n=== Full ===")
    print(create_frontmatter(metadata, 'full'))
```

---

## 6. 完整工作流示例

### 6.1 从URL到整理好的Markdown

```python
#!/usr/bin/env python3
"""
complete_workflow.py - 完整工作流示例
"""

import os
from claude_article_collector import ClaudeArticleCollector
from markdown_cleaner import create_default_cleaner
from image_processor import ImageProcessor

def complete_workflow(url, output_dir="./my_library"):
    """
    完整工作流：采集 -> 清理 -> 图片处理 -> 保存
    """
    # 1. 采集文章
    print("=" * 50)
    print("Step 1: Collecting article...")
    collector = ClaudeArticleCollector(output_dir=output_dir)
    result = collector.collect(url, options={
        'include_metadata': True,
        'include_images': True
    })

    if not result['success']:
        print(f"Failed: {result.get('error')}")
        return None

    filepath = result['filepath']

    # 2. 清理Markdown
    print("\nStep 2: Cleaning markdown...")
    cleaner = create_default_cleaner()

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = cleaner.clean(content)

    # 3. 处理图片
    print("Step 3: Processing images...")
    image_dir = os.path.join(output_dir, 'images')
    processor = ImageProcessor(output_dir=image_dir)

    processed = processor.process_markdown(
        cleaned,
        article_url=url,
        image_base_path='images'
    )

    # 4. 保存最终结果
    print("Step 4: Saving final result...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(processed)

    print(f"\n✅ Complete! File saved: {filepath}")

    return {
        'filepath': filepath,
        'title': result['metadata']['title'],
        'word_count': len(processed.split())
    }


# 运行示例
if __name__ == "__main__":
    url = input("Enter URL to collect: ")
    result = complete_workflow(url)

    if result:
        print(f"\n📄 Title: {result['title']}")
        print(f"📝 Word count: {result['word_count']}")
```

---

## 7. 推荐工具组合

### 7.1 最佳实践组合

| 场景 | 推荐工具 | 理由 |
|-----|---------|------|
| **日常手动采集** | MarkDownload + Obsidian | 一键保存，无缝集成 |
| **批量自动化** | trafilatura + Python脚本 | 学术级精度，可编程 |
| **AI/LLM工作流** | cpdown + Claude Code | Token优化，AI友好 |
| **命令行用户** | trafilatura CLI | 简单高效，无需编程 |
| **需要浏览器渲染** | Playwright + markdownify | 支持JS渲染的页面 |

### 7.2 依赖安装清单

```bash
# 核心依赖
pip install trafilatura markdownify requests beautifulsoup4 lxml

# 可选依赖
pip install html2text newspaper3k

# 浏览器渲染（用于JS页面）
pip install playwright
playwright install chromium

# 开发依赖
pip install pytest black flake8 mypy
```

---

## 8. 常见问题

### Q1: 如何处理需要登录的页面？

```python
# 使用requests.Session保持登录状态
import requests

session = requests.Session()
# 先登录
session.post('https://example.com/login', data={'user': 'xxx', 'pass': 'xxx'})
# 然后获取内容
response = session.get('https://example.com/protected-article')
```

### Q2: 如何处理JS渲染的页面？

```python
# 使用Playwright
from playwright.sync_api import sync_playwright

def fetch_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html
```

### Q3: 如何避免重复采集？

```python
# 使用URL哈希检查
import hashlib
import os

def is_already_collected(url, output_dir):
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    # 检查是否存在包含该hash的文件
    for filename in os.listdir(output_dir):
        if url_hash in filename:
            return True
    return False
```

---

*文档版本: 1.0*
*最后更新: 2024年*
