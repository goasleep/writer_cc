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
            'category', 'categories', 'tags', 'description'
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
        special_chars = [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']
        if any(c in value for c in special_chars):
            return True

        # 以特殊字符开头
        if value and value[0] in ['*', '&', '!', '?', '|', '-', '>', '%', '@', '`']:
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
    import argparse

    parser = argparse.ArgumentParser(description='Generate YAML frontmatter')
    parser.add_argument('--title', required=True, help='Article title')
    parser.add_argument('--url', required=True, help='Source URL')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--date', help='Published date')
    parser.add_argument('--tags', help='Tags (comma-separated)')
    parser.add_argument('--style', choices=['minimal', 'compact', 'full'], 
                        default='compact', help='Frontmatter style')

    args = parser.parse_args()

    metadata = {
        'title': args.title,
        'source_url': args.url,
    }

    if args.author:
        metadata['author'] = args.author

    if args.date:
        metadata['published_date'] = args.date
    else:
        metadata['published_date'] = datetime.now().strftime('%Y-%m-%d')

    if args.tags:
        metadata['tags'] = [t.strip() for t in args.tags.split(',')]

    print(create_frontmatter(metadata, args.style))
