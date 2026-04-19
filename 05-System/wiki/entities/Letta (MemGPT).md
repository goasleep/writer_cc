# Letta (前MemGPT)

**Type**: Agent Runtime / Agent OS
**Category**: Agent基础设施

## 概述

Letta（原名MemGPT）是一个Agent Memory框架项目，但根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析，它**根本不是Memory框架**，而是**Agent Runtime/Agent OS**。

## 技术特点

- 核心能力：把context window当作RAM，外部存储当作Disk
- 让模型通过tool call在两者之间swap
- 本质：操作系统意义上的虚拟内存管理

## 架构定位

**正确的归类**: Agent Runtime / Agent OS，属于**Harness赛道**，而非Memory赛道

**理由**:
- 它做的是执行引擎层的工作
- 是Harness下位的执行引擎
- 应该与Claude Code、OpenClaw、Hermes等产品归为一类

## 技术门槛

- 门槛不低
- 有其独特价值
- 但赛道归属应该是Runtime/Harness，不是Memory

## 市场表现

- 已完成多轮融资
- 官方支持PostgreSQL + pgvector后端
- 如果真能做成Agent Runtime方向，会很有意思

## 相关链接

- 类似项目: Claude Code, OpenClaw, Hermes
- 后端支持: PostgreSQL + pgvector
