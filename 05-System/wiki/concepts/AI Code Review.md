---
type: concept
name: "AI Code Review"
category: "AI/Software Development"
---

# AI Code Review

AI Code Review 是利用人工智能工具对代码进行自动化审查的过程，旨在发现潜在问题、优化代码质量并提高开发效率。

## 多 AI 协作的价值

在 [[Claude Pitfalls Database Indexes  Lincoln Loop]] 的案例中，展示了多 AI 协作的强大价值：

### 协作链路

```
OpenAI Codex → 发现问题
        ↓
Claude → 提供解决方案
        ↓
Gemini → 进一步优化
        ↓
Claude → 确认并整合
```

### 各 AI 的独特价值

| AI | 角色 | 贡献 |
|----|------|------|
| **Codex** | 代码审查者 | 发现并发索引创建的生产风险 |
| **Claude** | 解决方案提供者 | 提供并发索引创建的 Django 实现 |
| **Gemini** | 优化建议者 | 建议使用部分索引提升性能 |
| **Claude** | 整合者 | 确认优化方案并提供详细分析 |

## 关键洞察

### 1. 上下文至关重要

AI 需要完整的信息才能做出正确判断：

**缺失的上下文**：
- 索引是在**新添加的列**上创建
- 所有行的初始值都是 NULL

**结果**：AI 误判了问题的严重性

**教训**：向 AI 提供代码审查任务时，应该明确：
- 表的大小
- 列是新添加还是已存在
- 数据分布（NULL 比例）

### 2. AI 的优势

- **发现人类忽略的问题**：并发创建的风险被及时发现
- **提供正确的解决方案**：即使是误判，解决方案本身是正确的
- **持续优化**：Gemini 的部分索引建议进一步提升了性能

### 3. AI 的局限

- **需要完整上下文**：没有明确"新列"信息，导致误判
- **过度谨慎**：在没有完整信息时倾向于保守
- **缺乏实践经验**：不会像人类工程师那样考虑"实际运行情况"

## 最佳实践

### 为 AI 提供充分上下文

```markdown
# Code Review Prompt

## 代码背景
- 表名：images
- 表大小：3.1M 行
- 迁移目的：添加全文搜索功能
- 新列：search (tsvector, 初始值为 NULL)

## 问题
- 这是一个新添加的列
- 所有行的初始值都是 NULL
- 索引创建后，会通过管理命令填充数据

## 请审查
1. 生产风险
2. 性能影响
3. 改进建议
```

### 多 AI 协作流程

1. **第一轮**：让 AI A 审查代码
2. **第二轮**：将 A 的意见和代码一起发给 AI B
3. **第三轮**：综合 A 和 B 的意见，让 AI C 提供最终方案
4. **人类决策**：综合考虑所有建议，做出最终决策

## 工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| **GitHub Copilot** | 代码补全为主 | 开发阶段辅助 |
| **OpenAI Codex** | 代码理解能力强 | 代码审查、重构 |
| **Claude** | 上下文理解好 | 复杂逻辑分析 |
| **Gemini** | 多模态能力强 | 图表、文档分析 |

## 价值总结

> "The real result here, however, is not that Claude cannot be trusted to write code that it won't fail in a later code review, but that **using multiple agents gives much, much better results**, and is well worth your time and tokens to invest in."

多 AI 协作的价值：
1. **互补视角**：不同 AI 有不同的训练数据和分析方法
2. **相互验证**：减少单一 AI 的盲点和偏见
3. **持续优化**：每个 AI 都能在前一个的基础上改进

## 相关概念

- [[PostgreSQL]]
- [[GIN Index]]
- [[Database Migration]]

## 参考来源

- [[Claude Pitfalls Database Indexes  Lincoln Loop]]
