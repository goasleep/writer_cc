---
type: concept
status: active
---

# Secret

Kubernetes 提供的核心 API 对象，专门用于保存敏感信息（密码、令牌、TLS 证书等）。默认情况下存储在 etcd 中未加密。

## 关键特性

- 支持标记为 Immutable（v1.19+）
- 与 ConfigMap 类似，但额外增加了安全保护措施
- 生产环境中建议配合外部密钥管理系统使用

## 关联

- [[Kubernetes 配置管理技术选型与云原生实践指南]]
- [[ConfigMap]]
<!-- - [[Kubernetes]] -->
