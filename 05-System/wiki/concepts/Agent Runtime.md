---
type: concept
aliases: []
related: []
---

# Agent Runtime

**别名**: Agent OS, Agent执行引擎
**定位**: Harness层下位的执行引擎

AI Agent 的运行时环境，负责管理模型与外部世界的交互、执行流程控制、状态持久化与结果验证。Agent Runtime 是 Harness Engineering 的核心实现层，决定了 Agent 系统能否从 Demo 走向生产环境。

## 核心能力

根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析：

### 虚拟内存管理
- 把context window当作RAM（快速、有限、易失）
- 把外部存储当作Disk（慢速、海量、持久）
- 通过tool call在两者之间进行swap

### 执行引擎
- 管理Agent的执行循环
- 协调工具调用
- 处理状态管理

## 与Memory框架的区别

### Letta/MemGPT的误分类

Letta (MemGPT)常被归类为Memory框架，但这是**错误的**：

**它做的根本不是Memory框架该做的事**，而是：
- 操作系统意义上的虚拟内存管理
- Agent Runtime/Agent OS的执行引擎工作

**正确的归类**: 应该归到**Runtime/Harness赛道**，不是Memory赛道

### 为什么重要

这个区分很重要，因为：
- Memory框架是过渡态，会被替代
- Agent Runtime/Harness是终局架构的稳定一层

## 代表项目

- **Letta (前MemGPT)**: 核心能力是虚拟内存管理，后端支持PostgreSQL + pgvector
- **Claude Code**: 包含Runtime能力
- **OpenClaw**: 本地部署个人AI助理
- **Hermes Agent**: 开源自学习型AI助理
- **Cursor, Devin**: AI编程工具

## 在三分天下架构中的位置

```
模型层（智力）
    ↓
Harness层（驾驭执行）
    ↓
Agent Runtime（执行引擎）← 属于这一层
    ↓
数据库层（记忆）
```

Agent Runtime是**Harness层下位的执行引擎**，是Harness的一部分。

## 市场状态

- 这块还在摸索和成形
- Claude Code通过开源掀翻了壁垒
- Letta/MemGPT如果真能做成Agent Runtime方向会很有意思
- 局势仍在剧烈变动中

## 相关概念

- [[三分天下架构]]
- [[Agent Memory框架]]
- [[Harness Engineering]]

## 相关实体

- [[Letta (MemGPT)]]
- [[Claude Code]]
- [[OpenClaw]]
- [[Hermes Agent]]
