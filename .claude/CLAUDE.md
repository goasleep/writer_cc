# 个人写作库 - Claude Code 工作指令

> 本目录是一个 **Obsidian Vault**，同时也是一套由 Python 工具驱动的个人写作库系统。
> **重要原则：用户不直接使用任何 CLI 命令，所有工具操作都通过 Claude Code 完成。用户只在 Obsidian 中阅读和写作。**

---

## 核心原则

**用户入口只有 Claude Code 和 Obsidian。**

- `src/writer_tools/` 下的 Python 工具、CLI 命令（如 `uv run writer-collect`）**仅由 Claude Code 在用户指令下自动调用**，不对用户暴露。
- 用户的操作路径：
  1. **与 Claude Code 对话** → 完成采集、分析、仿写、整理
  2. **在 Obsidian 中** → 阅读、编辑、双向链接、写作创作
- 所有 bash 命令的运行都必须由 Claude Code 代理执行。

---

## 快速导航

| 命令 | 作用 | 触发方式 |
|------|------|----------|
| `/collect <url>` | 采集文章到 `raw/articles/` + 自动分析评分 + wiki ingest | 用户一句话指令 |
| `/batch <urls.txt>` | 批量采集文章 | 用户发送文件并请求处理 |
| `/query <问题>` | 搜索 wiki 并沉淀答案 | 用户提问 |
| `/lint` | 检查并修复 wiki 健康度 | 用户主动触发或建议 |
| `/imitate` | 启动参考文章仿写工作流 | 用户请求仿写某文章 |
| `/moc` | 查看或更新 MOC | 用户请求整理主题 |
| `/clean <file>` | 清理 Markdown 格式 | 用户请求整理某文章 |

---

## 系统架构

```
┌──────────────────────────────────────────────────────────────┐
│                        个人写作库系统                         │
├────────────────────┬───────────────────┬─────────────────────┤
│     文章收集        │     知识落库       │      仿写创作        │
├────────────────────┼───────────────────┼─────────────────────┤
│ 用户: "采集这篇文章" │ 用户: Obsidian    │ 用户: "仿写这篇文章"  │
│ ↓                  │ ↓                 │ ↓                   │
│ Claude Code        │ 阅读、链接、写作   │ Claude Code         │
│ ↓                  │                   │ ↓                   │
│ 自动调用 Python工具 │                   │ 三维分析 + 生成初稿 │
│ ↓                  │                   │ ↓                   │
│ 00-Inbox/          │ 03-Resources/     │ 01-Projects/        │
└────────────────────┴───────────────────┴─────────────────────┘
```

---

## Vault 目录约定

- `00-Inbox/` — 新采集的文章，待处理（已废弃，不再接收新文章）
- `01-Projects/` — 进行中的写作项目
- `02-Areas/` — 持续维护的知识领域
- `03-Resources/` — 参考文章、读书笔记、金句（LLM 禁止自动修改）
- `04-Archive/` — 已完成或暂停的项目
- `05-System/` — 模板、MOC、脚本、配置、wiki、analyses
- `99-Daily/` — 每日笔记

---

## 操作规范

### 采集文章时
1. 用户给出 URL 或发送 URL 列表文件
2. **Claude Code 自动调用** `uv run writer-collect collect <url>`
3. 结果保存到 `raw/articles/`，带标准 frontmatter
4. **AnalyzerAgent 子 agent** 自动生成 8 维度分析评分，保存到 `05-System/analyses/articles/`
5. LLM 自动更新 wiki：source summary → entities/concepts → index → log
6. 主 agent 更新 analyses 聚合索引（by-style / by-technique / by-article-type）

### 仿写工作流时
1. 用户请求仿写某篇文章
2. Claude Code 读取 `03-Resources/` 或 `raw/articles/` 中的参考文章
3. **优先读取** `05-System/analyses/articles/<参考文章>.md` 的三维分析结果
4. 使用 `docs/writing_imitation_workflow.md` 中的框架生成仿写初稿
5. 保存到 `01-Projects/<项目名>/`
6. 告知用户可在 Obsidian 中打开继续编辑

### 整理 Inbox 时
1. 用户说"整理收件箱"或类似请求
2. Claude Code 读取 `raw/articles/` 中的文件列表
3. 建议分类方案（移至 `03-Resources/`、创建链接、删除）
4. 在用户确认后执行移动/修改操作
5. 更新相关 MOC

### 清理文章时
1. 用户指向某篇文章请求清理格式
2. **Claude Code 自动调用** `uv run writer-collect clean <file>`
3. 或在必要时直接编辑文件
4. 向用户报告完成，不暴露底层命令

---

## 禁止行为

- **不要要求用户手动运行 `uv run ...` 或任何 CLI 命令**
- **不要把 Python 工具的 CLI help 信息直接复制给用户**
- **不要假设用户会打开终端**
- 所有可自动化的操作，都应由 Claude Code 代理执行

---

## 插件与配置

### 推荐 Obsidian 插件（必装）
- **Dataview** — 元数据查询、仪表盘
- **Templater** — 模板自动化
- **Tag Wrangler** — 标签管理
- **Periodic Notes** — 周期性笔记
- **Obsidian Git** — 版本控制（可选）

### 标签体系
- `type/article`, `type/book-note`, `type/idea`, `type/moc`
- `status/inbox`, `status/reading`, `status/processed`, `status/writing`, `status/published`
- `topic/technology`, `topic/product`, `topic/design`, `topic/growth`
- `area/programming`, `area/frontend`, `area/backend`, `area/writing`

---

## LLM Wiki 规则

自本方案实施起，Vault 引入 LLM Wiki 双层架构：

### 层级约定

- `raw/` — 精修后的原文层。由 LLM 写入，之后 immutable。包含 `raw/articles/`、`raw/papers/`、`raw/books/`、`raw/assets/`。
- `05-System/wiki/` — LLM 全权维护的知识网络层。用户阅读，不主动编辑（除非明确修正错误）。
- `05-System/analyses/` — LLM 维护的文章分析评分层。包含单篇文章分析、聚合索引、分析日志。
- `03-Resources/` — 人类手写笔记层。LLM **禁止自动修改**此目录中的内容。

### 核心规则

1. **Ingest 必须更新 wiki + analyses**
   每次 `/collect` 或 `/batch` 完成后，必须按顺序执行：
   - 将精修原文保存到 `raw/`（已由此前的 CLI 改动保证）
   - **启动 AnalyzerAgent 子 agent**，生成 `05-System/analyses/articles/<原文标题>.md`
   - 主 agent 更新 `05-System/analyses/indices/` 和 `analyses/log.md`
   - 撰写/更新 `wiki/sources/<原文标题>.md`
   - 提取实体和概念，新建或更新 `wiki/entities/` 和 `wiki/concepts/`
   - 更新 `wiki/index.md`
   - 追加 `wiki/log.md`

2. **Query 必须落库**
   用户提出的知识类问题（涉及比较、综合、分析），在合成答案后必须写入 `wiki/queries/YYYY-MM-DD-<slug>.md`。

3. **Lint 先报告后修改**
   运行 `/lint` 时，先生成 markdown 报告给用户确认，确认后方可批量修改 wiki。修改后追加 `wiki/log.md`。

4. **文件名使用原文标题**
   wiki 中 sources、entities、concepts 页面均使用原文标题/实体名/概念名作为文件名。analyses 中同样使用原文标题。

5. **追加 only**
   `wiki/log.md` 和 `analyses/log.md` 只能追加新条目，不能修改历史条目。

6. **00-Inbox 已废弃**
   原 `00-Inbox/` 目录不再接收新文章。旧内容由 LLM 一次性迁移后删除该目录。

### 新增命令

| 命令 | 作用 | 触发方式 |
|------|------|----------|
| `/query <问题>` | 搜索 wiki 并合成答案，写回 wiki/queries/ | 用户提问 |
| `/lint` | 对 wiki 进行健康检查，生成报告待确认后修复 | 用户主动触发或会话结束时建议 |

### 兼容调整

- `/collect <url>` 现在保存到 `raw/articles/`，并**自动触发 wiki ingest + AnalyzerAgent 分析全流程**
- `/batch <file>` 同上
- `/clean <file>` 现在清洗 `raw/` 中的文件
- `/imitate` 可同时读取 `raw/` 原文、`analyses/` 分析结果和 `wiki/sources/` 摘要
- `/moc` 可结合 `wiki/index.md`、`analyses/indices/` 和 `wiki/syntheses/` 给出建议

---

## Agent 架构说明

### AnalyzerAgent（子 agent）

**触发时机**：`/collect` 保存文章后自动触发。

**职责**：
- 读取 `raw/articles/<标题>.md` 和 `05-System/analyses/ANALYSIS_TEMPLATE.md`
- 输出 8 维度评分文件到 `05-System/analyses/articles/<标题>.md`
- 返回 JSON 摘要供主 agent 更新索引

**评分维度**：
- **五维内容质量**：`content_depth`, `readability`, `originality`, `ai_flavor`, `virality_potential`
- **三维写作技法**：`structure`, `style`, `technique`

### 主 agent（Orchestrator）

**职责**：
- 调用 Python pipeline 完成 fetch/extract
- 启动 AnalyzerAgent 子 agent
- 接收 JSON 摘要，更新 analyses/indices/
- 执行 wiki ingest
- 向用户汇报完整结果

---

## 命令详解（Claude Code 内部执行）

### `/collect <url>`
内部执行：
1. `uv run writer-collect collect <url>`
2. 在 `raw/articles/` 生成带 frontmatter 的 Markdown 文件
3. **启动 AnalyzerAgent 子 agent**：
   - 生成 `05-System/analyses/articles/<原文标题>.md`
   - 返回 JSON 摘要
4. 主 agent 更新 analyses 索引：
   - `indices/by-style.md`
   - `indices/by-technique.md`
   - `indices/by-article-type.md`
   - `analyses/log.md`
5. LLM 自动执行 wiki ingest：
   - 撰写 `wiki/sources/<原文标题>.md`
   - 更新 `wiki/entities/` 和 `wiki/concepts/`
   - 更新 `wiki/index.md`
   - 追加 `wiki/log.md`
6. 向用户返回：标题、保存路径、8 维评分摘要、quality_tier、新建/更新的 wiki 和分析页面列表

### `/batch <file>`
内部执行：
1. `uv run writer-collect batch <file>`
2. 所有文章保存到 `raw/articles/`
3. 生成并读取 `collection_report.json` 向用户汇报
4. 对每篇成功采集的文章，依次执行 AnalyzerAgent 分析 + wiki ingest（批量可请求用户确认是否全部分析）

### `/inbox`
工作流：
1. `uv run writer-collect inbox` 或直接读取 `raw/articles/` 目录
2. 列出 raw 中的所有文章
3. 主动询问用户是否需要整理或触发 wiki 更新

### `/imitate`
工作流：
1. 确认参考文章路径（`03-Resources/` 或 `raw/articles/`）
2. **读取 `05-System/analyses/articles/<参考文章>.md` 的三维分析结果**
3. 提取可仿写元素
4. 用户指定新主题后生成仿写初稿
5. 保存到 `01-Projects/`

### `/moc`
1. 列出 `05-System/MOCs/` 中的所有主题地图
2. 检查对应主题下是否有新文章/分析未被收录
3. 建议更新内容，在用户确认后执行

### `/clean <file>`
内部执行 `uv run writer-collect clean <file>`，标准化 Markdown 格式。

---

## 文档索引

| 文档 | 路径 | 内容 |
|------|------|------|
| Vault 设置指南 | `docs/vault_setup.md` | Obsidian 目录结构、标签、插件 |
| 仿写工作流 | `docs/writing_imitation_workflow.md` | 三维分析框架、完整流程 |
| Prompt 速查 | `docs/imitation_prompt_cheatsheet.md` | 11 个 Prompt 模板 |
| 分析评分模板 | `05-System/analyses/ANALYSIS_TEMPLATE.md` | 8 维度分析输出模板 |
| Collect Skill | `.claude/skills/collect-article/SKILL.md` | collect-article skill 定义 |
| 工具开发说明 | `README-for-tools.md` | Python 包架构、UV 使用 |

---

## Git 工作流

日常整理后，Claude Code 应主动建议用户提交：

```bash
git add raw/ 05-System/ 03-Resources/
git commit -m "collect: articles + analyses + update MOCs"
git push
```

建议：每次会话结束或 Inbox 清理后提交一次。
