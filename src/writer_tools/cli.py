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


def cmd_collect(args):
    """采集单篇文章到 raw/articles/"""
    from .pipeline import collect_article

    raw_articles_dir = RAW_DIR
    result = collect_article(
        args.url, include_images=args.images, raw_dir=RAW_DIR.parent
    )

    if result.success:
        filepath = None
        if args.save_raw:
            filepath = _save_raw_article(result, raw_articles_dir)

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


def _save_raw_article(result, raw_dir: Path) -> str:
    """将采集结果保存到 raw/articles/"""
    import re
    import hashlib

    title = result.metadata.get("title", "")
    if title:
        safe_title = re.sub(r'[<>:\"/\\|?*]', "", title)[:80]
        filename = f"{safe_title}.md"
    else:
        url_hash = hashlib.md5(result.final_url.encode()).hexdigest()[:8]
        filename = f"article_{url_hash}.md"

    filepath = raw_dir / filename
    counter = 1
    original_path = filepath
    while filepath.exists():
        stem = original_path.stem
        filepath = raw_dir / f"{stem}_{counter}{original_path.suffix}"
        counter += 1

    raw_dir.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result.content)
    return str(filepath)


def cmd_batch(args):
    """批量采集文章"""
    batch = BatchCollector(
        output_dir=str(RAW_DIR),
        max_workers=args.workers,
    )

    ext = os.path.splitext(args.input)[1].lower()
    if ext == ".csv":
        results = batch.from_csv(args.input, url_column=args.csv_column)
    elif ext == ".json":
        results = batch.from_json(args.input)
    else:
        results = batch.from_file(args.input)

    batch.save_report(str(RAW_DIR / "collection_report.json"))


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
    elif args.command == "frontmatter":
        cmd_frontmatter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
