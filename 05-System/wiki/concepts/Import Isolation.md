---
type: concept
name: "Import Isolation"
category: "Python/性能优化"
---

# Import Isolation

Import Isolation 是一种 Python 性能优化技术，通过将重量级导入隔离到独立子进程中，减少主进程的内存占用。

## 问题背景

### Import Chains 的内存成本

在 Python 中，一个简单的 `import` 语句会加载：
- 模块代码本身
- 模块的静态数据和单例
- 所有传递依赖

**实际内存成本**：
- `import boto3`：25 MB
- `import matplotlib`：17 MB
- `import pandas`：44 MB

### 隐形依赖链

```python
# app.py
from training.utils import some_helper

# utils.py
from training.models import User

# models.py
from training.database import MongoDB

# database.py
import boto3  # ← 25 MB，但 app.py 并不需要！
```

## 解决方案：子进程隔离

### 实现思路

```python
# 主进程：轻量级
import subprocess

def run_search_indexing():
    subprocess.run(["python", "search_indexer.py"])

# search_indexer.py：重量级
import boto3
import pandas
# ... 只在需要时运行
```

### 效果

在 [[Michael Kennedy]] 的实践中：

| 场景 | 内存使用 |
|------|----------|
| 单体进程 | 708 MB |
| 子进程隔离 | 22 MB |
| **优化比** | **32 倍** |

## 适用场景

✅ **适合**
- 定时任务（如每小时运行的索引更新）
- 偶尔需要的功能（如生成月度报告）
- 独立的功能模块

❌ **不适合**
- 频繁调用的功能（子进程启动开销）
- 需要共享内存状态的任务
- 实时性要求高的场景

## 相关概念

- [[Local Imports]]
- [[Memory Optimization]]
- [[PEP 8]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
