---
type: entity
name: "Quart"
category: "软件产品"
---

# Quart

Quart 是一个异步的 Python Web 框架，API 兼容 Flask，但完全支持异步编程。

## 核心特性

### Flask 兼容
- API 与 Flask 高度兼容
- 可以视为"async Flask"
- 降低迁移成本

### 异步原生
- 基于 ASGI 标准
- 支持异步路由、异步请求处理
- 可与异步数据库驱动协同工作

## 使用场景

### Talk Python 迁移案例

[[Michael Kennedy]] 将 Talk Python Training 从 Pyramid 框架重构到 Quart：
- 代码规模：178,000 行
- 重构工作：大量工作量
- 收益：为异步数据访问和单 worker 部署奠定基础

## 相关实体

- [[Flask]]
- [[Granian]]
- [[Talk Python]]
- [[Michael Kennedy]]

## 相关概念

- [[Async Workers]]
- [[Memory Optimization]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
- 官方文档：https://quart.palletsprojects.com/
