# User Preferences

This file stores user-specific preferences for the Qwen Image Generator agent.

---

## Communication

| Setting | Value |
|---------|-------|
| **Language** | Match user's message (English or Russian) |
| **Style** | Friendly and concise |
| **Detail Level** | Brief explanations, focus on results |

---

## Default Generation Settings

| Setting | Default | Options |
|---------|---------|---------|
| **Size** | `1280*1280` (1:1) | 1:1, 3:4, 4:3, 16:9, 9:16 |
| **Model** | `wan2.6-t2i` | wan2.6-t2i, wan2.5-t2i-preview |
| **Count** | 1 | 1–4 |

---

## User Information

- **Name:** (optional — not required for image generation)
- **Location:** (optional — used for timezone context)
- **Preferred Image Types:** (user's favorite styles/subjects)

---

## Saved Templates

User's saved prompt templates are stored in `templates.json`.

To manage templates:
- `/templates` — List all saved templates
- `/use_template <name>` — Load a template
- `/save_template` — Save current prompt as template

---

## Notes

- This agent is designed **only for image generation** — it will not answer general questions
- All generation requests require explicit user confirmation
- Image URLs expire after 24 hours
