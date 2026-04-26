#!/usr/bin/env python3
"""
writer_tools CLI - 统一的命令行入口

使用方法:
    uv run writer-collect <url>              # 采集单篇文章到 00-Inbox/
    uv run writer-collect --batch urls.txt   # 批量采集
    uv run writer-collect --clean <file>     # 清理 Markdown
    uv run writer-collect --inbox            # 查看 Inbox 状态
"""

import argparse
import os
import sys
import json
from pathlib import Path

# 确保可以从 src 导入
sys.path.insert(0, str(Path(__file__).parent.parent))

from writer_tools import (
    ArticleCollector,
    ClaudeArticleCollector,
    BatchCollector,
    create_default_cleaner,
    create_frontmatter,
    collect_article as pipeline_collect_article,
    CollectResult,
)


VAULT_ROOT = Path(__file__).parent.parent.parent
RAW_DIR = VAULT_ROOT / "raw" / "articles"
WIKI_DIR = VAULT_ROOT / "05-System" / "wiki"
RESOURCES_DIR = VAULT_ROOT / "03-Resources" / "文章收藏"
URL_INDEX_FILE = VAULT_ROOT / "05-System" / "url_index.json"


def load_url_index() -> dict:
    """加载 URL 索引缓存文件"""
    if URL_INDEX_FILE.exists():
        try:
            with open(URL_INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  索引文件读取失败: {e}，将重新构建")

    return {}


def save_url_index(url_index: dict):
    """保存 URL 索引到缓存文件"""
    # 将 Path 对象转换为字符串以便 JSON 序列化
    serializable_index = {
        url: str(filepath) for url, filepath in url_index.items()
    }

    URL_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(URL_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_index, f, ensure_ascii=False, indent=2)


def build_url_index(raw_dir: Path, force_rebuild: bool = False) -> dict:
    """构建 URL -> 文件的映射索引，优先使用缓存"""
    # 如果不强制重建，先尝试加载缓存
    if not force_rebuild:
        cached_index = load_url_index()
        if cached_index:
            # 验证缓存中的文件是否仍然存在
            valid_index = {}
            for url, filepath_str in cached_index.items():
                filepath = Path(filepath_str)
                if filepath.exists():
                    valid_index[url] = filepath

            # 如果缓存有效性 > 90%，直接使用
            if len(valid_index) > len(cached_index) * 0.9:
                return valid_index

    # 缓存不存在、过期或强制重建，扫描目录
    print("🔍 构建 URL 索引...")
    url_index = {}

    if not raw_dir.exists():
        return url_index

    for filepath in raw_dir.glob("*.md"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 提取 frontmatter 中的 source_url
            if content.startswith("---"):
                # 找到 frontmatter 结束位置
                fm_end = content.find("---", 3)
                if fm_end != -1:
                    frontmatter = content[3:fm_end]
                    for line in frontmatter.split("\n"):
                        if line.strip().startswith("source_url:") or line.strip().startswith("url:"):
                            url = line.split(":", 1)[1].strip().strip('"\'')
                            if url:
                                url_index[url] = filepath
                                break
        except Exception as e:
            # 忽略读取错误的文件
            continue

    # 保存到缓存
    save_url_index(url_index)
    print(f"✅ 索引构建完成，共 {len(url_index)} 个URL")

    return url_index


def update_url_index(url_index: dict, url: str, filepath: Path):
    """更新 URL 索引，添加新的 URL 映射"""
    url_index[url] = filepath
    # 异步保存到缓存（避免频繁IO）
    save_url_index(url_index)


def cmd_collect(args):
    """采集单篇文章到 raw/articles/"""
    from .pipeline import collect_article

    raw_articles_dir = RAW_DIR

    # 建立 URL 索引用于去重检查
    url_index = build_url_index(raw_articles_dir)

    # 检查 URL 是否已存在
    if args.url in url_index:
        existing_file = url_index[args.url]
        print(f"\n⚠️  该文章已存在，跳过采集")
        print(f"📄 已有文件: {existing_file.name}")
        print(f"🔗 URL: {args.url}")
        return

    result = collect_article(
        args.url, include_images=args.images, raw_dir=RAW_DIR.parent
    )

    if result.success:
        filepath = None
        if args.save_raw:
            filepath = _save_raw_article(result, raw_articles_dir, url_index, args.url)

        print(f"\n✅ 采集成功")
        print(f"🔧 方法: {result.method}")
        print(f"📝 标题: {result.metadata.get('title', 'N/A')}")
        if filepath:
            print(f"📄 文件: {filepath}")
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"\n❌ 失败: {result.error}")
        sys.exit(1)


def _save_raw_article(result, raw_dir: Path, url_index: dict = None, original_url: str = None) -> str:
    """将采集结果保存到 raw/articles/，带去重检查和索引更新"""
    import re
    import hashlib
    from datetime import datetime

    # 双重检查：final_url 是否已存在
    final_url = result.final_url or result.metadata.get("url", "")
    if url_index and final_url in url_index:
        existing_file = url_index[final_url]
        print(f"⚠️  该 URL 已对应文件: {existing_file.name}")
        return str(existing_file)

    title = result.metadata.get("title", "")
    if title:
        safe_title = re.sub(r'[<>:\"/\\|?*]', "", title)[:80]
        filename = f"{safe_title}.md"
    else:
        url_hash = hashlib.md5(final_url.encode()).hexdigest()[:8]
        filename = f"article_{url_hash}.md"

    filepath = raw_dir / filename

    # 如果文件名冲突，添加后缀（保留向后兼容）
    counter = 1
    original_path = filepath
    while filepath.exists():
        stem = original_path.stem
        filepath = raw_dir / f"{stem}_{counter}{original_path.suffix}"
        counter += 1

    # 构建 frontmatter
    frontmatter = _build_frontmatter(result.metadata, final_url or original_url)

    raw_dir.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write("\n\n")
        f.write(result.content)

    # 更新 URL 索引
    if url_index and final_url:
        update_url_index(url_index, final_url, filepath)
    elif url_index and original_url:
        # 如果没有 final_url，使用原始 URL
        update_url_index(url_index, original_url, filepath)

    return str(filepath)


def _build_frontmatter(metadata: dict, url: str) -> str:
    """构建 YAML frontmatter"""
    from datetime import datetime

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

    return create_frontmatter(meta, style='compact')


def cmd_batch(args):
    """批量采集文章"""
    # 建立 URL 索引用于去重检查
    url_index = build_url_index(RAW_DIR)

    batch = BatchCollector(
        output_dir=str(RAW_DIR),
        max_workers=args.workers,
        url_index=url_index,
        url_index_callback=lambda url, filepath: update_url_index(url_index, url, Path(filepath))
    )

    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".csv":
        results = batch.from_csv(args.input, url_column=args.csv_column)
    elif ext == ".json":
        results = batch.from_json(args.input)
    else:
        results = batch.from_file(args.input)

    batch.save_report(str(RAW_DIR / "collection_report.json"))

    # 显示去重统计
    if hasattr(batch, 'skipped_count'):
        print(f"\n📊 去重统计: 跳过 {batch.skipped_count} 个重复文章")


def cmd_rebuild_index(args):
    """重建 URL 索引"""
    import time

    print("🔄 开始重建 URL 索引...")

    start_time = time.time()
    url_index = build_url_index(RAW_DIR, force_rebuild=True)
    elapsed = time.time() - start_time

    print(f"✅ 索引重建完成")
    print(f"📊 总计 {len(url_index)} 个URL")
    print(f"⏱️  耗时 {elapsed:.2f} 秒")
    print(f"📁 索引文件: {URL_INDEX_FILE}")

    if args.verbose:
        print("\n📋 索引内容:")
        for url, filepath in sorted(url_index.items()):
            print(f"  {url} -> {filepath.name}")


def cmd_clean(args):
    """清理 Markdown 文件"""
    cleaner = create_default_cleaner()

    if os.path.isfile(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
        cleaned = cleaner.clean(content)
        output_path = args.input if args.in_place else args.input.replace(".md", "_cleaned.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        print(f"✅ 已清理: {output_path}")
    elif os.path.isdir(args.input):
        for filename in os.listdir(args.input):
            if filename.endswith(".md"):
                input_path = os.path.join(args.input, filename)
                with open(input_path, "r", encoding="utf-8") as f:
                    content = f.read()
                cleaned = cleaner.clean(content)
                output_path = os.path.join(args.input, filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
                print(f"✅ 已清理: {output_path}")
    else:
        print(f"❌ 无效路径: {args.input}")
        sys.exit(1)


def cmd_inbox(args):
    """查看 Raw 状态"""
    if not RAW_DIR.exists():
        print("Raw 目录不存在")
        return

    files = [f for f in RAW_DIR.iterdir() if f.suffix == ".md"]
    print(f"📥 Raw 状态: {len(files)} 篇精修文章")
    for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
        print(f"  - {f.name}")
    if len(files) > 10:
        print(f"  ... 还有 {len(files) - 10} 篇")


def cmd_frontmatter(args):
    """生成 frontmatter"""
    metadata = {}
    if args.title:
        metadata["title"] = args.title
    if args.url:
        metadata["source_url"] = args.url
    if args.author:
        metadata["author"] = args.author
    if args.tags:
        metadata["tags"] = [t.strip() for t in args.tags.split(",")]
    print(create_frontmatter(metadata, style=args.style))


def main():
    parser = argparse.ArgumentParser(
        prog="writer-collect",
        description="个人写作库工具集 - 文章采集与整理",
    )
    subparsers = parser.add_subparsers(dest="command")

    # collect
    collect_parser = subparsers.add_parser("collect", help="采集单篇文章")
    collect_parser.add_argument("url", help="文章 URL")
    collect_parser.add_argument("--no-metadata", action="store_true", help="不包含元数据")
    collect_parser.add_argument("--images", action="store_true", default=True, help="包含图片")
    collect_parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    collect_parser.add_argument("--save-raw", action="store_true", default=True, help="保存原始提取内容到 raw/articles/")

    # batch
    batch_parser = subparsers.add_parser("batch", help="批量采集文章")
    batch_parser.add_argument("input", help="包含 URL 列表的文件")
    batch_parser.add_argument("-w", "--workers", type=int, default=5, help="并发数")
    batch_parser.add_argument("--csv-column", default="url", help="CSV 中的 URL 列名")

    # clean
    clean_parser = subparsers.add_parser("clean", help="清理 Markdown 文件")
    clean_parser.add_argument("input", help="输入文件或目录")
    clean_parser.add_argument("--in-place", action="store_true", help="原地修改")

    # inbox
    inbox_parser = subparsers.add_parser("inbox", help="查看 Inbox 状态")

    # rebuild-index
    index_parser = subparsers.add_parser("rebuild-index", help="重建 URL 索引缓存")
    index_parser.add_argument("-v", "--verbose", action="store_true", help="显示详细索引内容")

    # frontmatter
    fm_parser = subparsers.add_parser("frontmatter", help="生成 frontmatter")
    fm_parser.add_argument("--title", help="标题")
    fm_parser.add_argument("--url", help="来源 URL")
    fm_parser.add_argument("--author", help="作者")
    fm_parser.add_argument("--tags", help="标签，逗号分隔")
    fm_parser.add_argument(
        "--style", choices=["minimal", "compact", "full"], default="compact"
    )

    # 兼容旧用法: writer-collect <url>
    parser.add_argument("url_compat", nargs="?", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # 兼容旧用法
    if args.command is None and args.url_compat:
        args.command = "collect"
        args.url = args.url_compat
        args.no_metadata = False
        args.images = True
        args.json = False
        args.save_raw = True

    if args.command == "collect":
        cmd_collect(args)
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "clean":
        cmd_clean(args)
    elif args.command == "inbox":
        cmd_inbox(args)
    elif args.command == "rebuild-index":
        cmd_rebuild_index(args)
    elif args.command == "frontmatter":
        cmd_frontmatter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
