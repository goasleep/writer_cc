# Manus

**类型**: AI Agent产品/平台
**Category**: Agent Harness

## 概述

Manus是一个AI Agent平台。根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的引用，Manus在Harness演进方面提供了一个典型案例。

## 关键特点

### 快速迭代
**案例**: Manus在半年内重建了五次

**演进方向**: 每次重写都在做减法

这说明了Harness设计的一个重要原则：
> 一边补承重结构，一边等待模型进步后再把不再承重的部分删掉。

## 启示

### Harness厚度的平衡
**太薄**: 很多稳定性问题只能靠模型自觉
**太厚**: 系统笨重、昂贵，和当前模型强绑定

**Manus的做法**:
- 早期补结构
- 模型进步后删减dead weight
- 持续优化到最简有效形态

### 演进逻辑
模型和Harness是**协同演化**的：
1. 早期模型弱 → Harness补结构
2. 模型跨过门槛 → Harness删除冗余
3. 模型继续进步 → Harness继续精简

## 相关概念

- [[Harness Engineering]]
- [[Agent Runtime]]
- [[Agent]]

## 相关实体

- [[Claude Code]]
- [[OpenAI]]
