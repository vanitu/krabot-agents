---
name: prompt-templates-skill
description: Save, retrieve, and manage named prompt templates for image generation. Use when the user wants to save a prompt for reuse, list saved templates, load a template, or delete a template. Templates persist in templates.json across sessions.
---

# Prompt Templates Skill

Manage reusable prompt templates for image generation. Templates are stored in `templates.json` in the workspace root.

## Quick Start

```bash
# List all templates
python scripts/templates.py list

# Save a template
python scripts/templates.py save "cinematic landscape" "wide mountain panorama at golden hour, 8k, dramatic clouds" \
  --size 1696*960 --model wan2.6-t2i

# Get a template
python scripts/templates.py get "cinematic landscape"

# Delete a template
python scripts/templates.py delete "cinematic landscape"
```

## Storage Format

Templates are stored as JSON in `templates.json`:

```json
{
  "cinematic landscape": {
    "prompt": "wide mountain panorama at golden hour, 8k...",
    "parameters": {
      "size": "1696*960",
      "model": "wan2.6-t2i",
      "n": 1
    }
  }
}
```

## Script Commands

| Command | Description |
|---------|-------------|
| `list` | Output JSON array of all templates with name and preview |
| `get <name>` | Output full template as JSON, or `null` if not found |
| `save <name> <prompt>` | Save template with optional `--size`, `--model`, `--n`, `--negative` |
| `delete <name>` | Delete template, outputs `{"deleted": true/false}` |

## Notes

- Template names are normalized (lowercase, trimmed)
- `get` command performs case-insensitive search
- Set `PROMPT_TEMPLATES_DB` env var to use a custom database file
