# LLM Wiki 融合实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 PARA 写作库系统与 LLM Wiki 模式融合，建立 `raw/` 原文层和 `05-System/wiki/` 知识网络层，更新 CLAUDE.md schema，迁移现有数据。

**Architecture:** 保留现有 Python 采集工具，改造输出路径；新增 LLM 驱动的 wiki 维护工作流（Ingest/Query/Lint）；通过更新 `.claude/CLAUDE.md` 约束 LLM 行为。

**Tech Stack:** Python (writer_tools), Markdown, Obsidian, Claude Code

---

## 文件变更总览

| 文件 | 职责 | 操作 |
|------|------|------|
| `raw/articles/` | 精修原文存储目录 | 新建 |
| `raw/papers/` | 论文报告存储目录 | 新建 |
| `raw/books/` | 书籍摘录存储目录 | 新建 |
| `raw/assets/` | 图片附件存储目录 | 新建 |
| `05-System/wiki/` | wiki 根目录 | 新建 |
| `05-System/wiki/sources/` | source summaries | 新建 |
| `05-System/wiki/entities/` | 实体页 | 新建 |
| `05-System/wiki/concepts/` | 概念页 | 新建 |
| `05-System/wiki/syntheses/` | 综合页 | 新建 |
| `05-System/wiki/queries/` | 查询产物 | 新建 |
| `05-System/wiki/index.md` | wiki 总目录 | 新建 |
| `05-System/wiki/log.md` | 操作日志 | 新建 |
| `.claude/CLAUDE.md` | LLM 工作指令 | 修改 |
| `src/writer_tools/cli.py` | CLI 入口，修改输出目录 | 修改 |
| `src/writer_tools/claude_collector.py` | 采集器，修改 frontmatter | 修改 |
| `00-Inbox/` | 废弃目录 | 删除（迁移后） |

---

## Task 1: 创建目录结构

**Files:**
- Create: `raw/articles/`
- Create: `raw/papers/`
- Create: `raw/books/`
- Create: `raw/assets/`
- Create: `05-System/wiki/sources/`
- Create: `05-System/wiki/entities/`
- Create: `05-System/wiki/concepts/`
- Create: `05-System/wiki/syntheses/`
- Create: `05-System/wiki/queries/`

- [ ] **Step 1: 创建所有目录**

```bash
mkdir -p raw/{articles,papers,books,assets}
mkdir -p 05-System/wiki/{sources,entities,concepts,syntheses,queries}
```

- [ ] **Step 2: 验证目录创建成功**

```bash
ls -d raw/articles raw/papers raw/books raw/assets 05-System/wiki/sources 05-System/wiki/entities 05-System/wiki/concepts 05-System/wiki/syntheses 05-System/wiki/queries
```

Expected: 所有目录均列出，无 "No such file or directory" 错误。

- [ ] **Step 3: Commit**

```bash
git add raw/ 05-System/wiki/
git commit -m "chore: create raw and wiki directory structure"
```

---

## Task 2: 初始化 wiki 核心文件

**Files:**
- Create: `05-System/wiki/index.md`
- Create: `05-System/wiki/log.md`

- [ ] **Step 1: 编写 index.md**

```markdown
---
type: index
last_updated: 2026-04-07
---

# Wiki Index

## Sources

## Entities

## Concepts

## Syntheses

## Queries
```

Write to: `05-System/wiki/index.md`

- [ ] **Step 2: 编写 log.md**

```markdown
---
type: log
---

# Wiki Log
```

Write to: `05-System/wiki/log.md`

- [ ] **Step 3: Commit**

```bash
git add 05-System/wiki/index.md 05-System/wiki/log.md
git commit -m "chore: initialize wiki index and log"
```

---

## Task 3: 更新 CLI 输出目录

**Files:**
- Modify: `src/writer_tools/cli.py`

当前 CLI 将采集结果输出到 `00-Inbox/`，需要改为输出到 `raw/articles/`。

- [ ] **Step 1: 修改 CLI 中的目录常量**

将 `src/writer_tools/cli.py` 中的：

```python
VAULT_ROOT = Path(__file__).parent.parent.parent
INBOX_DIR = VAULT_ROOT / "00-Inbox"
RESOURCES_DIR = VAULT_ROOT / "03-Resources" / "文章收藏"
```

替换为：

```python
VAULT_ROOT = Path(__file__).parent.parent.parent
RAW_DIR = VAULT_ROOT / "raw" / "articles"
WIKI_DIR = VAULT_ROOT / "05-System" / "wiki"
RESOURCES_DIR = VAULT_ROOT / "03-Resources" / "文章收藏"
```

- [ ] **Step 2: 更新 cmd_collect 使用 RAW_DIR**

将 `cmd_collect` 中的：

```python
collector = ClaudeArticleCollector(output_dir=str(INBOX_DIR))
```

替换为：

```python
collector = ClaudeArticleCollector(output_dir=str(RAW_DIR))
```

- [ ] **Step 3: 更新 cmd_batch 使用 RAW_DIR**

将 `cmd_batch` 中的：

```python
batch = BatchCollector(
    output_dir=str(INBOX_DIR),
    max_workers=args.workers,
)
```

以及：

```python
batch.save_report(str(INBOX_DIR / "collection_report.json"))
```

分别替换为：

```python
batch = BatchCollector(
    output_dir=str(RAW_DIR),
    max_workers=args.workers,
)
```

以及：

```python
batch.save_report(str(RAW_DIR / "collection_report.json"))
```

- [ ] **Step 4: 更新 cmd_inbox 使用 RAW_DIR**

将 `cmd_inbox` 中的：

```python
if not INBOX_DIR.exists():
    print("Inbox 目录不存在")
    return

files = [f for f in INBOX_DIR.iterdir() if f.suffix == ".md"]
print(f"📥 Inbox 状态: {len(files)} 篇文章待处理")
```

替换为：

```python
if not RAW_DIR.exists():
    print("Raw 目录不存在")
    return

files = [f for f in RAW_DIR.iterdir() if f.suffix == ".md"]
print(f"📥 Raw 状态: {len(files)} 篇精修文章")
```

以及输出前缀从 `"  - "` 保持不变，文案从 `"... 还有 {len(files) - 10} 篇"` 改为 `"... 还有 {len(files) - 10} 篇"`（最小改动）。

- [ ] **Step 5: 验证 CLI 无语法错误**

Run:

```bash
cd /home/smith/Project/writer_cc && python -m py_compile src/writer_tools/cli.py
```

Expected: 无输出（表示编译通过）。

- [ ] **Step 6: Commit**

```bash
git add src/writer_tools/cli.py
git commit -m "feat: redirect CLI output from 00-Inbox to raw/articles"
```

---

## Task 4: 更新采集器 frontmatter

**Files:**
- Modify: `src/writer_tools/claude_collector.py`

当前 frontmatter 使用 `collected_at`，需要更明确的标注，并为 LLM 智能清洗预留接口。

- [ ] **Step 1: 增强 frontmatter 字段**

修改 `_build_frontmatter` 方法，在 `meta` 初始化时增加 `type` 和 `status`：

```python
meta = {
    'type': 'source',
    'source_url': url,
    'collected_at': datetime.now().isoformat(),
    'status': 'raw',
}
```

- [ ] **Step 2: 验证修改后的编译**

Run:

```bash
cd /home/smith/Project/writer_cc && python -m py_compile src/writer_tools/claude_collector.py
```

Expected: 无输出。

- [ ] **Step 3: Commit**

```bash
git add src/writer_tools/claude_collector.py
git commit -m "feat: add type and status to collected article frontmatter"
```

---

## Task 5: 更新 CLAUDE.md 的 schema 规则

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: 在命令详解之前插入 "LLM Wiki 规则" 章节**

在 `.claude/CLAUDE.md` 的 "## 命令详解" 之前，插入以下内容：

```markdown
---

## LLM Wiki 规则

自本方案实施起，Vault 引入 LLM Wiki 双层架构：

### 层级约定

- `raw/` — 精修后的原文层。由 LLM 写入，之后 immutable。包含 `raw/articles/`、`raw/papers/`、`raw/books/`、`raw/assets/`。
- `05-System/wiki/` — LLM 全权维护的知识网络层。用户阅读，不主动编辑（除非明确修正错误）。
- `03-Resources/` — 人类手写笔记层。LLM **禁止自动修改**此目录中的内容。

### 核心规则

1. **Ingest 必须更新 wiki**
   每次 `/collect` 或 `/batch` 完成后，必须按顺序执行：
   - 将精修原文保存到 `raw/`（已由此前的 CLI 改动保证）
   - 撰写/更新 `wiki/sources/<原文标题>.md`
   - 提取实体和概念，新建或更新 `wiki/entities/` 和 `wiki/concepts/` 页面
   - 更新 `wiki/index.md`
   - 追加 `wiki/log.md`

2. **Query 必须落库**
   用户提出的知识类问题（涉及比较、综合、分析），在合成答案后必须写入 `wiki/queries/YYYY-MM-DD-<slug>.md`。

3. **Lint 先报告后修改**
   运行 `/lint` 时，先生成markdown报告给用户确认，确认后方可批量修改 wiki。修改后追加 `wiki/log.md`。

4. **文件名使用原文标题**
   wiki 中 sources、entities、concepts 页面均使用原文标题/实体名/概念名作为文件名。

5. **追加 only**
   `wiki/log.md` 只能追加新条目，不能修改历史条目。

6. **00-Inbox 已废弃**
   原 `00-Inbox/` 目录不再接收新文章。旧内容由 LLM 一次性迁移后删除该目录。

### 新增命令

| 命令 | 作用 | 触发方式 |
|------|------|----------|
| `/query <问题>` | 搜索 wiki 并合成答案，写回 wiki/queries/ | 用户提问 |
| `/lint` | 对 wiki 进行健康检查，生成报告待确认后修复 | 用户主动触发或会话结束时建议 |

### 兼容调整

- `/collect <url>` 现在保存到 `raw/articles/`，并**自动触发 wiki ingest 全流程**
- `/batch <file>` 同上
- `/clean <file>` 现在清洗 `raw/` 中的文件
- `/imitate` 可同时读取 `raw/` 原文和 `wiki/sources/` 摘要
- `/moc` 可结合 `wiki/index.md` 和 `wiki/syntheses/` 给出建议

---
```

- [ ] **Step 2: 更新快速导航表格**

将 "## 快速导航" 中的表格增加 `/query` 和 `/lint`：

```markdown
| 命令 | 作用 | 触发方式 |
|------|------|----------|
| `/collect <url>` | 采集文章到 `raw/articles/` | 用户一句话指令 |
| `/batch <urls.txt>` | 批量采集文章 | 用户发送文件并请求处理 |
| `/query <问题>` | 搜索 wiki 并沉淀答案 | 用户提问 |
| `/lint` | 检查并修复 wiki 健康度 | 用户主动触发或建议 |
| `/imitate` | 启动参考文章仿写工作流 | 用户请求仿写某文章 |
| `/moc` | 查看或更新 MOC | 用户请求整理主题 |
| `/clean <file>` | 清理 Markdown 格式 | 用户请求整理某文章 |
```

- [ ] **Step 3: 更新操作规范中的采集说明**

将 "### 采集文章时" 中的步骤 2 和 3 改为：

```markdown
2. **Claude Code 自动调用** `uv run writer-collect collect <url>`
3. 结果保存到 `raw/articles/`，带标准 frontmatter
4. LLM 自动更新 wiki：source summary → entities/concepts → index → log
```

- [ ] **Step 4: 更新命令详解中的 /collect**

将 "### `/collect <url>`" 中的步骤改为：

```markdown
1. `uv run writer-collect collect <url>`
2. 在 `raw/articles/` 生成带 frontmatter 的 Markdown 文件
3. LLM 自动执行 wiki ingest：
   - 撰写 `wiki/sources/<原文标题>.md`
   - 更新 `wiki/entities/` 和 `wiki/concepts/`
   - 更新 `wiki/index.md`
   - 追加 `wiki/log.md`
4. 向用户返回：标题、保存路径、核心论点、新建/更新的 wiki 页面列表
```

- [ ] **Step 5: 更新命令详解中的 /batch**

将保存路径从 `00-Inbox/` 改为 `raw/articles/`。

- [ ] **Step 6: 更新命令详解中的 /inbox**

`/inbox` 命令已从查看 Inbox 状态改为查看 raw 状态。将整节替换为：

```markdown
### `/inbox`
工作流：
1. `uv run writer-collect inbox` 或直接读取 `raw/articles/` 目录
2. 列出 raw 中的所有文章
3. 主动询问用户是否需要整理或触发 wiki 更新
```

- [ ] **Step 7: 更新 Git 工作流中的路径**

将 Git 工作流中的：

```bash
git add 00-Inbox/ 03-Resources/ 05-System/
```

替换为：

```bash
git add raw/ 03-Resources/ 05-System/
```

- [ ] **Step 8: Commit CLAUDE.md 更新**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: add LLM Wiki schema rules to CLAUDE.md"
```

---

## Task 6: 迁移现有 00-Inbox/ 内容

**Files:**
- Delete: `00-Inbox/` (迁移后)

- [ ] **Step 1: 检查 00-Inbox 内容**

Run:

```bash
ls -la /home/smith/Project/writer_cc/00-Inbox/
```

当前 00-Inbox 为空（根据项目状态检查）。

- [ ] **Step 2: 若为空，直接删除目录**

```bash
rmdir /home/smith/Project/writer_cc/00-Inbox/
```

- [ ] **Step 3: 在 wiki/log.md 中记录迁移**

Append to `05-System/wiki/log.md`:

```markdown
## [2026-04-07] migrate | 00-Inbox 迁移
- 00-Inbox 为空，直接删除
- 新采集文章将保存到 raw/articles/ 并触发 wiki ingest
```

- [ ] **Step 4: Commit**

```bash
git add 00-Inbox/ 05-System/wiki/log.md
git commit -m "chore: retire 00-Inbox, all new articles go to raw/articles"
```

---

## Task 7: 功能验证

- [ ] **Step 1: 测试 CLI 编译通过**

Run:

```bash
cd /home/smith/Project/writer_cc && python -m py_compile src/writer_tools/cli.py src/writer_tools/claude_collector.py
```

Expected: 无输出。

- [ ] **Step 2: 测试目录结构完整**

Run:

```bash
ls -d raw/articles raw/papers raw/books raw/assets 05-System/wiki/sources 05-System/wiki/entities 05-System/wiki/concepts 05-System/wiki/syntheses 05-System/wiki/queries 05-System/wiki/index.md 05-System/wiki/log.md
```

Expected: 所有路径均存在。

- [ ] **Step 3: 测试 CLAUDE.md 已包含 LLM Wiki 规则**

Run:

```bash
grep -q "LLM Wiki 规则" /home/smith/Project/writer_cc/.claude/CLAUDE.md && echo "FOUND" || echo "MISSING"
```

Expected: `FOUND`

- [ ] **Step 4: 确认 00-Inbox 已删除**

Run:

```bash
test ! -d /home/smith/Project/writer_cc/00-Inbox && echo "DELETED" || echo "EXISTS"
```

Expected: `DELETED`

---

## Self-Review

**1. Spec coverage:**
- ✅ 创建 `raw/` 和 wiki 目录结构 → Task 1
- ✅ 初始化 `index.md` 和 `log.md` → Task 2
- ✅ 更新 `.claude/CLAUDE.md` schema → Task 5
- ✅ 迁移 `00-Inbox/` → Task 6
- ✅ 更新 CLI 输出路径 → Task 3, Task 4
- ✅ 测试验证 → Task 7

**2. Placeholder scan:** 无 TBD/TODO/"implement later"/"add appropriate error handling"

**3. Type consistency:** 所有 CLI 改动使用相同的 `RAW_DIR` 和 `WIKI_DIR` 变量名，无前后期不一致问题。

---

## 执行方式选择

Plan complete and saved to `docs/superpowers/plans/2026-04-07-llm-wiki-integration.md`.

Two execution options:

**1. Subagent-Driven (recommended)** - 每个 Task 派一个子代理执行，我在 Task 之间做审查
**2. Inline Execution** - 在当前会话中直接顺序执行

Which approach do you prefer?
