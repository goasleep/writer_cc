---
type: concept
created: 2026-04-09
---

# OpenTelemetry

OpenTelemetry（OTel）是一个开源的可观测性框架，由 CNCF 托管，提供统一的 API、SDK 和数据格式来采集指标（Metrics）、日志（Logs）和链路追踪（Traces）。

## 与 W3C Trace Context 的关系

- OpenTelemetry 默认使用 W3C Trace Context 作为追踪上下文的传播格式
- 在大多数自动插桩场景中无需额外配置
- 在未插桩系统、遗留系统或异步执行上下文（如消息队列、线程池）中可能需要手动注入/提取 traceparent

## 相关来源

- [[Trace Context 关键字段]]
