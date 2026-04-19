# Claude Code

**Type**: Harness / Agent开发工具
**开发者**: Anthropic
**Category**: Agent基础设施

## 概述

Claude Code是Anthropic官方推出的Agent开发工具，属于**Harness层**产品。它是"驾驭执行"的那一层，负责把模型套起来、驾驭它去完成具体任务。

## 核心能力

根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析：

1. **加载Skills**: 组织和管理Agent技能
2. **组织context**: 管理对话上下文和提示词
3. **调用工具**: 协调工具使用
4. **处理循环**: 管理Agent的执行循环

## 在三分天下架构中的位置

```
MODEL_URL=https://api.anthropic.com/v1  (模型层)
       ↓
Claude Code  (Harness层)
       ↓
DB_URL=postgres://user:pass@host:5432/memory  (记忆层)
```

**定位**: Harness层 - 驾驭执行层

**职责**: 在模型和数据库之间协调，完成具体任务的执行

## Skills机制

Claude Code的**Skills机制**已经证明了一个关键趋势：

- 用户写个`memory-skill.md`，描述清楚"记忆怎么存、怎么查"
- Claude在需要时自动调用
- **不需要任何外部Memory框架**

这意味着Memory框架的"认知架构"工作，现在可以由**一个markdown文件 + 模型自己写SQL**完成。

## 在AI辅助写作中的应用

根据[我怎么用 AI 辅助写作](../sources/我怎么用 AI 辅助写作.md)的实践：

**用于第二、三、四步**：
- **第二步（和AI讨论）**: 讨论感触和观点，获取新名词、新想法，刺激灵感
- **第三步（提炼观点）**: 基于讨论结果再思考，提炼自己的观点
- **第四步（梳理结构）**: 一起列出全部信息和观点，探讨合适的组合方式

## 市场地位

- 目前跑在最前面的Harness产品
- 通过开源掀翻了壁垒，拉平到水平线
- 与Cursor、Devin、OpenClaw、Hermes等竞争

## 相关链接

- 竞品: Cursor, Devin, OpenClaw, Hermes
- 层级: 三分天下架构中的Harness层
- 机制: Skills系统
