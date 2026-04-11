---
type: concept
name: "Async Workers"
category: "并发编程/架构模式"
---

# Async Workers

Async Workers 是指使用异步编程模型的 worker 进程，可以高效处理并发请求而不需要多进程或多线程。

## 工作原理

### 传统同步 Worker
```
请求1 → 处理 → 响应 → 请求2 → 处理 → 响应
```
每个请求阻塞期间，worker 无法处理其他请求。

### 异步 Worker
```
请求1 → 处理中...
请求2 → 处理中...    (并发)
请求3 → 处理中...
```
使用事件循环和协程，单个 worker 可同时处理多个请求。

## 内存优势

在 [[Michael Kennedy]] 的优化实践中：

| 模式 | Worker 数量 | 内存使用 |
|------|------------|----------|
| 多进程同步 | 2+ | 1,280 MB |
| 单进程异步 | 1 | 536 MB |

**节省 542 MB（42%）**

## 技术栈

### Python 异步生态
- **框架**：Quart（async Flask）、FastAPI、Starlette
- **服务器**：Granian、Uvicorn、Hypercorn
- **标准**：ASGI (Asynchronous Server Gateway Interface)

### 关键要求
- 异步数据库驱动（如 motor for MongoDB）
- 异步 HTTP 客户端（如 httpx、aiohttp）
- 全异步调用链（避免阻塞操作）

## 适用场景

✅ **适合**
- I/O 密集型应用（web APIs、数据库操作）
- 需要高并发处理的场景
- 内存受限的环境

❌ **不适合**
- CPU 密集型任务（应使用多进程）
- 阻塞操作无法改为异步的场景

## 相关概念

- [[Memory Optimization]]
- [[Raw+DC Pattern]]
- [[Quart]]
- [[Granian]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
