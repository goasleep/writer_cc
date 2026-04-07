---
type: source
title: LLM Wiki
source_url: https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/ac46de1ad27f92b28ac95459c782c07f6b8c964a/llm-wiki.md
source: GitHub Gist
author: Andrej Karpathy
published_date: "2024"
collected_at: "2026-04-07"
---

# LLM Wiki

## 核心论点

Karpathy 提出了一种不同于 RAG 的知识管理模式：让 LLM 持续维护一个结构化的 markdown wiki，使知识成为**持久、复利增长的资产**，而不是每次查询都重新推导的碎片。

## 关键要点

1. **与 RAG 的本质区别**
   - RAG 每次查询都从零拼接片段，没有知识积累
   - LLM Wiki 在文献进入时就将信息编译进结构化页面， cross-reference 和矛盾点已经被标记

2. **三层架构**
   - **Raw sources**: 不可变的原始文档（文章、论文、图片）
   - **The wiki**: LLM 全权生成和维护的 markdown 页面集合
   - **The schema**: 告诉 LLM 如何维护 wiki 的规则文档（如 CLAUDE.md / AGENTS.md）

3. **三大操作**
   - **Ingest**: LLM 读取新来源，提取要点，更新 wiki 中 10-15 个相关页面
   - **Query**: 在 wiki 而非 raw sources 上提问，优质回答可再写回 wiki
   - **Lint**: 定期检查矛盾、过时主张、孤儿页面、缺失概念页

4. **Index 与 Log**
   - `index.md`: 内容导向的 wiki 目录，按类别组织，附带一行摘要
   - `log.md`: 追加式的操作日志，记录每次 ingest、query、lint

5. **适用场景**
   - 个人成长日志
   - 学术研究
   - 读书笔记（可像 Tolkien Gateway 那样构建 companion wiki）
   - 企业内部知识库
   - 竞争分析、尽职调查、旅行规划等

6. **工具建议**
   - Obsidian Web Clipper 快速剪藏
   - qmd 作为本地 wiki 搜索引擎
   - Marp + Dataview 扩展输出形式

7. **哲学根基**
   - 人类放弃 wiki 是因为维护负担超过价值
   - LLM 不会厌倦、不会遗漏 cross-reference，单次操作可更新十几个文件
   - 与 Vannevar Bush 的 Memex（1945）精神相通：私人、主动策展、文档间关联与文档本身同等重要

## 原文链接

- [GitHub Gist 原文](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/ac46de1ad27f92b28ac95459c782c07f6b8c964a/llm-wiki.md)
