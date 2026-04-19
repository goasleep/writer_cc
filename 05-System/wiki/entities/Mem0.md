# Mem0

**Type**: Memory框架/数据库套壳SDK
**Category**: Agent基础设施

## 概述

Mem0是一个Agent Memory框架项目，属于**数据库套壳SDK**类型。它在数据库（通常是PG+pgvector或SQLite）上封装一套"extract/store/retrieve/update"的API，提供episodic和semantic两层存储，以及重要性打分和时间衰减规则。

## 技术特点

- 核心：封装数据库操作的API层
- 存储：episodic层（情景记忆）+ semantic层（语义记忆）
- 策略：重要性打分、时间衰减、反思压缩
- 检索：向量召回 + BM25 + cross-encoder重排 + RRF融合

## 市场表现

- 已完成多轮融资
- GitHub star持续增长
- 被列为早期"数据库套壳SDK"代表项目

## 终局判断

根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析：

**命运**: 会被 **Skill + 模型直接写SQL** 替代

**理由**:
1. 技术上无壁垒，只是"建表和SQL"
2. 任何工程师一个周末就能写出基础版
3. Claude的Skills机制已证明这条路可行
4. 一旦模型厂商发布官方memory skill，从模型侧被架空

**真正的价值**:
- 运营和产品壁垒（UI、SaaS控制台、开发者关系）
- 非技术壁垒

## 相关链接

- 类似项目: LangMem, MemoryScope, SuperMemory
- 对标架构: PostgreSQL + Skills + Claude Code
