---
type: query
question: "obsidian vault 在其中扮演了什么角色？"
answered_at: "2026-04-07"
---

# obsidian vault 在其中扮演了什么角色？

## Answer

在这个个人写作库系统中，Obsidian Vault 扮演了**人类专属的阅读与创作入口**的角色，与 Claude Code 形成明确分工：

1. **用户阅读层**
   - 整个项目目录（`writer_cc/`）本身就是一个 Obsidian Vault，用户直接在 Obsidian 中打开即可阅读所有内容。
   - 通过 Obsidian 的双向链接、图谱视图（Graph View）和 Dataview 查询，用户可以直观地浏览 LLM 维护的 wiki 网络。

2. **人类创作层**
   - 用户在 Obsidian 中进行手写笔记、双向链接和写作创作，主要工作空间是 `03-Resources/`（人类手写笔记层）和 `01-Projects/`（进行中的写作项目）。
   - `05-System/wiki/` 原则上由 LLM 全权维护，用户只阅读、不主动编辑（除非明确修正错误）。

3. **与 LLM Wiki 的协同关系**
   - Karpathy 在 [[LLM Wiki]] 原文中也特别推荐了 Obsidian 生态：Obsidian Web Clipper 用于快速剪藏，Graph View 用于观察 wiki 的连接结构，Dataview 用于基于 frontmatter 的动态查询，Marp 用于将 wiki 内容直接生成演示文稿。
   - 在这个项目里，Obsidian 不仅是文件浏览器，更是 LLM Wiki 成果的**可视化终端**——LLM 负责后台的采集、结构化、cross-reference，人类负责在 Obsidian 中消费、联想和二次创作。

## Sources

- [[LLM Wiki]] — 原文推荐了 Obsidian Web Clipper、Graph View、Dataview 等工具作为 LLM Wiki 的前端载体
- [[个人写作库 - Claude Code 工作指令]]（CLAUDE.md）—— 明确定义 Obsidian 为用户阅读和写作的入口，与 Claude Code 的操作入口分离
