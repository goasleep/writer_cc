---
type: concept
status: active
---

# LLM Wiki

由 Andrej Karpathy 提出的一种知识管理模式：利用 LLM 持续维护一个结构化的 markdown 知识库，使知识成为持久、复利增长的资产。

## 核心特征

- 区别于 RAG：知识在 ingest 时就被编译进 wiki，而非查询时临时拼接
- 三层架构：Raw sources → The wiki → The schema
- 三大操作：Ingest、Query、Lint
- 由 LLM 负责维护，人类负责策展和提问

## 关联

- [[LLM Wiki (source)]]
- [[Andrej Karpathy]]
- [[RAG]]
- [[Memex]]
