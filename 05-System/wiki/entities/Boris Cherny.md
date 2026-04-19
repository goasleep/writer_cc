# Boris Cherny

**角色**: Claude Code创始人
**领域**: AI Agent、工程工具
**所属公司**: Anthropic

## 概述

Boris Cherny是Claude Code的创始人。根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的引用，他在验证反馈方面提出了重要观点。

## 核心观点

### 外部验证的价值
> 给模型一种能验证自己工作的方式，质量提升2到3倍。

这个观点强调了：
- **工具给了模型行动能力**
- **验证才给了模型纠错能力**

### 验证方法

外部反馈回路包括：
- 测试
- lint
- 类型检查
- 页面截图
- 端到端操作
- 专门的评估器

### 为什么需要外部验证

**问题**: 让生成器自己验自己，速度很快，但最容易放过自己

**解决**: 只要任务碰到代码、页面、部署、数据写入这些"能真测"的地方，外部验证几乎都是值得补上的

## 影响

Boris Cherny的洞察推动了Claude Code和类似产品对验证机制的重视，这也是生产级Agent与Demo级Agent的重要分水岭。

## 相关概念

- [[Harness Engineering]]
- [[验证反馈]]
- [[Claude Code]]

## 相关实体

- [[Claude Code]]
- [[Anthropic]]
