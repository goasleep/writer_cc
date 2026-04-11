---
type: concept
name: "Local Imports"
category: "Python/性能优化"
---

# Local Imports

Local Imports（局部导入）是一种将 `import` 语句放在函数内部而非模块顶部的优化技巧，用于延迟加载重量级库，减少内存占用。

## 传统做法 vs 局部导入

### PEP 8 标准（模块级导入）

```python
# 模块顶部
import boto3
import matplotlib
import pandas

def generate_report():
    # 使用这些库
    pass
```

**问题**：
- 模块加载时立即导入所有依赖
- 即使函数未被调用，内存也已占用

### 局部导入（优化）

```python
# 模块顶部：只导入轻量级依赖
import os

def generate_report():
    # 函数内部：按需导入重量级库
    import matplotlib
    import pandas
    # 使用这些库
    pass
```

**优势**：
- 只在函数被调用时才导入
- 如果函数永不调用，内存完全不占用

## 内存成本实例

| 库 | 导入成本 | 使用频率 |
|----|---------|----------|
| boto3 | 25 MB | 偶尔（文件上传） |
| matplotlib | 17 MB | 罕见（生成图表） |
| pandas | 44 MB | 罕见（数据分析） |

**总计**：如果这三项功能每月只运行一次，采用局部导入可节省 86 MB 内存。

## 实战案例

在 [[Michael Kennedy]] 的实践中，将偶尔使用的库（如 boto3、matplotlib、pandas）改为局部导入，配合 worker 进程的 TTL（Time-To-Live）策略，显著降低了内存占用。

### Worker TTL 策略

```python
# Granian 配置
# 每 6 小时重启一次 worker
# 释放局部导入累积的内存
granian --worker-ttl 21600 app:app
```

## 权衡考虑

### 优点

✅ **内存节省**：延迟加载节省初始内存
✅ **更快的启动时间**：模块加载更快
✅ **条件导入**：可根据运行时条件选择不同库

### 缺点

❌ **违反 PEP 8**：Python 官方代码风格指南
❌ **首次调用延迟**：第一次调用时有导入开销
❌ **代码可读性**：依赖关系不够直观

## 未来：PEP 810 (Lazy Imports)

Python 3.15 将引入 **PEP 810**（Explicit Lazy Imports），原生支持延迟导入：

```python
from __future__ import lazy_imports

import boto3  # 自动延迟导入
import matplotlib  # 自动延迟导入
```

**预期收益**：
- 符合 PEP 8 规范
- 自动优化内存占用
- 无需手动管理导入位置

## 适用场景

✅ **强烈推荐**
- 偶尔使用的功能（报告生成、批处理）
- Worker 进程可定期重启的环境
- 内存极度受限的场景

✅ **可以考虑**
- 中等使用频率的功能（每日、每周）
- 有明显冷热路径的代码

❌ **不推荐**
- 热路径函数（每次请求都会调用）
- 微秒级延迟敏感的场景
- 团队不熟悉此技巧的代码库

## 相关概念

- [[Import Isolation]]
- [[Memory Optimization]]
- [[PEP 8]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
- PEP 810: https://peps.python.org/pep-0810/
