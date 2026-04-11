---
type: concept
created: 2026-04-09
---

# W3C Trace Context

W3C Trace Context 是万维网联盟（W3C）制定的分布式追踪标准，定义了在微服务架构中跨服务传递追踪上下文的标准格式。它解决了不同厂商追踪系统（如 Zipkin、Jaeger、AWS X-Ray）之间互操作性差的问题。

## 核心组件

- **traceparent**：标准追踪头，包含 version、trace-id、parent-id、trace-flags
- **tracestate**：供应商扩展头，用于传递厂商特定的追踪数据

## 设计目标

- 统一多厂商追踪系统的 HTTP 头格式
- 保持头部轻量，避免传递完整历史路径
- 支持无状态逐跳传播与后台事后组装

## 相关来源

- [[Trace Context 关键字段]]
