# LLM Wiki 融合设计文档

> 将现有 PARA 写作库系统与 Karpathy 的 LLM Wiki 模式相融合的设计方案。
> 日期：2026-04-07

---

## 一、设计目标

在保留现有 PARA 写作库优势（仿写工作流、Obsidian 集成、自动化采集）的基础上，引入 LLM Wiki 的核心能力：

1. **持续复利积累**：每采集一篇文章，LLM 自动更新实体页、概念页、交叉引用
2. **查询即沉淀**：用户提问的答案写回 wiki，探索本身产生积累
3. **自动化维护**：通过 lint 定期检查 wiki 健康度
4. **原文与知识分离**：`raw/` 存放immutable精修原文，`wiki/` 存放 LLM 维护的派生知识网络

---

## 二、目录结构

```
/home/smith/Project/writer_cc/
├── 01-Projects/                 # 进行中的写作项目
├── 02-Areas/                    # 持续维护的知识领域
├── 03-Resources/                # 手写笔记、读书心得、金句（人类创作层）
├── 04-Archive/                  # 已完成或暂停的项目
├── 05-System/
│   ├── MOCs/                    # 主题地图
│   ├── Templates/               # 模板
│   ├── Scripts/                 # 脚本
│   └── wiki/                    # LLM 全权维护的知识网络
│       ├── index.md             # wiki 总目录（内容导向）
│       ├── log.md               # 操作日志（时间导向，追加 only）
│       ├── sources/             # 每篇 raw 文章的 LLM 摘要
│       ├── entities/            # 实体页（人、公司、产品、技术等）
│       ├── concepts/            # 概念页（框架、理论、模式等）
│       ├── syntheses/           # 综合页（跨 source 的主题综述）
│       └── queries/             # 查询产物（用户提问后写回的答案）
├── 99-Daily/                    # 每日笔记
└── raw/                         # 精修后的原文（immutable，LLM 只读）
    ├── articles/                # 网页文章
    ├── papers/                  # 论文、报告
    ├── books/                   # 书籍章节/摘录
    └── assets/                  # 图片等附件
```

### 层级约定

| 层级 | 路径 | 负责人 | 说明 |
|------|------|--------|------|
| 原文层 | `raw/` | LLM 写入，人类审阅后不再修改 | 精修后的原文，immutable |
| wiki 层 | `05-System/wiki/` | LLM 全权维护 | 用户阅读，不主动编辑 |
| 人类笔记层 | `03-Resources/` | 用户手动维护 | 读书心得、金句、手写笔记 |
| 创作层 | `01-Projects/` | 用户 + LLM 协作 | 仿写初稿、进行中项目 |

### 废弃目录

- `00-Inbox/` 不再使用。现有内容将进行一次性迁移分析，决定入 `raw/` 或 `03-Resources/` 后删除该目录。

---

## 三、wiki 页面规范

### 3.1 文件名格式

- 统一使用**原文标题**作为文件名，如 `LLM Wiki.md`、`深度工作.md`
- 允许中文标题直接作为文件名

### 3.2 Source Summary 模板

路径：`wiki/sources/<原文标题>.md`

```markdown
---
type: source
source_raw: raw/articles/<原文标题>.md
date_collected: 2026-04-07
entities: [实体A, 实体B]
concepts: [概念X, 概念Y]
---

# <原文标题>

## 核心论点
...

## 关键证据
- ...

## 我的启发
...
```

### 3.3 Entity Page 模板

路径：`wiki/entities/<实体名>.md`

```markdown
---
type: entity
aliases: []
related_entities: []
related_concepts: []
sources: [source-title-1, source-title-2]
---

# <实体名>

## 定义/简介
...

## 相关论述
- 在 [[source title]] 中提到...

## 更新记录
- 2026-04-07: 由 LLM 从 [[source title]] 中提取创建
```

### 3.4 Concept Page 模板

路径：`wiki/concepts/<概念名>.md`

```markdown
---
type: concept
aliases: []
related_entities: []
related_concepts: []
sources: []
---

# <概念名>

## 定义
...

## 在不同来源中的论述
- [[source title]]: ...

## 更新记录
- 2026-04-07: 由 LLM 从 [[source title]] 中提取创建
```

### 3.5 Query Output 模板

路径：`wiki/queries/YYYY-MM-DD-<slug>.md`

```markdown
---
type: query
date_queried: 2026-04-07
question: "用户提出的问题原文"
sources: [source-1, source-2]
entities: []
concepts: []
---

# Query: <问题摘要>

## 答案
...

## 引用来源
- [[source title]]: ...
```

### 3.6 Index.md 规范

`wiki/index.md` 为内容导向的总目录，按类别组织：

```markdown
---
type: index
last_updated: 2026-04-07
---

# Wiki Index

## Sources
- [[source title]] — 一句话摘要

## Entities
- [[entity name]] — 一句话摘要

## Concepts
- [[concept name]] — 一句话摘要

## Syntheses
- [[synthesis title]] — 一句话摘要

## Queries
- [[query title]] — 一句话摘要
```

### 3.7 Log.md 规范

`wiki/log.md` 为追加 only 的时序日志，条目格式必须一致以便解析：

```markdown
## [2026-04-07] ingest | <原文标题>
- 新增 source: [[<原文标题>]]
- 更新 entities: [[实体A]], [[实体B]]
- 更新 concepts: [[概念X]]

## [2026-04-07] query | <问题摘要>
- 新增 query: [[<query标题>]]

## [2026-04-07] lint | 自动维护
- 修复孤儿页: [[page name]]
- 新增缺失链接: 3 处
```

---

## 四、命令体系与工作流

### 4.1 `/collect <url>`

**流程（全自动）：**

1. 下载原文
2. **智能清洗**：LLM 规范格式、提取目录结构、标注重点段落、生成标准 frontmatter
3. 保存精修版到 `raw/articles/<原文标题>.md`
4. LLM 阅读精修版，撰写 `wiki/sources/<原文标题>.md`
5. 提取文中所有实体和概念，为每个新建或更新 `wiki/entities/` 和 `wiki/concepts/` 页面
6. 更新 `wiki/index.md`
7. 追加 `wiki/log.md`
8. 向用户汇报：保存路径、核心论点、新建/更新的 wiki 页面列表

### 4.2 `/batch <file>`

与 `/collect` 逻辑相同，批量处理 URL 列表文件。
采集完成后统一汇报：成功数、失败数、新增的 sources/entities/concepts 统计。

### 4.3 `/query <问题>`

**流程：**

1. LLM 读取 `wiki/index.md` 定位相关页面
2. 读取具体 wiki 页面（sources/entities/concepts/syntheses）
3. **必要时回查** `raw/` 原文和 `03-Resources/` 手写笔记
4. 合成带引用的答案
5. **写入** `wiki/queries/YYYY-MM-DD-<slug>.md`
6. 在对话中返回摘要和文件链接

**例外**：纯临时性问题（如"帮我翻译这句话"）可由 LLM 自行判断不写文件；涉及知识合成、比较、分析的查询必须落库。

### 4.4 `/lint`

**流程：**

1. LLM 对 wiki 进行全面健康检查，覆盖：
   - **矛盾检查**：不同页面间是否存在矛盾论述
   - **过时检查**：新 source 是否使旧页面的某些声明失效
   - **孤儿页**：是否存在无 inbound links 的页面
   - **缺失链接**：文中提及但未创建页面的实体/概念
   - **数据缺口**：是否有重要问题 wiki 尚未回答
2. 生成 markdown 格式的 lint 报告（不直接修改）
3. 将报告呈现给用户，等待确认
4. 用户确认后，批量执行修改
5. 追加 `wiki/log.md`

**触发方式**：
- 用户主动输入 `/lint`
- 每次会话结束或 Inbox 清理后，Claude 主动建议运行 lint

### 4.5 `/imitate`

**兼容调整：**

1. 确认参考文章路径（优先从 `raw/` 中检索）
2. **同时读取** `wiki/sources/` 中的摘要，快速定位仿写重点
3. 执行三维分析（结构、风格、技巧）
4. 提取可仿写元素
5. 生成仿写初稿，保存到 `01-Projects/<项目名>/`

### 4.6 `/moc`

**兼容调整：**

1. 列出 `05-System/MOCs/` 中的所有主题地图
2. 检查对应主题下是否有新文章/实体/概念未被收录
3. **结合 `wiki/index.md` 和 `wiki/syntheses/`** 给出更智能的更新建议
4. 在用户确认后执行更新

### 4.7 `/clean <file>`

**兼容调整：**

清洗对象改为 `raw/` 中的文件。执行智能清洗：标准化 frontmatter、修复格式、提取目录、标注重点。

---

## 五、数据迁移

### 5.1 `00-Inbox/` 迁移

现有 `00-Inbox/` 中的文章将一次性处理：

1. LLM 逐篇分析 Inbox 内容
2. 判断去向：
   - **高质量参考原文** → 迁移到 `raw/articles/`，触发 wiki ingest
   - **个人笔记/摘抄/金句** → 迁移到 `03-Resources/`
   - **过时/重复/无用** → 删除或移至 `04-Archive/`
3. 迁移完成后删除空 `00-Inbox/` 目录
4. 在 `wiki/log.md` 中记录本次迁移

---

## 六、CLAUDE.md 新增 schema 摘要

以下规则将被追加到 `.claude/CLAUDE.md`：

1. **层级分离**：`raw/` 为 immutable 原文层，`05-System/wiki/` 为 LLM 维护层
2. **Ingest 必须更新 wiki**：每次 `/collect` 或 `/batch` 完成后，必须执行 wiki 更新（sources → entities/concepts → index → log）
3. **Query 必须落库**：知识类查询的答案必须写入 `wiki/queries/`
4. **Lint 先报告后修改**：`/lint` 生成报告后必须等待用户确认才能批量修改 wiki
5. **文件名使用原文标题**：wiki 中所有页面均以原文标题命名
6. **追加 only**：`wiki/log.md` 只能追加，不能修改历史条目
7. **禁止覆盖 03-Resources**：LLM 不得自动修改 `03-Resources/` 中的人类手写笔记

---

## 七、实施 checklist

- [ ] 创建 `raw/` 子目录
- [ ] 创建 `05-System/wiki/` 及子目录
- [ ] 更新 `.claude/CLAUDE.md`
- [ ] 迁移现有 `00-Inbox/` 内容
- [ ] 将现有 `00-Inbox/` 中的高价值文章导入 wiki 并删除该目录
- [ ] 初始化 `wiki/index.md` 和 `wiki/log.md`
- [ ] 测试 `/collect` 全流程
- [ ] 测试 `/query` 全流程
- [ ] 测试 `/lint` 全流程
