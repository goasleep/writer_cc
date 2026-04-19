# Beren Millidge

**领域**: 认知科学、AI研究
**知名贡献**: Agent Harness的CPU类比（2023）

## 概述

Beren Millidge是一位认知科学家和AI研究者。根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的引用，他在2023年提出了一个被广泛引用的类比，帮助理解Agent Harness的本质。

## 核心贡献

### LLM的CPU类比（2023）

> 裸的LLM是一颗没有RAM、没有磁盘、没有I/O的CPU。

**类比分解**:
- **上下文窗口**: 充当内存（RAM）
- **外部数据库**: 充当磁盘
- **工具集**: 充当设备驱动
- **Harness**: 让这台机器持续跑起来的调度、执行、校验和保护机制

## 意义

这个类比之所以重要，是因为：

1. **澄清角色**: 模型是"处理器"，不是完整系统
2. **凸显Harness**: 让模型持续运转需要外部系统
3. **工程视角**: 把AI问题拉回到系统工程问题

## 类比详解

### 没有Harness的LLM
就像一颗裸CPU：
- 有计算能力
- 但没有持久存储
- 无法与外部世界交互
- 无法持续运行复杂任务

### 有Harness的LLM
就像完整计算机：
- CPU（模型）提供智能
- RAM（上下文窗口）提供工作内存
- 磁盘（数据库）提供持久存储
- 设备驱动（工具）提供交互能力
- 操作系统（Harness）协调一切

## 相关概念

- [[Harness Engineering]]
- [[Agent Runtime]]
- [[Agent]]

## 相关实体

- [[Claude Code]]
- [[Akshay]]
