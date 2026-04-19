---
type: source-summary
source_url: https://mp.weixin.qq.com/s/twOGltgevrfhLv6f90SCgg
title: 拆解 Hermes Agent 的三层学习机制：OpenClaw 加自总结 Skills 后，差异还剩什么？
author: ""
published_date: ""
ingested_at: 2026-04-14
---

# 拆解 Hermes Agent 的三层学习机制：OpenClaw 加自总结 Skills 后，差异还剩什么？

## 核心论点

Agent 的"长期记忆"不应被混为一谈。Hermes Agent 将其拆分为**事实记忆**（MEMORY.md / USER.md）、**会话检索**（session_search）和**过程记忆**（skill_manage）三层，每层有不同的存储、召回和更新机制。OpenClaw 与 Hermes 的差异不只在"有没有"这些功能，而在于经验沉淀被放置在运行时的哪一层、是否具备完整的生命周期管理。

## 关键洞察

- **事实记忆是随身备忘录，不是档案室**：Hermes 的 MEMORY.md / USER.md 容量很小（约 800 / 500 tokens），会话开始时作为 frozen snapshot 注入 system prompt，写入后本轮不生效，目的是保护 prompt cache。
- **SQLite + FTS5 是会话检索，不是内置记忆**：`session_search` 解决的是"上次我们怎么修的"这类问题，按需从历史 transcript 中召回，而不是替代 MEMORY.md。
- **skill_manage 是过程记忆的核心**：skills 记录的是"这类事下次该怎么做"，支持 create / patch / edit / delete，并有 `skills_guard` 做安全扫描。后台 review agent 在任务结束后判断是否有可复用经验值得沉淀。
- **差异在于运行时位置**：OpenClaw 更厚在 gateway / control / memory plane；Hermes 更厚在执行循环、学习闭环和长期资产分层。若 OpenClaw 仅做离线归档，而不让 skill 进入 Agent Runtime 的主路径，两者仍有本质区别。

## 工程细节亮点

- `MemoryStore.load_from_disk()` 捕获 `_system_prompt_snapshot`，保证 prompt 稳定。
- 内存写入使用 `tempfile.mkstemp()` + `os.fsync()` + `os.replace()` 做原子替换，并用 `fcntl.flock` 加锁。
- `_MEMORY_THREAT_PATTERNS` 扫描 prompt injection 和凭据泄露模式。
- `session_search` 的截断策略优先短语匹配，再退回到近邻共现和单词位置。
- 外部 memory provider（如 Honcho）是 additive，不会替代内置记忆。

## 可迁移概念

- [[事实记忆]] — 用户偏好、环境事实、稳定约定
- [[会话检索]] — 按需搜索历史对话与任务记录
- [[过程记忆]] — 可复用流程与技能（procedural memory / skills）
- [[后台 review]] — 任务结束后由独立 agent 判断经验沉淀
- [[frozen snapshot]] — 保护 prompt cache 的系统提示快照机制

## 相关文章

- [[很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？]]
- [[构建 Claude Code 的经验：我们如何使用 Skills]]
- [[LLM Wiki]]
