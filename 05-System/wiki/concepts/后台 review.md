---
type: concept
aliases: [background review, review agent, self-improving runtime]
related:
  - "[[过程记忆]]"
  - "[[事实记忆]]"
  - "[[Hermes Agent]]"
---

# 后台 review

**后台 review（Background Review）** 是 Agent 系统中在主任务完成后，由独立的 review agent 异步评估本次会话是否有值得沉淀为长期资产的机制。它是学习闭环的关键工程组件。

## 核心特征

- **触发时机**：按轮数或迭代数阈值触发（如每 10 轮），在主任务结束后执行。
  - `_turns_since_memory`：触发事实记忆 review
  - `_iters_since_skill`：触发过程记忆 review
- **执行方式**：fork 一个安静的 review agent，运行在独立线程，stdout/stderr 重定向到 `/dev/null`。
- **评估内容**：
  - 用户是否透露了新的偏好、人设、工作风格
  - 是否使用了非平凡方法、经历了试错改道
  - 是否有可复用经验值得创建或更新 skill
- **输出**：如果没有值得保存的内容，返回 `Nothing to save.`；否则执行 memory 或 skill 工具操作。

## 设计原则

- **不抢主任务注意力**：经验沉淀是好事，但不能干扰当前工作。先把活干完，复盘的事后台跑。
- **阈值可配置**：触发频率可通过配置文件调整，适应不同任务密度。
- **与主 agent 共享 memory store**：保证 review agent 能访问完整的上下文。

## 在 Hermes 中的实现

- review prompt 有三种：`_MEMORY_REVIEW_PROMPT`、`_SKILL_REVIEW_PROMPT`、`_COMBINED_REVIEW_PROMPT`
- review 完成后扫描消息历史，提取成功的工具操作，生成紧凑摘要通知用户，如：
  - `💾 Memory updated · Skill 'docker-network-fix' created`
