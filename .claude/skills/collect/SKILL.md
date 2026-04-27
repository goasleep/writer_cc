---
name: collect
description: Collect a web article and convert it to Markdown, saving it to the Vault's raw/articles/ directory. Automatically triggers wiki ingest AND article analysis (5-dimension + 3-dimension scoring) via AnalyzerAgent subagent. Use this skill whenever the user says /collect or asks to collect, save, clip, or archive a web article.
---

# Collect Skill

You are a writing library assistant. When the user wants to collect a single article from a URL:

1. Extract the URL from the user's request.
2. **Do not ask the user to run CLI commands.** Run the command yourself:
   ```bash
   uv run writer-collect collect <url>
   ```
3. The command will save the article to `raw/articles/` with standard YAML frontmatter.
4. After collection, automatically perform the full ingest pipeline:

   ### Step A: Wiki Ingest (by主 agent)
   - Read the newly saved article in `raw/articles/` to identify its title, source URL, author, and core arguments.
   - **Challenge Detection (NEW):** Before writing the source summary, check if the article contains:
     * Specific numbers with claims (% gains, "X times", "X days/weeks", improvements/reductions)
     * Absolute statements ("best", "only", "must", "certainly")
     * Methodology claims ("this method", "my framework", "X-step approach")
     * Data/research citations ("studies show", "data indicates", "experiments prove")
   - **If challenge triggers found:** Run a critical review prompt to identify:
     * Data source limitations (sample size, selective reporting, source credibility)
     * Prerequisite conditions (hidden assumptions, boundary conditions)
     * Applicability scope (specific scenarios/industries/user types where valid)
     * Potential conflicts of interest (author's incentives, product promotion)
     * Logical gaps (missing assumptions in argument chains)
     * Generate output in this format:
       ```markdown
       ## ⚠️ 局限性与前提条件
       - 数据来源：[说明]
       - 前提条件：[列出关键假设]
       - 适用范围：[说明边界]
       - 其他风险：[利益冲突/方法论缺陷等]
       ```
   - **If no triggers found:** Skip challenge step (no "局限性" section needed).
   - Write/update `05-System/wiki/sources/<article_title>.md` with a summary, source metadata, key takeaways, AND the limitations section if challenge was triggered.
   - Extract important entities (people, organizations, products) and create/update `05-System/wiki/entities/<entity_name>.md`.
   - Extract important concepts (ideas, frameworks, methodologies) and create/update `05-System/wiki/concepts/<concept_name>.md`.
   - Update `05-System/wiki/index.md` to reflect new or changed pages.
   - Append a new entry to `05-System/wiki/log.md` describing the ingest action (note if challenge was triggered).

   ### Step B: Article Analysis (by AnalyzerAgent subagent)
   - Launch an `Agent` with the **AnalyzerAgent** role.
   - Pass to the subagent:
     - `article_path`: `raw/articles/<title>.md`
     - `template_path`: `05-System/analyses/ANALYSIS_TEMPLATE.md`
     - `output_path`: `05-System/analyses/articles/<title>.md`
     - `source_url`: the original URL
   - The AnalyzerAgent must:
     1. Read the article and the template.
     2. Score the article on 8 dimensions: `content_depth`, `readability`, `originality`, `ai_flavor`, `virality_potential`, `structure`, `style`, `technique` (each 0-100).
     3. Determine `quality_tier` (S/A/B/C).
     4. Extract `style_tags`, `technique_tags`, `article_type`, `target_audience`, `core_hook`, `key_techniques`, `emotional_triggers`, `estimated_read_time`, `language`.
     5. Write the full analysis file to `05-System/analyses/articles/<title>.md`.
     6. Return a JSON summary with `scores`, `quality_tier`, `style_tags`, `technique_tags`, `article_type`, `summary`.

   ### Step C: Index Update (by主 agent)
   - Read the JSON summary from the subagent.
   - Update `05-System/analyses/indices/by-style.md` to include the article under each `style_tag`, sorted by `scores.style` descending.
   - Update `05-System/analyses/indices/by-technique.md` similarly.
   - Update `05-System/analyses/indices/by-article-type.md` under `article_type`, sorted by average score descending.
   - Append an entry to `05-System/analyses/log.md`.

5. Report back to the user with:
   - Article title
   - Save path (e.g., `raw/articles/<filename>.md`)
   - One-sentence summary of the core argument
   - 8-dimension score summary and `quality_tier`
   - List of newly created or updated wiki / analysis pages
