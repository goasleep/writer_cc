---
type: entity
name: "Hermes Agent"
category: "软件产品"
---

# Hermes Agent

Hermes Agent 是由 [[Nous Research]] 开发的开源个人 AI 助理工具。

## 核心特性

### 定位
- **开源免费**：MIT 协议
- **自学习型**："自己会长大的助手"，强调 AI 自学习能力
- **跨平台**：支持 Windows（需 WSL2）、macOS、Linux

### 技术亮点

1. **程序性记忆**：完成复杂任务（5+ 次工具调用）后自动提炼成 Skill，后续使用中自动优化路径
2. **三层学习机制**：
   - [[事实记忆]]：`MEMORY.md`（环境/项目信息，约 2200 字符）+ `USER.md`（用户偏好/习惯，约 1375 字符）。会话开始时作为 [[frozen snapshot]] 注入 system prompt，保护 prompt cache。
   - [[会话检索]]：`session_search` 基于 SQLite + FTS5 的历史对话全文检索，按需召回，非常驻上下文。
   - [[过程记忆]]：`skill_manage` 工具支持创建、修补、编辑、删除 skill，记录可复用的做事方法。
3. **后台 review**：主任务结束后由独立 review agent 异步判断是否有用户偏好或技能值得沉淀。
4. **框架级安全**：
   - 命令执行授权审批（单次/会话/永久/拒绝）
   - 第三方 Skills 安全扫描（防数据泄露、提示词注入）
   - 容器隔离、凭证泄露拦截、路径穿越防护

### 生态

- **GitHub**：两个月从零飙到 3 万+ 星
- **文档**：结构清晰、层次分明
- **Slash 命令**：`/tools`、`/model`、`/skills`、`/personality`、`/voice` 等
- **性格切换**：内置 14 种性格（technical、concise、catgirl、pirate 等）

### 对比

与 [[OpenClaw]] 的对比：
- **设计哲学**：Hermes 强调"AI 自学习"，OpenClaw 强调"用户控制权"
- **Skills**：Hermes 自动生成，OpenClaw 人工编写
- **安装**：Hermes 更简单（一键脚本），OpenClaw 配置更复杂

### 在三分天下架构中的定位

根据[[三分天下：为什么Agent Memory框架是死路]]的分析，Hermes Agent属于**Harness层**产品：

- **定位**：Agent Runtime / Agent OS
- **职责**：驾驭执行层，负责把模型套起来、完成具体任务
- **核心能力**：加载Skills、组织context、调用工具、处理循环
- **同类产品**：Claude Code、Cursor、Devin、OpenClaw

在"三分天下"终局架构中，Hermes处于中间层：模型层 → **Hermes (Harness)** → 数据库层

## 相关链接

- GitHub: https://github.com/NousResearch/hermes-agent
- 对比文章：
  - [[很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？]]
  - [[拆解 Hermes Agent 的三层学习机制：OpenClaw 加自总结 Skills 后，差异还剩什么？]]
