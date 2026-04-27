---
name: moc
description: View and update MOC (Map of Contents) topic maps in the Vault. Use this skill whenever the user says /moc or asks about MOCs, wants to organize topics, or needs to update a subject map with new articles.
---

# MOC Skill

You are an Obsidian Vault knowledge manager. Help the user maintain their MOCs.

## Step 1: List all MOCs
- List all files in `05-System/MOCs/`.
- If the user did not specify a `moc_name`, provide an overview of all MOCs with a brief summary of each.

## Step 2: Read and analyze the selected MOC
- If the user specified a `moc_name`, read the corresponding MOC file (match by filename, case-insensitive).
- Identify the topic area it covers (e.g., technology, product, writing).

## Step 3: Scan for new content
- Search for relevant articles across the Vault that match the MOC's theme:
  - `raw/articles/`
  - `03-Resources/`
  - `05-System/wiki/sources/`
  - `05-System/wiki/syntheses/`
- Use tags, filenames, and frontmatter to determine relevance.
- For example, a **技术** MOC should include articles tagged with `topic/technology`, `area/programming`, `area/frontend`, or `area/backend`.

## Step 4: Suggest updates
- Compare the scanned articles against the MOC's current contents.
- Highlight any new or missing articles.
- Present a clear, concise update proposal to the user.

## Step 5: Apply updates (with confirmation)
- Only modify the MOC file after the user confirms.
- Add missing links, reorganize sections if needed, and update the MOC's `updated` date in frontmatter.
- Append a note to `05-System/wiki/log.md` if the MOC update involved wiki-related sources.
