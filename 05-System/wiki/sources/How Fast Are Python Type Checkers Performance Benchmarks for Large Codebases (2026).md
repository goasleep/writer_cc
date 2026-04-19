# How Fast Are Python Type Checkers? Performance Benchmarks for Large Codebases (2026)

**Source URL**: https://docs.bswen.com/blog/2026-03-17-python-type-checker-performance-benchmarks/
**Source**: bswen.dev
**Author**: bswen
**Date**: March 17, 2026
**Language**: 英文

## 核心论点

作者面临CI管道中12分钟的类型检查瓶颈，开始探索更快的Python类型检查器替代方案。发现只有ty（Astral）提供了可验证的基准测试数据，而其他工具大多只有营销声明而无具体数字。通过实际测试发现：mypy daemon提供10x加速，pyright提供4x加速，ty提供27-50x加速但覆盖率较低。

## 作者观点

### 问题陈述

**CI性能危机**:
> 我的CI管道每次类型检查需要12分钟。每个PR、每次push。每周50个PR意味着每周消耗1200分钟CI时间，每年$624成本

**真正的成本是开发者时间**：
> 等待12分钟vs 1分钟获得反馈会改变开发者的工作方式

### 工具声称vs现实

**性能声称摘要**（2026年3月）:
| Checker | 声称 | 架构 | 证据 |
|---------|------|------|------|
| ty (Astral) | 10x-100x faster | Rust, incremental | 已发布图表 |
| mypy daemon | 10x+ faster than mypy | Python daemon | 官方文档 |
| pyrefly | "Lightning-fast" | Rust, incremental | 仅为营销 |
| zuban | Performance-focused | Rust | 无数据 |
| pyright | "High performance" | TypeScript/Node | 为此设计 |
| pyre | "Millions of lines" | OCaml | 仅为营销 |

**问题**:
> 只有ty提供了已发布的基准测试数据。其他所有工具都在没有可比较数字的情况下做出声明

### 唯一的真实基准测试

**Ty的主张**（来自Astral自己的基准图表）:
- 在home-assistant代码库上的结果
- mypy: 45.2s（基线1x）
- pyright: 12.8s（3.5x faster）
- ty: 0.9s（50x faster）

**警告**:
> 这来自Astral自己的基准图表。实际结果可能显著不同

## 实际测试结果

### 测试环境

**代码库规模**:
- 100,000行代码
- 作者的实际项目代码库

### 标准Mypy（基线）
```
$ time mypy src/ --ignore-missing-imports
real 8m43.127s
user 8m41.892s
sys 0m1.235s
# 8分43秒类型检查
```

### Mypy Daemon（增量模式）
**首次检查（冷缓存）**:
```
$ dmypy start -- --ignore-missing-imports
$ time dmypy check --ignore-missing-imports src/
real 8m41.892s
```

**第二次检查（热缓存，增量）**:
```
$ time dmypy check --ignore-missing-imports src/
real 0m52.314s
# 哇 - 增量运行10x更快
```

**工作原理**:
> daemon在后台保持mypy运行并缓存类型信息。后续运行只分析更改的文件

### Pyright
```
$ npm install -g pyright
$ time pyright src/
real 2m18.453s
user 2m16.892s
sys 0m1.561s
# 比标准mypy快约4x
# 但仍然比mypy daemon的增量模式慢
```

**特点**:
- 对于每次运行从头开始的CI管道很重要
- 在VS Code中通过Pylance使用

### Ty
```
$ pip install ty
$ time ty check src/
real 0m23.127s
user 0m22.892s
sys 0m0.235s
# 我见过的最快：23秒
# 但ty仍处于早期，可能遗漏一些错误
```

**问题**:
> ty是最快的，但我注意到它标记的错误比mypy少。早期阶段工具，覆盖率不完整

## CI/CD成本分析

### 优化前
- 类型检查时间：12分钟/PR
- PRs/周：100
- 总CI分钟：1,200分钟/周
- 成本：$12/周 = **$624/年**

### Mypy Daemon后（增量）
- 类型检查时间：1.2分钟（估计）
- 总CI分钟：120分钟/周
- 节省：**$562/年**

### 切换到Ty（如果可行）
- 类型检查时间：0.5分钟（估计）
- 总CI分钟：50分钟/周
- 节省：**$614/年**

### 真正的节省
> 真正的节省是开发者时间。等待12分钟vs 1分钟获得反馈会改变开发者的工作方式

## LSP响应时间

**测试条件**: 500行文件，光标位于类型密集部分

| Checker | 首次Hover | 编辑到诊断 |
|---------|-----------|-----------|
| pyright | 0.3s | 0.5s |
| mypy | 2.1s | 3.8s |
| ty | 0.1s | 0.2s |

**说明**:
- pyright是VS Code通过Pylance使用的工具
- mypy的LSP明显比pyright慢
- LSP体验对日常开发很重要

## 误报比较

**同一代码库上的误报率**:

| Checker | 报告错误 | 实际错误 | 误报 |
|---------|---------|---------|------|
| mypy | 231 | 89 | 142 |
| pyright | 94 | 89 | 5 |
| ty | 67 | 89 | 3（但25个漏报） |
| zuban | 89 | 89 | 0 |

**结论**:
> 最快的检查器（ty）规范符合度较低。速度不是一切

## 基准测试脚本

**简单Python脚本**:
```python
#!/usr/bin/env python3
"""Compare type checker performance on your codebase."""
import subprocess
import time
from pathlib import Path

CHECKERS = [
    ("mypy (standard)", ["mypy", "src/", "--ignore-missing-imports"]),
    ("pyright", ["pyright", "src/"]),
    ("ty", ["ty", "check", "src/"]),
]

def benchmark(name: str, cmd: list[str]) -> float:
    """Run a checker and return elapsed time in seconds."""
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.1f}s (exit code: {result.returncode})")
    return elapsed
```

**作者代码库上的结果**:
```
=== Type Checker Benchmark ===
mypy (standard): 523.1s (exit code: 1)
pyright: 138.4s (exit code: 1)
ty: 19.2s (exit code: 1)
=== Summary ===
ty: 19.2s (27.2x vs mypy)
pyright: 138.4s (3.8x vs mypy)
mypy (standard): 523.1s (1.0x vs mypy)
```

## 缺失的数据

### Pyrefly（Meta的基于Rust的检查器）
```
$ pip install pyrefly
ERROR: Could not find a version that satisfies requirement pyrefly
# Pyrefly仍处于封闭测试或有限发布阶段
```

### Zuban
```
$ pip install zuban
# 已安装，但类型检查给出与mypy不同的错误
# 当错误检测不同时难以公平比较
```

**观察**:
> 这些工具显示出前景，但缺乏可访问的基准测试或稳定版本

## 作者的选择

### 选项1: Mypy + Daemon（已选择）
- 无迁移成本 - 只需启用daemon
- 10x加速足够显著
- 我习惯的相同错误检测
- 与现有mypy配置一起工作

### 选项2: Pyright（新项目考虑）
- 更好的准确度
- 原生VS Code支持
- 4x加速

### 选项3: Ty（最大速度）
- 仍处于早期阶段
- 覆盖率较低
- 需要验证结果与mypy匹配

### 选项4: 等待pyrefly/zuban成熟
- 都是基于Rust，有前景
- 但目前缺乏可访问性

## GitHub Actions配置

**优化后的CI管道**:
```yaml
name: Type Check
on: [push, pull_request]
jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      # Cache mypy for 10x speedup on subsequent runs
      - name: Cache mypy
        uses: actions/cache@v4
        with:
          path: .mypy_cache
          key: mypy-${{ hashFiles('**/*.py') }}
          restore-keys: |
            mypy-
      - name: Install dependencies
        run: pip install mypy
      - name: Run mypy daemon
        run: |
          dmypy start -- --ignore-missing-imports
          dmypy check --ignore-missing-imports src/
          dmypy stop
```

## 本地开发工作流

**Shell别名**（添加到.bashrc或.zshrc）:
```bash
alias mypy-start='dmypy start -- --ignore-missing-imports'
alias mypy-check='dmypy check --ignore-missing-imports .'
alias mypy-stop='dmypy stop'
alias mypy-restart='dmypy restart -- --ignore-missing-imports'
```

**用法**:
```bash
$ mypy-start  # 启动daemon一次
$ mypy-check  # 快速增量检查
$ mypy-check  # 后续运行更快
$ mypy-stop   # 完成时停止
```

## 关键洞察

### 基准测试缺失
> 跨类型检查器缺乏标准化基准测试是一个真正的差距。每个项目测量方式不同，如果有的话。我最终在自己的代码库上进行基准测试以获得真实数字

### 速度vs准确度
**最快并不意味着最好**:
- ty: 27-50x更快，但规范符合度较低
- pyright: 4x更快，更好的准确度
- mypy daemon: 10x更快，零迁移成本，相同准确度

### LSP重要性
> CLI性能是一回事。IDE性能是另一回事

pyright与VS Code的集成使其成为许多开发者的默认选择。

## 最终建议

**立即收益**: 启用mypy daemon（10x+加速，零成本）

**新项目**: 考虑pyright（更好的准确度 + VS Code支持）

**持续关注**: ty、pyrefly、zuban随时间成熟

**关键要点**:
- 缺乏标准化基准测试
- 只有ty提供已发布的性能数据
- Mypy daemon提供立即10x加速
- 速度不是一切 - 准确度很重要

## 相关实体

- [[Astral]]（ty和ruff的创建者）
- [[mypy]]
- [[pyright]]
- [[ty]]
- [[pyrefly]]（Meta）
- [[zuban]]
- [[pyre]]（Facebook/Meta）

## 相关概念

- [[Python类型检查]]
- [[CI/CD优化]]
- [[LSP（Language Server Protocol）]]
- [[增量类型检查]]
- [[Daemon模式]]

## 参考资料

- Ty Repository: https://github.com/astral-sh/ty
- Mypy Daemon Documentation: https://mypy.readthedocs.io/en/stable/mypy_daemon.html
- Pyrefly Repository: https://github.com/facebook/pyrefly
- Pyright Repository: https://github.com/microsoft/pyright
- Reddit讨论: https://www.reddit.com/r/Python/comments/1bswen/python_type_checkers_comparison/

