---
type: entity
name: "OpenClaw"
category: "软件产品"
aliases: ["小龙虾"]
---

# OpenClaw（小龙虾）

OpenClaw（昵称"小龙虾"）是一个开源的本地部署个人 AI 助理工具。

## 核心特性

### 定位
- **本地部署**：数据完全私有
- **多平台支持**：接 Telegram、飞书、企业微信等 14 个聊天平台
- **定时任务**：可设定时任务半夜自动执行

### 技术架构

1. **Skills 系统**：
   - 人工编写的 Markdown 文件
   - 社区贡献 5700+ 个 Skills
   - 安装什么就学会什么

2. **记忆系统**：
   - MEMORY.md + 每日笔记
   - 纯 Markdown，透明可编辑
   - 新增 Dreaming 功能
   - 依赖模型主动判断"值得存"（易漏存）

3. **安全机制**：
   - 主要依赖大模型判断力
   - 曾发生邮件被清空和 CVE-2026-25253 漏洞事件

### 生态

- **社区**：活跃，贡献了大量 Skills
- **文档**：较为零碎
- **Claude 订阅**：已被封杀，只能使用 API

### 对比

与 [[Hermes Agent]] 的对比：
- **设计哲学**：OpenClaw 强调"用户控制权"（你来指挥，AI 执行）
- **Skills**：OpenClaw 人工编写，Hermes 自动生成并支持运行时 patch/edit/delete
- **记忆**：OpenClaw 文件日记式；Hermes 分为 [[事实记忆]]、[[会话检索]]、[[过程记忆]] 三层，并有 [[frozen snapshot]] 和 [[后台 review]] 机制
- **安全**：OpenClaw 模型级，Hermes 框架级
- **厚度层**：OpenClaw 更厚在 gateway / control / memory plane；Hermes 更厚在执行循环、学习闭环和长期资产分层

### 在三分天下架构中的定位

根据[[三分天下：为什么Agent Memory框架是死路]]的分析，OpenClaw属于**Harness层**产品：

- **定位**：Agent Runtime / Agent OS
- **职责**：驾驭执行层，负责把模型套起来、完成具体任务
- **核心能力**：加载Skills、组织context、调用工具、处理循环
- **同类产品**：Claude Code、Cursor、Devin、Hermes Agent

在"三分天下"终局架构中，OpenClaw处于中间层：模型层 → **OpenClaw (Harness)** → 数据库层

## 关联

- [[为什么 AI Agent 框架都用 TypeScript？]]
- [[很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？]]
- [[拆解 Hermes Agent 的三层学习机制：OpenClaw 加自总结 Skills 后，差异还剩什么？]]
