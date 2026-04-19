# Akshay

**Type**: 技术作者/研究者
**领域**: Agent Harness研究

## 概述

Akshay是《The Anatomy of an Agent Harness》一文的作者。根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的引用，Akshay最有启发的地方在于把视角从"模型有多强"挪到了"模型外面那套系统到底在干什么"。

## 核心贡献

### The Anatomy of an Agent Harness
这篇文章对Agent Harness领域有重要影响：

1. **视角转换**: 从关注模型能力转向关注工程系统
2. **系统解剖**: 详细拆解了Harness的六个承重层
3. **实证案例**: 引用TerminalBench 2.0数据证明Harness重要性
   - LangChain只换外围基础设施
   - 从前30名外拉到第5名

## 关键观点

### Harness vs 模型
> 同一个模型、同一组权重，只换外面的系统层，表现就可能大幅跳跃。

### 研究方向
有研究项目把"优化Harness"本身变成搜索对象，最终拿到了76.4%的通过率。

### 关于工具系统
- Claude Code把工具分成六类
- OpenAI Agents SDK支持函数工具、托管工具和MCP工具
- 分类方法不同，但要解决的问题一样

### 关于工具数量
> 当工具数超过10个且职责重叠时，模型的调用质量会明显下降。

## 相关链接

- 文章: The Anatomy of an Agent Harness
- 相关概念: [[Harness Engineering]], [[Agent Runtime]]

## 相关实体

- [[Claude Code]]
- [[OpenAI]]
- [[LangChain]]
