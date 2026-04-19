# OpenTelemetry Spans

**类型**: 可观测性概念
**标准**: OpenTelemetry Specification
**应用**: 分布式追踪（Distributed Tracing）

## 简介

OpenTelemetry Span是分布式追踪中的基本单位，表示系统中单个操作或工作单元的执行。Span捕获了操作的开始时间、结束时间、关键事件、属性和状态，提供了对系统行为和性能的深入洞察。在监控Celery任务重试和失败时，spans提供了追踪重试模式、链接重试尝试和识别失败原因的完美机制。

## Span核心概念

### Span生命周期

**基本流程**:
1. **创建**: 当操作开始时创建span
2. **激活**: 设置为当前活动的span
3. **添加事件**: 记录操作过程中的关键事件
4. **设置属性**: 添加元数据标签
5. **结束**: 操作完成时标记span结束

### Span结构

**必填字段**:
- **Trace ID**: 全局唯一标识符，链接所有相关spans
- **Span ID**: 单个span的唯一标识符
- **Parent Span ID**: 父span的ID（如果有）
- **Name**: 操作的描述性名称
- **Start Time**: 操作开始时间戳
- **End Time**: 操作结束时间戳

**可选字段**:
- **Attributes**: 键值对元数据
- **Events**: 时间戳事件
- **Links**: 到其他spans的链接
- **Status**: 操作状态（OK/ERROR）

## Span类型（Span Kind）

### CONSUMER
**用途**: 接收和处理消息的操作

**Celery任务示例**:
```python
with tracer.start_as_current_span(
    "celery.task.{task_name}",
    kind=SpanKind.CONSUMER
) as span:
    # 任务执行代码
```

### PRODUCER
**用途**: 发送消息的操作

### SERVER
**用途**: 处入站请求的操作

### CLIENT
**用途**: 出站请求的操作

### INTERNAL
**用途**: 应用程序内部的本地操作

## Celery任务重试追踪

### 重试感知Span设计

**关键属性**:
```python
span.set_attribute("celery.task.name", task_name)
span.set_attribute("celery.task.id", task_id)
span.set_attribute("celery.task.retry.current", retries)
span.set_attribute("celery.task.retry.max", max_retries)
span.set_attribute("celery.task.is_retry", is_retry)
```

**重试事件**:
```python
span.add_event("task_retry_attempt", {
    "retry.number": retries,
    "retry.max": max_retries,
    "retry.remaining": max_retries - retries
})
```

### 异常处理

**Retry异常**:
```python
except Retry as exc:
    span.set_attribute("celery.task.status", "retrying")
    span.add_event("task_scheduled_for_retry", {
        "retry.eta": str(exc.when) if hasattr(exc, 'when') else None,
        "retry.reason": str(exc)
    })
    if exc.__cause__:
        span.record_exception(exc.__cause__)
```

**MaxRetriesExceededError**:
```python
except MaxRetriesExceededError as exc:
    span.set_attribute("celery.task.status", "failed_max_retries")
    span.add_event("task_max_retries_exceeded", {
        "retry.attempts": retries,
        "retry.max": max_retries
    })
    span.record_exception(exc)
```

## Span最佳实践

### 属性命名规范

**语义约定**:
- 使用OpenTelemetry语义约定（Semantic Conventions）
- 遵循命名空间约定（如`celery.task.*`）
- 使用一致的键名

**示例**:
```python
# 好的属性命名
span.set_attribute("celery.task.name", task_name)
span.set_attribute("celery.task.retry.current", retries)

# 避免的属性命名
span.set_attribute("taskName", task_name)  # 不一致
span.set_attribute("retry", retries)  # 太模糊
```

### 事件vs属性

**何时使用事件**:
- 时间戳重要的事件
- 操作过程中的状态变化
- 错误和异常

**何时使用属性**:
- 元数据和标签
- 不会变化的值
- 用于过滤和查询的键

### Span层次结构

**嵌套spans**:
```python
# 父span
with tracer.start_as_current_span("celery.task.fetch_api") as parent_span:
    # 子span
    with tracer.start_as_current_span("http_request") as child_span:
        # HTTP请求代码
        pass
```

**链接重试尝试**:
- 每次重试创建新的span
- 使用相同的trace ID链接所有尝试
- 使用parent span ID表示层次关系

## 可视化Span数据

### Trace可视化工具

**Jaeger**:
- 开源分布式追踪平台
- 支持OpenTelemetry
- 提供trace瀑布流可视化

**Zipkin**:
- Twitter开发的分布式追踪系统
- 支持OpenTelemetry

**商业工具**:
- Datadog APM
- New Relic
- Honeycomb

### Span查询

**按属性过滤**:
```
celery.task.status = "failed_max_retries"
celery.task.name = "fetch_external_api"
```

**按时间范围查询**:
```
timestamp > now() - 1h
celery.task.is_retry = true
```

## 与Metrics的结合

**Spans + Metrics**:
- Spans提供详细的操作级追踪
- Metrics提供聚合的统计信息
- 结合使用获得全面的可观测性

**Celery重试指标示例**:
```python
task_retry_counter.add(1, {
    "task.name": task_name,
    "retry.attempt": retries
})
```

## 优势

### 标准化
- 跨语言互操作性
- 与可观测性后端兼容
- 社区支持和工具生态

### 详细性
- 捕获操作的完整生命周期
- 记录错误和异常
- 追踪因果关系

### 可查询性
- 基于属性的过滤
- 时间范围查询
- 模式识别

## 相关实体

- [[Celery]]
- [[OpenTelemetry]]

## 相关概念

- [[分布式追踪]]
- [[重试模式]]
- [[熔断器模式]]
- [[可观测性]]

## 参考资料

- OpenTelemetry Specification: https://opentelemetry.io/docs/reference/specification/
- OpenTelemetry Python: https://opentelemetry.io/docs/instrumentation/python/
- Celery Instrumentation: https://opentelemetry.io/docs/instrumentation/python/celery/

