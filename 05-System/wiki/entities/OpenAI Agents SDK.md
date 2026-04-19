# OpenAI Agents SDK

**类型**: Agent开发框架/SDK
**开发商**: OpenAI
**Category**: Agent基础设施

## 概述

OpenAI Agents SDK是OpenAI提供的Agent开发工具包。根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的对比，它体现了不同的工具分类方法。

## 工具分类

OpenAI Agents SDK支持三类工具：

1. **函数工具（Function Tools）**
   - 传统的函数调用
   - 定义明确的输入输出

2. **托管工具（Hosted Tools）**
   - 由平台托管的服务
   - 无需自建基础设施

3. **MCP工具（Model Context Protocol Tools）**
   - 基于MCP协议的工具
   - 标准化的工具接口

## 设计理念

虽然分类方法不同，但要解决的问题和Claude Code类似：
- 工具注册
- 参数校验
- 执行环境隔离
- 结果回写

## 核心问题

工具系统不只是"给几个函数名"，还需要管理：
1. **工具如何注册**
2. **参数如何校验**
3. **执行环境是否隔离**
4. **结果如何回写成模型能理解的Observation**

## 关键洞察

> 模型知道可以调用什么工具，只是起点。它能不能在合适的时候调用、带着正确参数调用、在失败后继续恢复，才是Harness的事情。

## 相关概念

- [[Tool System]]
- [[Harness Engineering]]
- [[Agent Runtime]]

## 相关实体

- [[OpenAI]]
- [[Claude Code]]
- [[Akshay]]
