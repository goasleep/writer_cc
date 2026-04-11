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
2. **三层记忆系统**：
   - MEMORY.md：环境和项目信息（2200 字符上限）
   - USER.md：用户偏好和习惯（1375 字符上限）
   - Session Search：SQLite 全文检索 + 大模型摘要
3. **框架级安全**：
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

## 相关链接

- GitHub: https://github.com/NousResearch/hermes-agent
- 对比文章：[[很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？]]
