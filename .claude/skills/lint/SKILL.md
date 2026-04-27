---
name: lint
description: This skill should be used when the user says "/lint", "检查 wiki", "修复 wiki", "wiki 健康度", "整理 wiki", or asks to lint, check, fix, or clean up the vault's LLM Wiki layer under 05-System/wiki/.
version: 0.1.0
---

# Wiki Lint Skill

Check the health of the vault's LLM Wiki, report issues, and fix them after user confirmation.

## When to Use

- User explicitly says `/lint`
- User asks to check, fix, clean, or lint the wiki
- User mentions "wiki 健康度" or "整理 wiki"

## Workflow

### Step 1: Scan the Wiki Structure

Read and inspect the following directories:
- `05-System/wiki/index.md`
- `05-System/wiki/sources/`
- `05-System/wiki/entities/`
- `05-System/wiki/concepts/`
- `05-System/wiki/queries/`
- `05-System/wiki/syntheses/` (if exists)
- `05-System/wiki/log.md`

### Step 2: Detect Issues

For each page, check for:
1. **Missing frontmatter** — every wiki page should have a `type` field
2. **Orphaned pages** — pages not linked from `wiki/index.md`
3. **Broken internal links** — `[[Page Name]]` references to non-existent pages
4. **Empty or near-empty pages** — less than 50 characters of content (excluding frontmatter)
5. **Missing index entries** — pages exist but are not listed in `wiki/index.md`
6. **Inconsistent filenames** — wiki sources/entities/concepts should use the exact title as filename

### Step 3: Generate Report

Present findings as a markdown report to the user. Use this structure:

```markdown
## Wiki 健康检查报告

### 问题汇总
| 类别 | 数量 |
|------|------|
| 孤儿页面 | X |
| 损坏链接 | X |
| 空页面 | X |
| 缺失索引 | X |
| 其他问题 | X |

### 详细问题
1. **孤儿页面**: [[Page Name]] — 未被 index.md 引用
2. **损坏链接**: index.md 引用了不存在的 [[Missing Page]]
3. ...

### 建议修复
- 将 [[Page Name]] 添加到 index.md 的对应章节
- 删除或补充空页面 [[Empty Page]]
- ...
```

**Do not make any edits yet.** Wait for user confirmation.

### Step 4: Apply Fixes (After Confirmation)

If the user confirms (e.g. says "修复", "确认", "ok", "好的", "全部修复"):

1. Fix `wiki/index.md`:
   - Add missing entries under the correct section (`## Sources`, `## Entities`, `## Concepts`, `## Syntheses`, `## Queries`)
   - Remove broken links (or comment them out with `<!-- [[Broken]] -->`)
   - Keep sections sorted alphabetically or by insertion order; be consistent

2. For empty pages:
   - If the page has no meaningful content, delete it
   - If it should exist but is empty, either leave it with a stub or add a brief description based on related sources

3. For missing frontmatter:
   - Add minimal frontmatter (`type: entity|concept|source|query|synthesis`)

4. Update `wiki/log.md`:
   - Append a new entry under the current date explaining what was linted and fixed

### Step 5: Report Results

After applying fixes, tell the user:
- Which files were modified
- Which files were deleted (if any)
- A brief summary of changes

## Rules

- Always report before modifying
- Only modify files in `05-System/wiki/`
- Never modify `03-Resources/` or `raw/` files during lint
- Append to `wiki/log.md`, never rewrite history entries
