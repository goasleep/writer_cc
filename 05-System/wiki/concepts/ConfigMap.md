---
type: concept
status: active
---

# ConfigMap

Kubernetes 提供的核心配置管理 API 对象，用于存储非敏感的配置数据，支持键值对形式，可通过环境变量、命令行参数或存储卷的方式被 Pod 使用。

## 关键特性

- 单个 ConfigMap 大小限制 1MiB（etcd 约束）
- 不支持历史版本管理和灰度发布
- 以环境变量方式使用时需要重启 Pod 才能更新

## 关联

- [[Kubernetes 配置管理技术选型与云原生实践指南]]
- [[Secret]]
<!-- - [[Kubernetes]] -->
