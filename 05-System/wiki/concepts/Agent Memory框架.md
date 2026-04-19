# Agent Memory框架

**定义**: 为AI Agent提供记忆能力的中间件框架
**当前状态**: 繁荣但可能是过渡态
**终局判断**: 独立Memory框架赛道可能在未来两年内消失

## 概述

Agent Memory框架是一类专门为AI Agent设计记忆能力的中间件产品。它们通常提供episodic（情景记忆）、semantic（语义记忆）、reflection/procedural（反思/程序性记忆）等多层存储，以及consolidation（整合）、retrieval（检索）、forgetting（遗忘）等机制。

## 四种类型

根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析，当前市面上的Memory框架可分为四类：

### 1. 数据库套壳SDK
**代表**: Mem0, LangMem, MemoryScope, SuperMemory

**特点**:
- 在数据库（PG+pgvector或SQLite）上封装API
- 提供extract/store/retrieve/update操作
- episodic和semantic分表存储
- 重要性打分、时间衰减规则

**命运**: 会被Skill + 模型直接写SQL替代

### 2. 知识图谱/时序图谱构建器
**代表**: Graphiti, Cognee, Hindsight

**特点**:
- bi-temporal knowledge graph
- 增量实体消歧
- 冲突检测与失效
- 混合检索（语义+关键词+图遍历）

**命运**: 策略层被模型吸收，存储层归回数据库

### 3. Agent Runtime/Agent OS
**代表**: Letta (MemGPT)

**特点**:
- 把context window当作RAM
- 把外部存储当作Disk
- 通过tool call在两者之间swap
- 操作系统意义上的虚拟内存管理

**命运**: 应归入Harness赛道，不是Memory赛道

### 4. 其他
大多数是"替Agent建表和写SQL"，无技术壁垒

## 为什么独立Memory框架没有未来

### 1. 产业结构上没位置

在"三分天下"终局架构中：
- **模型层**: 提供智力（Anthropic、OpenAI等）
- **Harness层**: 驾驭执行（Claude Code、Cursor、Devin等）
- **数据库层**: 管理记忆（PostgreSQL、SQLite等）

Memory框架试图在三者之间插入一层，但三方都互相制衡，没有给中间商留位置。

### 2. 技术上无壁垒

- 核心工作就是"建表和SQL"
- 任何工程师一个周末就能写出基础版
- Claude的Skills机制已证明可行
- 一张markdown + 模型自己写SQL就能替代

### 3. The Bitter Lesson

Memory框架硬编码的"认知策略"（信息价值判断、分层决策、检索策略）属于"替AI做决策"的领域特定知识，根据Rich Sutton的《The Bitter Lesson》，这类方法长期必输给通用方法。

随着模型变强，这些手工策略会被"模型自己写SQL"的通用方法替代。

## 真正的壁垒在哪

### 数据库层

PostgreSQL将成为通用Agent记忆层的终局：
- **线缆协议是事实标准**: 模型在训练语料里见过几百万次SQL，天然会说
- **扩展生态覆盖所有检索原语**: pgvector、tsvector、AGE、TimescaleDB、PostGIS、Citus
- **不在AI冲击范围内**: 物理世界持久化，非信息加工

### Harness层

Claude Code、Cursor、Devin、OpenClaw、Hermes等产品负责驾驭执行，这块还在成形中。

### 模型层

 Anthropic、OpenAI等模型厂商提供智力，这块会打血战。

## 相关概念

- [[三分天下架构]]
- [[The Bitter Lesson]]
- [[Agent Runtime]]
- [[线缆协议]]
