---
type: source
source_url: https://www.kimi.com/share/19d7025e-f822-84ca-8000-0000dc808859
author: null
date: 2026-04-09
---

# Trace Context 关键字段

## 核心论点

这是一篇关于 W3C Trace Context 分布式追踪标准的问答式对话记录，以“用户提问 - AI 解答”的形式，深入浅出地解释了 `traceparent` 和 `tracestate` 两个 HTTP 头的结构、字段含义与协作机制。

## 关键内容

- **traceparent 格式**：`version-trace-id-parent-id-trace-flags`，其中 `trace-id` 全程不变，`parent-id` 每经过一个服务更新为当前 Span ID，`trace-flags` 控制采样决策。
- **tracestate 作用**：承载供应商特定的追踪数据，最多 32 个键值对，最近更新的键值对放在最左侧。
- **传播 vs 重组**：HTTP Header 中只传递“上一站”的 parent-id，但各服务上报 Span 时携带自己的 span-id 与 parent-id，后台 Collector 按 trace-id 分组、按 parent-id 建树，事后重组出完整调用链。
- **与 OpenTelemetry 的关系**：OpenTelemetry 默认使用 W3C Trace Context 作为传播格式，未插桩系统或异步场景（消息队列）可能需要手动注入/提取。

## 关键要点

- trace-id = 链路级锚点（高铁车次号），全程不变
- parent-id = 跳转级构建器（上一站到达口），每服务更新一次
- trace-flags = 控制级标记（是否拍照记录），控制采样行为
- 各服务无需知道完整历史路径，这种“无状态传递 + 事后组装”设计避免了头部膨胀与架构泄露

## 相关概念

- [[W3C Trace Context]]
- [[OpenTelemetry]]
- [[分布式追踪]]
- [[微服务]]
