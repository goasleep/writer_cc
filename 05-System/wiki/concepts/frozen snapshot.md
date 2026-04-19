---
type: concept
aliases: [prompt snapshot, system prompt cache protection]
related:
  - "[[事实记忆]]"
  - "[[Hermes Agent]]"
---

# frozen snapshot

**frozen snapshot** 是 Hermes Agent 中保护 prompt cache 的一种机制：在会话开始时将 `MEMORY.md` / `USER.md` 的内容捕获为固定的 system prompt 快照，会话中途即使写入新记忆，也不改变当前会话的系统提示，直到下一轮新会话才生效。

## 为什么需要 frozen snapshot

- 如果每一轮都修改 system prompt，缓存前缀会不断失效。
- 失效会导致成本和延迟显著放大。
- 通过"先冻结、后生效"的策略，在保证记忆持久化的同时维护上下文稳定性。

## 工程实现

- `MemoryStore.load_from_disk()` 执行完毕后，内容被捕获到 `_system_prompt_snapshot`。
- 会话中途调用 memory 工具写入时，数据立刻落盘，但不更新当前 system prompt。
- 新会话启动时重新加载，最新记忆自然进入主上下文。

## 设计启示

- 上下文不是越多越好，稳定前缀与动态内容需要分层管理。
- 长期记忆的更新频率应与 prompt 的稳定性要求相匹配。
