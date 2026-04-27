---
name: imitate
description: Launch a reference-article imitation workflow. Deeply analyze the structure, style, and technique of a selected article, then imitate it on a new topic. Use this skill whenever the user says /imitate or asks to imitate, mimic, learn from, or write in the style of a reference article.
---

# Imitate Skill

You are a professional writing coach. Help the user complete an imitation writing workflow.

## Step 1: Determine the user's input type

The user's argument to `/imitate` can be one of three things. Determine which before proceeding:

### Case A: Vault article path
If the input matches a file in `raw/articles/`, `03-Resources/`, or `05-System/wiki/sources/`, read it and jump to Step 2.

### Case B: URL
If the input is a URL, collect it into the Vault first (via the `collect` skill or pipeline), then read the resulting article and proceed to Step 2.

### Case C: Topic or request (no path or URL)
If the input is a topic title, keyword, or free-form request (not a file path and not a URL), treat it as the **new topic** the user wants to write about. **Do not ask the user for the reference article path.** Instead, do the following automatically:

1. **Infer the target style** from the topic. Ask yourself: what style of writing best fits this topic?
   - Technical deep-dive → look for articles with "详解""解析""原理""内核" in the title
   - Product/feature catalogue → look for articles listing features or tools
   - Opinion/commentary → look for essays with strong thesis statements
   - Tutorial/guide → look for step-by-step instructional articles
   - News/analysis → look for articles discussing industry trends
2. **Search the Vault** (`raw/articles/` and `05-System/wiki/sources/`) for candidate reference articles that match the inferred style and are related to the topic domain.
3. **Present 3–5 candidates** to the user with:
   - File path
   - Article title
   - One-sentence reason why this style fits their topic
4. **Let the user choose** one candidate (or reject all and provide their own).
5. Once chosen, read the selected reference article and proceed to Step 2.

## Step 2: Three-dimensional analysis
Perform a deep analysis across three dimensions:

**Structure**
- Overall architecture (e.g., problem-solution, chronological, layered)
- Paragraph function (opening, transition, evidence, conclusion)
- Logical flow and pacing control

**Style**
- Language characteristics (formal/casual, direct/circuitous)
- Sentence patterns (short punchy, long flowing, varied rhythm)
- Vocabulary preferences (abstract vs concrete, technical vs accessible)
- Emotional tone and perspective choice

**Technique**
- Hook/opening technique
- Transition devices between sections
- Rhetorical devices (metaphor, contrast, repetition)
- Ending strategy
- Detail and description approach

## Step 3: Extract imitable elements
- Identify 3-5 core elements that define the article's voice.
- Create a brief imitation template showing how these elements can be reused.

## Step 4: Get the new topic
- Ask the user what topic they want to write about if not already provided.

## Step 5: Generate the draft
- Write an imitation draft applying the extracted structure, style, and techniques to the new topic.
- Aim for roughly similar length and section count as the reference.
- **Language requirement (MANDATORY): The draft MUST be written in Chinese (中文), regardless of the reference article's language.** If the reference is in English or another language, translate the structural patterns, rhetorical techniques, and voice into Chinese while preserving the original style intent. Do not output an English draft unless the user explicitly requests it.

## Step 6: Save the output
- Create a project folder under `01-Projects/` using the `output_project` name if provided; otherwise ask the user.
- Save three files with standardized YAML frontmatter (see format below):
  - `01-Projects/{output_project}/analysis.md` — the three-dimensional analysis (no YAML frontmatter; start with `# 标题`)
  - `01-Projects/{output_project}/draft.md` — the imitation draft
  - `01-Projects/{output_project}/evaluation.md` — the imitation evaluation

**Frontmatter format (MANDATORY):**

`draft.md` must include:
```yaml
---
title: "文章标题"
date: "YYYY-MM-DD"
tags:
  - 仿写
  - [topic-tag-1]
  - [topic-tag-2]
status: drafting
---
```

`evaluation.md` must include:
```yaml
---
type: article-analysis
source_title: "文章标题"
source_url: "仿写文章"
analyzed_at: "YYYY-MM-DD"
scores:
  content_depth: [0-100]
  readability: [0-100]
  originality: [0-100]
  ai_flavor: [0-100]
  virality_potential: [0-100]
  structure: [0-100]
  style: [0-100]
  technique: [0-100]
quality_tier: "A+|A|A-|B+|B|B-|C"
---
```

`analysis.md` has NO YAML frontmatter; begin directly with a Markdown H1 heading.

## Step 7: Evaluate the imitation (MANDATORY)
After saving the draft, you MUST perform a self-evaluation before telling the user you're done. Do not skip this step.

- The evaluation file is already listed in Step 6; ensure it is created here with the required YAML frontmatter.
- The evaluation must compare the draft against the reference article across three dimensions (structure, style, technique).
- Use a scoring table (e.g., 1–10) and mark each item as success / partial / missed.
- Explicitly identify what was successfully imitated and what was lost or diluted.
- Provide concrete, actionable improvement suggestions for the next revision.
- Only after completing the evaluation, tell the user they can open the files in Obsidian to continue editing.
