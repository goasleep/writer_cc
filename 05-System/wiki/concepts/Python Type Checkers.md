# Python Type Checkers

**类型**: 开发工具
**用途**: 静态类型检查（Static Type Checking）
**语言**: Python

## 简介

Python类型检查器是用于在运行时之前检测类型错误的工具。它们分析代码中的类型标注（type annotations）并识别潜在的类型不匹配、缺失标注和类型相关错误。2026年的主要类型检查器包括mypy、pyright、ty、pyrefly和zuban，性能差异显著（从10x到50x加速）。

## 主要类型检查器

### mypy

**类型**: Python实现、daemon模式
**性能**: 基线（1x），daemon模式10x加速
**特点**:
- 最成熟和广泛使用的类型检查器
- Python编写，易于扩展
- daemon模式提供增量检查
- 大型社区和生态系统

**性能数据**:
- 标准模式: 8m43s（100,000行代码库）
- daemon模式（增量）: 52s（**10x加速**）
- daemon模式（首次）: 8m42s

**优势**:
- 零迁移成本（已有项目）
- daemon模式立即10x加速
- 相同的错误检测体验
- 与现有配置兼容

**劣势**:
- 标准模式较慢
- LSP响应较慢（2.1s hover, 3.8s诊断）

### pyright

**类型**: TypeScript/Node实现
**性能**: 比标准mypy快4x
**特点**:
- 微软开发
- VS Code通过Pylance集成
- 更好的规范符合度
- 原生LSP支持

**性能数据**:
- 总时间: 2m18s（**3.8x加速**）
- LSP hover: 0.3s
- LSP诊断: 0.5s

**优势**:
- 更好的准确度（94错误，5误报）
- VS Code深度集成
- 优秀的LSP性能
- 适合新项目

**劣势**:
- 需要Node.js运行时
- 不如mypy daemon的增量性能

### ty

**类型**: Rust实现、Astral开发
**性能**: 比mypy快27-50x
**特点**:
- 极快的类型检查
- 仍处于早期开发阶段
- 增量类型检查
- 与ruff生态集成

**性能数据**:
- 作者代码库: 19.2s（**27.2x加速**）
- Astral基准（home-assistant）: 0.9s（**50x加速**）
- LSP hover: 0.1s
- LSP诊断: 0.2s

**优势**:
- 最快的类型检查器
- 优秀的LSP性能
- Rust的内存安全
- Astral生态系统

**劣势**:
- 早期阶段，覆盖率较低
- 67错误报告（25个漏报）
- 规范符合度较低
- 不适合生产环境（截至2026年）

### pyrefly

**类型**: Rust实现、Meta开发
**性能**: 声称"Lightning-fast"
**状态**: 封闭测试或有限发布

**特点**:
- Facebook/Meta支持
- Rust实现（性能潜力）
- 增量类型检查

**可用性**:
```
$ pip install pyrefly
ERROR: Could not find a version that satisfies requirement pyrefly
```

**潜在**:
- Meta的支持意味着持续开发
- Rust性能优势
- 可能与PyTorch生态集成

### zuban

**类型**: Rust实现
**性能**: Performance-focused
**状态**: 已发布但缺乏基准测试

**特点**:
- Rust实现
- 性能导向设计
- 无公开基准测试数据

**问题**:
- 错误检测与mypy不同
- 难以公平比较
- 缺乏可访问的基准测试

## 性能比较

### CLI性能（100,000行代码库）

| Checker | 时间 | 相对加速 | 基准 |
|---------|------|---------|------|
| mypy (standard) | 523.1s | 1.0x | 基线 |
| pyright | 138.4s | 3.8x | ✅ |
| ty | 19.2s | 27.2x | ✅✅ |
| mypy daemon | 52.3s | 10.0x | ✅ |

### LSP性能（500行文件）

| Checker | 首次Hover | 编辑到诊断 | 评分 |
|---------|-----------|-----------|------|
| ty | 0.1s | 0.2s | ✅✅ |
| pyright | 0.3s | 0.5s | ✅ |
| mypy | 2.1s | 3.8s | ❌ |

### 准确度比较

| Checker | 报告错误 | 实际错误 | 误报 | 漏报 |
|---------|---------|---------|------|------|
| mypy | 231 | 89 | 142 | 0 |
| pyright | 94 | 89 | 5 | 0 |
| ty | 67 | 89 | 3 | 25 ❌ |
| zuban | 89 | 89 | 0 | 0 |

**结论**:
> 最快的检查器（ty）规范符合度较低。速度不是一切

## CI/CD影响

### 成本分析

**优化前**（mypy standard）:
- 类型检查时间: 12分钟/PR
- PRs/周: 100
- 总CI分钟: 1,200分钟/周
- 成本: **$624/年**

**mypy daemon后**:
- 类型检查时间: 1.2分钟
- 总CI分钟: 120分钟/周
- 节省: **$562/年**

**ty（如果可行）**:
- 类型检查时间: 0.5分钟
- 总CI分钟: 50分钟/周
- 节省: **$614/年**

### 真正的成本
> 真正的节省是开发者时间。等待12分钟vs 1分钟获得反馈会改变开发者的工作方式

## 选择建议

### 现有项目
**选择**: mypy + daemon

**理由**:
- 无迁移成本
- 10x加速显著
- 相同错误检测
- 与现有配置兼容

**实施**:
```bash
# 启动daemon
dmypy start -- --ignore-missing-imports

# 增量检查
dmypy check --ignore-missing-imports src/
```

### 新项目
**选择**: pyright

**理由**:
- 更好的准确度
- 原生VS Code支持
- 优秀的LSP性能
- 4x加速足够

**未来考虑**: ty成熟后迁移

### 早期采用者
**选择**: ty

**前提**:
- 验证结果与mypy匹配
- 接受较低覆盖率
- 愿意提交bug报告
- 关注Rust生态系统

## 基准测试缺失

### 问题
> 跨类型检查器缺乏标准化基准测试是一个真正的差距。每个项目测量方式不同，如果有的话

### 现状
- **ty**: 唯一提供已发布基准测试的工具
- **pyrefly**: 营销声明"Lightning-fast"，无数据
- **zuban**: "Performance-focused"，无数据
- **pyre**: "Millions of lines"，营销声明

### 自定义基准测试
```python
#!/usr/bin/env python3
"""比较代码库上类型检查器的性能。"""
import subprocess
import time

CHECKERS = [
    ("mypy (standard)", ["mypy", "src/", "--ignore-missing-imports"]),
    ("pyright", ["pyright", "src/"]),
    ("ty", ["ty", "check", "src/"]),
]

def benchmark(name: str, cmd: list[str]) -> float:
    """运行检查器并返回经过时间（秒）。"""
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.1f}s (exit code: {result.returncode})")
    return elapsed
```

## 未来趋势

### Rust实现
- ty、pyrefly、zuban都用Rust编写
- 性能优势显著（10-50x）
- 内存安全保证
- 编译到WebAssembly的潜力

### LSP集成
- 所有检查器都在改进LSP支持
- IDE性能成为差异化因素
- 实时类型检查成为标准

### AI辅助
- LLM驱动的类型标注生成
- 智能类型推断
- 自动错误修复

## 相关实体

- [[Astral]]（ty开发者）
- [[Microsoft]]（pyright开发者）
- [[Meta]]（pyrefly开发者）
- [[mypy]]
- [[pyright]]
- [[ty]]

## 相关概念

- [[静态类型检查]]
- [[类型标注]]
- [[LSP（Language Server Protocol）]]
- [[CI/CD优化]]

## 参考资料

- Ty Repository: https://github.com/astral-sh/ty
- Mypy Daemon: https://mypy.readthedocs.io/en/stable/mypy_daemon.html
- Pyrefly: https://github.com/facebook/pyrefly
- Pyright: https://github.com/microsoft/pyright
- 类型检查器比较: https://www.reddit.com/r/Python/comments/1bswen/python_type_checkers_comparison/

