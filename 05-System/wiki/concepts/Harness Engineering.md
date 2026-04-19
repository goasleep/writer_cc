---
type: concept
aliases: []
related: []
---

# Harness Engineering

**定义**: 驾驭和执行AI模型的技术工程领域
**定位**: 三分天下架构中的中间层

AI Agent 系统工程中的一个核心概念，指围绕模型构建的运行时系统（Agent Runtime System）的设计与实现。其目标不是提升模型推理能力，而是保证 Agent 在复杂、长流程任务中的稳定运行。典型 Harness 包含 Environment、Tool、Control、Memory、Evaluation 五个模块。

## 核心定义

根据[Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的分析：

> Harness是在模型和真实交付之间，补上一套可运行、可恢复、可验证、可治理的软件系统。

**工程问题**: 怎样把一个无状态、会推理的模型，变成一个能持续交付结果的系统。

## 在三分天下架构中的定位

根据[三分天下：为什么Agent Memory框架是死路](../sources/三分天下：为什么Agent Memory框架是死路.md)的分析，Harness是"三分天下"架构中的中间层：

```
MODEL_URL=https://api.anthropic.com/v1
       ↓
Harness (Claude Code/Cursor/Devin/OpenClaw/Hermes)
       ↓
DB_URL=postgres://user:pass@host:5432/memory
```

**上层**: 模型层（智力）
**本层**: **Harness层（驾驭执行）**
**下层**: 数据库层（记忆）

## 核心职责

### 1. 加载Skills
- 管理和组织Agent的技能库
- 动态加载和卸载技能
- 技能的版本控制和更新

### 2. 组织context
- 管理对话上下文
- 优化提示词
- 管理token预算
- Prompt cache优化

### 3. 调用工具
- 协调工具的使用
- 管理工具权限和安全
- 处理工具调用结果

### 4. 处理循环
- 管理Agent的执行循环
- 控制流和状态机
- 错误处理和重试

## 代表产品

### Claude Code
- 目前跑在最前面
- Anthropic官方出品
- 通过开源掀翻了壁垒

### Cursor
- AI驱动的代码编辑器
- 集成AI编程能力

### Devin
- AI软件工程师
- 自主完成编程任务

### OpenClaw
- 本地部署的个人AI助理
- 强调用户控制权

### Hermes Agent
- 开源自学习型AI助理
- 强调AI自学习能力

### Letta/MemGPT
- Agent Runtime/Agent OS
- 如果真能做成Agent Runtime方向会很有意思

## 市场状态

### 为什么现在被重视（2026）

**两个信号**:

1. **同一模型，不同Harness表现大不同**
   - LangChain只换外围基础设施，TerminalBench 2.0从前30名外拉到第5
   - 研究项目优化Harness本身，拿到76.4%通过率

2. **长任务误差快速累积**
   - 10步流程，每步99%成功率，全链路约90%
   - 任务越长，误差堆积越明显

**演进时间线**:
- 2024: 卷Prompt
- 2025: 补Context
- 2026: 讨论收到Harness

**核心原因**: 
> 模型智力在线之后，大家开始重新面对软件工程。只不过这次面对的，是一个会推理、会调用工具、还会不断消耗上下文预算的新型系统。

### 当前阶段（2026年）
- 这块还在摸索和成形
- 刚长出些壁垒又被Claude Code开源掀翻
- 局势仍在剧烈变动中

### 未来展望
- 这块有壁垒，但还在成形
- 竞争格局尚未稳定
- 可能会出现更多创新

## Harness六大承重层

根据[Agent Harness 综述](../sources/Agent Harness 综述：同一个模型，为什么做出来的 Agent 差这么远.md)的分析，成熟的Harness包含六个关键层：

### 1. 循环控制（Loop Control）
**表面**: while loop - 组装输入，调用模型，解析输出，执行工具

**难点**:
- 每一步由谁控制
- 何时终止
- 出错后怎么回来

**常见问题**: 无限转圈、提前收尾、误把中间结果当最终结果

### 2. 工具系统（Tool System）
需要管理四件事：
1. 工具如何注册
2. 参数如何校验
3. 执行环境是否隔离
4. 结果如何回写成模型能理解的Observation

**分类对照**:
- Claude Code: 文件操作、搜索、执行、Web访问、代码智能、子Agent派生（六类）
- OpenAI Agents SDK: 函数工具、托管工具、MCP工具

### 3. 记忆管理（Memory Management）
**该记什么、什么时候记、什么时候删**

**Claude Code三层做法**:
1. 始终加载的轻量索引（每条约150字符）
2. 按需拉取的详细主题文件
3. 只通过搜索访问的原始会话记录

**核心原则**: 
> 成熟系统不会把记忆当真相，而是把它当线索。先靠记忆提示方向，再回到真实文件、真实环境和真实状态里确认。

### 4. 状态管理（State Management）
系统需要知道：
- 当前做到哪一步
- 失败后从哪恢复
- 哪些中间产物值得保留
- 哪些只是临时噪音

### 5. 权限控制（Permission Control）
**关键拆分**:
- **模型负责**: 提出动作
- **工具系统负责**: 决定动作能不能做、要不要用户确认、失败后如何处理

### 6. 验证反馈（Validation & Feedback）
**外部反馈回路**: 测试、lint、类型检查、页面截图、端到端操作、专门的评估器

**Boris Cherny观点**: 给模型一种能验证自己工作的方式，质量提升2到3倍。

## 与Memory框架的区别

### Memory框架
- 试图在模型、Harness、数据库之间插入一层
- 替Agent做认知决策（信息价值、分层、检索）
- 无技术壁垒，会被模型自己写SQL替代

### Harness
- 终局架构的稳定一层
- 提供执行引擎和工具编排
- 有真正的工程价值

## 完整Harness组成

### 不只是Runtime
**误区**: 很多人以为Harness只是Runtime

**真相**: Harness真正吃力的地方，往往是那些把团队经验外移成工件的层。

**核心问题**: 尽量缩小"必须靠模型临场发挥"的面积。

### 三层工件

1. **AGENTS.md**: 仓库地图/默认答案
2. **Spec**: 任务契约/本轮任务的上下文管理层
3. **Skills**: 程序性记忆/团队沉淀下来的可复用方法

**合起来做同一件事**: 把团队经验外移成工件，让模型不必临场发挥。

## 为什么叫"Harness"

"Harness"这个词很形象：

- **马具/挽具**: 套在马身上，用来驾驭马匹
- **Harness层**: 套在模型外面，用来驾驭模型完成具体任务

模型提供"智力"，但需要Harness来"驾驭"它才能完成工作。

## 相关概念

- [[三分天下架构]]
- [[Agent Runtime]]
- [[Agent Memory框架]]

## 相关实体

- [[Claude Code]]
- [[OpenClaw]]
- [[Hermes Agent]]
- [[Letta (MemGPT)]]
