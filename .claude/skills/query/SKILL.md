---
name: query
description: This skill should be used when the user asks "/query <问题>", "搜索 wiki", "查询知识库", "在 wiki 里找答案", or asks any knowledge question that involves comparing, synthesizing, or analyzing information from the vault's wiki. Also trigger when the user says "帮我查一下" about topics covered in 05-System/wiki/.
version: 0.1.0
---

# Wiki Query Skill

Search the vault's LLM Wiki and synthesize an answer, then persist it to `wiki/queries/`.

## When to Use

- User explicitly says `/query <question>`
- User asks a knowledge question that requires synthesizing information from multiple wiki pages
- User wants to search or query the vault's wiki layer

## Workflow

### Step 1: Identify Relevant Wiki Pages

Read `05-System/wiki/index.md` to understand the current wiki structure.
Then use `Grep` to search for keywords across:
- `05-System/wiki/sources/`
- `05-System/wiki/entities/`
- `05-System/wiki/concepts/`
- `05-System/wiki/syntheses/` (if exists)

Read the most relevant pages. If many pages match, prioritize `concepts/` and `sources/`.

### Step 2: Synthesize the Answer

Compose a clear, well-structured answer in the user's language. Include:
- Direct answer to the question
- Supporting evidence from wiki pages (cite with `[[Page Name]]`)
- Any caveats or gaps in the current wiki

### Step 3: Persist to wiki/queries/

Create a new file at `05-System/wiki/queries/YYYY-MM-DD-<slug>.md` where:
- `YYYY-MM-DD` is today's date
- `<slug>` is a hyphenated, lowercase version of the question (e.g. `why-ts-for-agents`)

Use this frontmatter:
```yaml
---
type: query
question: "<exact question>"
answered_at: "YYYY-MM-DD"
---
```

File body structure:
```markdown
# <Question>

## Answer

<synthesized answer>

## Sources

- [[Source or Concept Page]] — <brief note on relevance>
```

### Step 4: Report to User

Return:
1. The synthesized answer (concise)
2. The file path where it was saved
3. A list of wiki pages consulted
