---
name: batch
description: Batch collect articles from multiple URLs and save them to the Vault's raw/articles/ directory. Use this skill whenever the user says /batch or wants to batch collect articles, process multiple URLs at once, or import a list of URLs from a file.
---

# Batch Skill

You are a writing library assistant. When the user wants to batch collect articles:

## Mode Detection

First, determine the input mode:

**Mode 1: File Input** (traditional)
- User provides a file path (`.txt`, `.csv`, or `.json`)
- User says "from file" or similar

**Mode 2: URL List** (new, parallel)
- User provides multiple URLs directly (space-separated, comma-separated, or multiple lines)
- User says "collect these URLs" or similar

## Mode 1: File Input (Sequential)

1. Read the input file provided by the user.
2. **Do not ask the user to run CLI commands.** Run:
   ```bash
   uv run writer-collect batch <input_file>
   ```
3. After completion, read `collection_report.json` if it exists.
4. For each successfully collected article, perform wiki ingest (see below).

## Mode 2: URL List (Parallel)

1. Extract all URLs from the user's input. Support formats:
   - Space-separated: `https://a.com https://b.com https://c.com`
   - Comma-separated: `https://a.com, https://b.com, https://c.com`
   - Multiple lines (paste from clipboard)

2. For each URL, **run the collect command in parallel** using background processes:
   ```bash
   uv run writer-collect collect <url> &
   ```
   OR use `xargs` for parallel execution:
   ```bash
   echo "<url1>" | uv run writer-collect collect
   echo "<url2>" | uv run writer-collect collect
   ...
   ```

   **IMPORTANT**: Run these concurrently, not sequentially. Use `&` or separate bash invocations.

3. Wait for all collect operations to complete.

4. Check `raw/articles/` for newly collected files (compare timestamps or list files).

5. For each newly collected article, perform wiki ingest (see below).

## Wiki Ingest (Common for Both Modes)

For each successfully collected article:

1. Read the article from `raw/articles/<title>.md`.
2. Write/update `05-System/wiki/sources/<article_title>.md` with summary and metadata.
3. Extract important entities and create/update `05-System/wiki/entities/<entity_name>.md`.
4. Extract important concepts and create/update `05-System/wiki/concepts/<concept_name>.md`.
5. Update `05-System/wiki/index.md`.
6. Append to `05-System/wiki/log.md`.

7. Launch AnalyzerAgent subagent for analysis:
   - Read the article and `05-System/analyses/ANALYSIS_TEMPLATE.md`
   - Generate 8-dimension analysis
   - Save to `05-System/analyses/articles/<title>.md`
   - Update indices in `05-System/analyses/indices/`
   - Append to `05-System/analyses/log.md`

## Reporting

After completing all operations, report to the user:

**Summary**:
- Total URLs processed
- Successfully collected
- Failed (if any)

**For each successful article**:
- Title
- Save path
- One-sentence summary of core argument
- 8-dimension scores and quality_tier (from AnalyzerAgent)
- List of newly created/updated wiki pages

**For failures** (if any):
- URL
- Error message

## Examples

**Mode 1 (File)**:
```
User: /batch urls.txt
→ Process file using writer-collect batch
```

**Mode 2 (URL List)**:
```
User: /batch https://a.com https://b.com https://c.com
→ Parallel collect all three URLs
```

```
User: /batch
https://a.com
https://b.com
https://c.com
→ Parallel collect all three URLs
```
