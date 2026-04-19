# 三分天下：为什么Agent Memory框架是死路

**Source URL**: https://mp.weixin.qq.com/s/bWpka2OzrJFyrbmrecIQUw
**Author**: 老冯
**Collected**: 2026-04-19
**Language**: 中文

## 核心论点

Agent Memory框架赛道在两年后可能消失，不是因为Agent不需要记忆，而是因为不需要今天这种独立的"Memory框架"。终局是**三分天下**架构：模型层提供智力，Harness层负责驾驭执行，数据库层管理记忆，三方彻底解耦。

## 关键论据

### 1. 终局架构：三分天下
```
MODEL_URL=https://api.anthropic.com/v1
DB_URL=postgres://user:pass@host:5432/memory
```
- 模型厂商：提供智力
- Harness（Claude Code/Cursor/Devin）：驾驭执行、加载Skills、组织context
- 数据库厂商：管理记忆

### 2. 真正的壁垒：私有数据
- 算力会摊平，模型会平权
- 企业不会允许核心数据被单一服务商锁定
- 三方制衡是必然结果

### 3. Memory框架的四种类型及命运
1. **数据库套壳SDK**（Mem0/LangMem）：会被Skill + 模型直接写SQL替代
2. **知识图谱构建器**（Graphiti/Cognee）：策略层被模型吸收，存储层归回数据库
3. **Agent Runtime**（Letta/MemGPT）：应归入Harness赛道，不是Memory赛道
4. **其他**: 大多数是"替Agent建表和写SQL"，无技术壁垒

### 4. The Bitter Lesson
- 手工编码的"认知策略"长期必输给通用方法
- Memory框架硬编码的决策（信息价值、分层、检索策略）会被模型自己写SQL替代

### 5. 数据库的确定性
- 数据库不在AI冲击范围内（物理世界持久化，非信息加工）
- PostgreSQL将成为通用Agent记忆层的终局：
  - 线缆协议是事实标准
  - 扩展生态覆盖所有检索原语
  - 模型天然会说SQL

## 核心金句

> "Agent需要记忆，但不需要今天这种被称作'Memory框架'的东西。"

> "你以为的护城河，其实是一张写着几百字的markdown。"

> "数据库不在AI冲击的范围内。"

> "十年后再回望2026年这场Memory框架喧哗，会看到一件很平淡的事——那些号称'给Agent设计认知'的框架，最后真正留下来的代码，是它们最朴素的那一部分：把数据老老实实塞进PostgreSQL的那几行SQL。"

## 相关实体

- **Memory框架**: Mem0, MemGPT/Letta, Zep, Cognee, Hindsight, MemoryScope, Memobase, SuperMemory, Graphiti, LangMem, EverMemOS
- **Harness产品**: Claude Code, Cursor, Devin, OpenClaw, Hermes
- **数据库**: PostgreSQL, SQLite, Pigsty
- **模型厂商**: Anthropic, OpenAI

## 相关概念

- [[Agent Memory框架]]
- [[三分天下架构]]
- [[The Bitter Lesson]]
- [[Agent Runtime]]
- [[线缆协议]]

## 参考价值

- **技术趋势判断**: 架构演化规律、赛道生死判断
- **创业投资**: 哪些方向有壁垒，哪些是过渡态
- **写作技法**: 结构化论证、分类拆解、历史类比
