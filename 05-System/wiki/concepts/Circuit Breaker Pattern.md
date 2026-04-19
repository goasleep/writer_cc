# Circuit Breaker Pattern

**类型**: 设计模式
**分类**: 弹性模式（Resilience Pattern）
**应用**: 分布式系统、微服务架构

## 简介

熔断器模式（Circuit Breaker Pattern）是一种用于防止级联故障的设计模式。当检测到外部服务持续失败时，熔断器"打开"（open），快速失败而不允许请求继续流向失败的服务。经过一段时间后，熔断器进入"半开"（half-open）状态，允许有限请求通过以测试服务是否恢复。如果请求成功，熔断器"关闭"（closed）；如果失败，重新打开。

在Celery任务重试监控中，熔断器模式可以防止在注定失败的重试尝试上浪费资源。

## 核心概念

### 三种状态

#### Closed（关闭）
**正常状态**:
- 请求正常流向服务
- 失败计数增加
- 当失败达到阈值时，熔断器打开

**特点**:
- 系统正常运行
- 失败被记录但不阻止请求

#### Open（打开）
**故障状态**:
- 所有请求立即失败
- 不调用实际服务
- 防止资源浪费

**特点**:
- 快速失败（fail fast）
- 保护系统资源
- 经过超时时间后进入半开状态

#### Half-Open（半开）
**测试状态**:
- 允许有限请求通过
- 测试服务是否恢复
- 根据结果决定关闭或重新打开

**特点**:
- 谨慎恢复
- 单个成功关闭熔断器
- 单个失败重新打开熔断器

### 关键参数

**failure_threshold**: 失败阈值
- 触发熔断器打开的失败次数
- 典型值：5次

**timeout**: 超时时间
- 熔断器保持打开的时间（秒）
- 典型值：60秒

**success_threshold**: 成功阈值
- 半开状态下关闭熔断器所需的成功次数
- 典型值：1次

## Python实现

### 基础熔断器

```python
import time
from collections import defaultdict
from threading import Lock

class CircuitBreaker:
    """
    Celery任务的熔断器。
    跟踪失败率并在超过阈值时打开熔断器。
    """
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = defaultdict(int)
        self.last_failure_time = defaultdict(float)
        self.circuit_open = defaultdict(bool)
        self.lock = Lock()

    def is_open(self, task_name: str) -> bool:
        """检查任务的熔断器是否打开。"""
        with self.lock:
            if not self.circuit_open[task_name]:
                return False
            # 检查超时是否已过
            if time.time() - self.last_failure_time[task_name] > self.timeout:
                # 重置熔断器
                self.circuit_open[task_name] = False
                self.failures[task_name] = 0
                return False
            return True

    def record_failure(self, task_name: str):
        """记录任务失败。"""
        with self.lock:
            self.failures[task_name] += 1
            self.last_failure_time[task_name] = time.time()
            if self.failures[task_name] >= self.failure_threshold:
                self.circuit_open[task_name] = True

    def record_success(self, task_name: str):
        """记录任务成功。"""
        with self.lock:
            if self.circuit_open[task_name]:
                # 半开状态：成功关闭熔断器
                self.circuit_open[task_name] = False
                self.failures[task_name] = 0
```

### Celery任务集成

```python
# 全局熔断器
circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

class CircuitBreakerTask(MetricsTrackedTask):
    """带熔断器模式的任务。"""
    def __call__(self, *args, **kwargs):
        """执行带熔断器检查的任务。"""
        with tracer.start_as_current_span("circuit_breaker_check") as span:
            span.set_attribute("task.name", self.name)
            # 检查熔断器是否打开
            if circuit_breaker.is_open(self.name):
                span.set_attribute("circuit_breaker.state", "open")
                span.add_event("circuit_breaker_open", {
                    "failures": circuit_breaker.failures[self.name]
                })
                logger.warning(f"Circuit breaker open for {self.name}, failing fast")
                raise Exception("Circuit breaker is open")
            span.set_attribute("circuit_breaker.state", "closed")

        try:
            result = super().__call__(*args, **kwargs)
            # 记录成功
            circuit_breaker.record_success(self.name)
            return result
        except Exception as exc:
            # 记录失败
            circuit_breaker.record_failure(self.name)
            with tracer.start_as_current_span("circuit_breaker_failure") as span:
                span.set_attribute("task.name", self.name)
                span.set_attribute("circuit_breaker.failures",
                                   circuit_breaker.failures[self.name])
                if circuit_breaker.is_open(self.name):
                    span.add_event("circuit_breaker_opened")
                    logger.error(f"Circuit breaker opened for {self.name}")
                raise

@app.task(
    base=CircuitBreakerTask,
    bind=True,
    autoretry_for=(Exception,),
    max_retries=3
)
def protected_task(self, resource_id: str):
    """受熔断器保护的任务。"""
    with tracer.start_as_current_span("protected_operation") as span:
        span.set_attribute("resource.id", resource_id)
        # 调用可能宕机的外部服务
        result = call_unreliable_service(resource_id)
        return result
```

## 优势

### 资源保护
> 当任务持续失败时，熔断器可以防止在注定失败的重试尝试上浪费资源

**避免**:
- 无数重试消耗CPU和网络带宽
- 数据库连接池耗尽
- 队列积压

### 快速失败
- 立即返回错误而不是等待超时
- 更好的用户体验
- 更快的错误恢复

### 系统稳定性
- 防止级联故障
- 保护下游服务
- 保持系统可用性

## 最佳实践

### 阈值配置

**failure_threshold**:
- 根据服务可靠性调整
- 可靠服务：高阈值（10+）
- 不可靠服务：低阈值（3-5）

**timeout**:
- 根据服务恢复时间调整
- 快速恢复：短超时（30秒）
- 慢速恢复：长超时（2-5分钟）

### 监控和告警

**追踪熔断器事件**:
```python
span.add_event("circuit_breaker_opened", {
    "task.name": task_name,
    "failures": failure_count
})
```

**指标监控**:
- 熔断器打开次数
- 熔断器打开持续时间
- 受保护的请求数量

### 组合模式

**熔断器 + 重试**:
- 熔断器防止级联故障
- 重试处理瞬态故障
- 两者结合提供全面保护

**熔断器 + 超时**:
- 熔断器防止重复失败
- 超时防止单个请求挂起
- 双重保护机制

## 与重试的关系

### 重试模式
- 处理**瞬态故障**（transient failures）
- 假设最终会成功
- 适用于偶发性问题

### 熔断器模式
- 处理**持续故障**（persistent failures）
- 假设短期内不会恢复
- 适用于系统级问题

### 组合使用
**Celery任务的最佳实践**:
1. 首先检查熔断器状态
2. 如果关闭，允许执行
3. 如果失败，触发重试
4. 如果达到失败阈值，打开熔断器
5. 快速失败而不重试

## 常见实现

### 库和框架

**Python**:
- `circuitbreaker`：独立的熔断器库
- `pybreaker`：Python熔断器实现
- 自定义实现（如上面的示例）

**其他语言**:
- Java: Resilience4j, Hystrix（已停止维护）
- Go: gobreaker, hystrix-go
- JavaScript: opencircuitry

## 相关概念

- [[重试模式]]
- [[超时模式]]
- [[舱壁隔离模式（Bulkhead Pattern）]]
- [[弹性模式]]

## 参考资料

- Circuit Breaker Pattern: https://martinfowler.com/bliki/CircuitBreaker.html
- Microsoft Cloud Design Patterns: https://docs.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
- Celery最佳实践: https://docs.celeryproject.org/en/stable/userguide/tasks.html

