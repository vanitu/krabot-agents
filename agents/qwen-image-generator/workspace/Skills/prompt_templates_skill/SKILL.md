# Prompt Templates Skill

Save and reuse named image prompt templates. Templates persist in `templates.json` inside the agent workspace across sessions.

## Storage Format

Templates are stored in `templates.json` at the workspace root:

```json
{
  "cinematic landscape": {
    "prompt": "wide mountain panorama at golden hour, 8k, highly detailed, dramatic clouds",
    "parameters": {
      "size": "1696*960",
      "model": "wan2.6-t2i",
      "n": 1
    }
  },
  "portrait studio": {
    "prompt": "professional headshot, soft studio lighting, neutral background, sharp focus",
    "parameters": {
      "size": "1104*1472",
      "model": "wan2.6-t2i",
      "n": 1
    }
  }
}
```

- Keys are template names (lowercase, trimmed)
- Each entry contains `prompt` (string) and `parameters` (object with `size`, `model`, `n`)
- If `templates.json` does not exist yet, treat it as an empty object `{}`

---

## Operations

### list()

Read `templates.json` and return all template entries as a summary list.

**Returns:** array of objects, or empty array if no templates saved.

```json
[
  { "name": "cinematic landscape", "preview": "wide mountain panorama at golden hour, 8k, highly..." },
  { "name": "portrait studio",     "preview": "professional headshot, soft studio lighting, neutr..." }
]
```

`preview` is the first 60 characters of `prompt` followed by `...` if truncated.

---

### get(name)

Find a template by name (case-insensitive, trimmed match).

**Returns:** full template object if found, `null` if not found.

```json
{
  "name": "cinematic landscape",
  "prompt": "wide mountain panorama at golden hour, 8k, highly detailed, dramatic clouds",
  "parameters": {
    "size": "1696*960",
    "model": "wan2.6-t2i",
    "n": 1
  }
}
```

---

### save(name, prompt, parameters)

Write or overwrite a template entry.

**Steps:**
1. Read `templates.json` (create empty `{}` if missing)
2. Normalise `name`: lowercase, trim whitespace
3. Set `templates[name] = { prompt, parameters }`
4. Write the updated object back to `templates.json`

**Returns:**
```json
{ "saved": true }
```

---

### delete(name)

Remove a template by name.

**Steps:**
1. Read `templates.json`
2. Normalise `name`: lowercase, trim
3. If key exists: delete it and write back; return `{ "deleted": true }`
4. If key not found: return `{ "deleted": false, "reason": "not found" }`

---

## Example: Full Workflow

```
# User says: "save as template"
# Agent calls: prompt_templates_skill.save("cinematic landscape", "...", { size, model, n })

# User says: /templates
# Agent calls: prompt_templates_skill.list()
# → [{ name: "cinematic landscape", preview: "wide mountain panorama..." }]

# User says: /use_template cinematic landscape
# Agent calls: prompt_templates_skill.get("cinematic landscape")
# → { prompt: "...", parameters: { ... } }
# → Agent shows confirmation summary and waits for user to approve before generating
```
