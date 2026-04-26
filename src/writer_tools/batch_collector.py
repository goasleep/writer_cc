#!/usr/bin/env python3
"""
batch_collector.py - 批量文章采集脚本
"""

import os
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from .collector import ArticleCollector

class BatchCollector:
    def __init__(self, output_dir="./articles", max_workers=5, url_index=None, url_index_callback=None):
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.collector = ArticleCollector(output_dir)
        self.url_index = url_index or {}
        self.url_index_callback = url_index_callback  # 回调函数，用于更新索引
        self.results = []
        self.skipped_count = 0

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
        """并行处理多个URL，带去重检查"""
        # 过滤掉已存在的URL
        unique_urls = []
        skipped_urls = []

        for url in urls:
            if url in self.url_index:
                skipped_urls.append(url)
                self.results.append({
                    'url': url,
                    'status': 'skipped',
                    'reason': 'URL already exists',
                    'existing_file': str(self.url_index[url])
                })
                self.skipped_count += 1
            else:
                unique_urls.append(url)

        if skipped_urls:
            print(f"📋 跳过 {len(skipped_urls)} 个已存在的URL")

        print(f"Processing {len(unique_urls)} URLs with {self.max_workers} workers...")

        completed = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self.collector.save_article, url): url
                for url in unique_urls
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
                        # 调用回调函数更新索引
                        if self.url_index_callback:
                            self.url_index_callback(url, result)
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
                    print(f"Progress: {total}/{len(unique_urls)} (Success: {completed}, Failed: {failed})")

        print(f"\nCompleted: {completed}, Failed: {failed}, Skipped: {len(skipped_urls)}")
        return self.results

    def save_report(self, filepath="collection_report.json"):
        """保存采集报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"Report saved: {filepath}")


# 使用示例
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Batch collect articles')
    parser.add_argument('input', help='Input file (txt, csv, or json)')
    parser.add_argument('-o', '--output', default='./articles', help='Output directory')
    parser.add_argument('-w', '--workers', type=int, default=5, help='Number of workers')
    parser.add_argument('--csv-column', default='url', help='CSV column name for URLs')

    args = parser.parse_args()

    batch = BatchCollector(output_dir=args.output, max_workers=args.workers)

    # 根据文件扩展名判断类型
    ext = os.path.splitext(args.input)[1].lower()

    if ext == '.csv':
        batch.from_csv(args.input, url_column=args.csv_column)
    elif ext == '.json':
        batch.from_json(args.input)
    else:
        batch.from_file(args.input)

    batch.save_report()
