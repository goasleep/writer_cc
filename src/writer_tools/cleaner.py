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
    import argparse

    parser = argparse.ArgumentParser(description='Clean and normalize markdown files')
    parser.add_argument('input', help='Input markdown file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('--in-place', action='store_true', help='Modify files in place')

    args = parser.parse_args()

    cleaner = create_default_cleaner()

    if os.path.isfile(args.input):
        # 处理单个文件
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()

        cleaned = cleaner.clean(content)

        output_path = args.input if args.in_place else (args.output or args.input.replace('.md', '_cleaned.md'))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"Cleaned: {output_path}")

    elif os.path.isdir(args.input):
        # 处理目录
        output_dir = args.output or args.input
        os.makedirs(output_dir, exist_ok=True)

        for filename in os.listdir(args.input):
            if filename.endswith('.md'):
                input_path = os.path.join(args.input, filename)

                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                cleaned = cleaner.clean(content)

                output_path = os.path.join(output_dir, filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)

                print(f"Cleaned: {output_path}")
