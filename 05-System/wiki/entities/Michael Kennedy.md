---
type: entity
name: "Michael Kennedy"
category: "人物"
aliases: ["Michael Kennedy", "Talk Python"]
---

# Michael Kennedy

Michael Kennedy 是 Talk Python 的创始人，Python 社区的知名教育者和技术播客主持人。

## 主要项目

### Talk Python Training
- 在线 Python 教育平台
- 提供 Python 课程和培训服务
- 代码规模：178,000 行

### Talk Python 播客
- Python 技术播客主持人
- 访谈 Python 社区专家和开发者

## 技术实践

### 部署架构
- 采用"One Big Server"模式：将所有应用部署在单台大服务器上
- 运行 23 个容器（包括 web apps、APIs、数据库服务器）
- 服务器配置：16 GB 内存

### 技术栈偏好
- 异步框架：Quart（async Flask）
- 应用服务器：Granian
- 数据库：MongoDB
- 语言：Python 3.14+

## 写作风格

Michael 的技术文章具有以下特点：
- **数据驱动**：所有优化都有具体的 before/after 数字
- **实战导向**：基于真实生产环境，非 toy example
- **个人化叙述**：使用第一人称，分享心路历程
- **渐进式复杂度**：从架构到实现，逐步深入

## 相关链接

- 个人博客：https://mkennedy.codes
- Twitter: [@mkennedy](https://twitter.com/mkennedy)

## 相关文章

- [[Cutting Python Web App Memory Over 31%]]
- [[Raw+DC Database Pattern: A Retrospective]]

## 相关概念

- [[Memory Optimization]]
- [[Async Workers]]
- [[Import Isolation]]
