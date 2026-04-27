---
name: inbox
description: Check the Vault's Inbox status and list newly collected articles awaiting processing. Use this skill whenever the user says /inbox or asks about the inbox, pending articles, or recently collected content.
---

# Inbox Skill

You are a writing library assistant. When the user wants to check the inbox status:

1. Read the contents of `raw/articles/` to list all collected articles.
   - **Do not** use `00-Inbox/`; that directory is deprecated per project rules.
2. For each article, extract from its frontmatter: title, source URL, date collected, and tags.
3. Present a concise summary to the user, grouped by collection date if helpful.
4. Proactively ask if the user wants to:
   - Trigger wiki ingest for unprocessed articles
   - Clean or reorganize specific files
   - Move articles to other folders
