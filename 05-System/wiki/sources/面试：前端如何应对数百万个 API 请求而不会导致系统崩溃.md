---
type: source
source_url: https://mp.weixin.qq.com/s/YqOAy5edIyOkA_OB_EpDng
original_author: Sanjeevani Bhandari
collected_at: 2026-04-13
language: zh-CN
article_type: 技术科普/面试指南
quality_tier: B
---

# 面试：前端如何应对数百万个 API 请求而不会导致系统崩溃

## 核心观点

文章将"百万级 API 请求"这一通常归于后端的高并发命题，转化为前端开发者可直接操作的面试题与工程实践清单。核心论点是：糟糕的前端 API 调用模式会浪费请求、增加服务器压力并 ruin 用户体验；前端架构设计对可扩展性的重要性不亚于后端伸缩能力。

## 关键要点

1. **减少不必要的请求**
   - 利用浏览器缓存（`Cache-Control`）
   - 客户端缓存（Context、Redux、React Query / TanStack Query）
   - CDN 边缘缓存静态内容

2. **控制请求频率**
   - 防抖（Debounce）：搜索框场景等待用户停止输入（300–500ms）后再请求
   - 节流（Throttle）：滚动加载等场景限制频率

3. **合并请求**
   - 将多个查询合并为一次批量请求
   - 使用 GraphQL 只取所需数据
   - 对相似请求分组

4. **异步加载**
   - 先渲染已有数据，后台静默刷新
   - 只更新变化部分（Instagram、Twitter 的 Feed 策略）

5. **优雅降级与容错**
   - 展示缓存或上一次成功数据
   - 提供重试机制
   - 指数退避（exponential backoff）避免雪崩

6. **监控**
   - 使用 Sentry、LogRocket、Datadog RUM 跟踪 API 错误率、延迟、重试次数

7. **推动后端改进**
   - 为前端场景定制接口
   - 支持聚合响应
   - 合理的 rate limit 与缓存策略

## 可仿写元素

- 用生活化反差建立代入感（"早上并不会想着处理百万请求" vs "某天项目爆火"）
- 第二人称质问读者，制造紧迫感
- 金句包装术："每一个不必要的 API 调用，都是对性能的'犯罪'"
- 短段落 + emoji 的节奏控制
