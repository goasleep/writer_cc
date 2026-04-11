---
type: entity
name: "Granian"
category: "软件产品"
---

# Granian

Granian 是一个现代的 Python 应用服务器，支持 Rust 实现的高性能并发处理。

## 核心特性

### 异步能力
- 原生支持异步 Python 应用
- 兼容 ASGI 应用（如 Quart、FastAPI）
- 单进程即可处理高并发请求

### 部署模式
- **Web Garden 模式**：一个 orchestrator + 多个 worker 进程
- **单 Worker 模式**：全异步代码下，单 worker 即可满足需求

### 性能优势
- 低 CPU 占用
- 更低的内存占用（相比多进程模式）
- 优雅的 worker 进程重启和 TTL 管理

## 使用场景

在 [[Michael Kennedy]] 的优化实践中，Granian 的单异步 worker 模式配合 Quart 框架，使得内存使用从 1,280 MB 降低到 536 MB（节省 542 MB）。

## 相关实体

- [[Talk Python]]
- [[Michael Kennedy]]

## 相关概念

- [[Async Workers]]
- [[Quart]]
- [[Memory Optimization]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
- GitHub: https://github.com/emmett-framework/granian
