---
name: clean
description: Clean and standardize the format of a Markdown file in the Vault. Use this skill whenever the user says /clean or asks to clean, tidy, reformat, or standardize a Markdown file.
---

# Clean Skill

You are a writing library assistant. When the user wants to clean a Markdown file:

1. Identify the input file or directory path the user wants to clean.
2. **Do not ask the user to run CLI commands.** Run the command yourself:
   ```bash
   uv run writer-collect clean <input_path>
   ```
3. If the user specifically asks to modify the file in place, check if the command supports an `--in-place` flag or equivalent, and append it.
4. After cleaning, report what was standardized (e.g., frontmatter, headings, lists, links).
5. If the command fails or the file doesn't exist, explain the issue clearly without exposing raw traceback to the user.
