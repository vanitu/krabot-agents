# Available Tools

---

## qwen_image_skill

**Purpose:** Generate images from text prompts using the Alibaba Cloud DashScope Wan text-to-image API.

**When to use:** ONLY after the user has explicitly confirmed the generation in the current session. Never call this autonomously.

### generate(prompt, size, model, n, negative_prompt)

Submits an async image generation task and polls for the result. Returns a list of image URLs on success.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | yes | The positive text description of the image to generate |
| `size` | string | yes | Resolution in `width*height` format (e.g. `1280*1280`) |
| `model` | string | yes | Model ID: `wan2.6-t2i` or `wan2.5-t2i-preview` |
| `n` | integer | no | Number of images to generate (1–4, default 1) |
| `negative_prompt` | string | no | Description of what to avoid in the image |

**Returns on success:**
```
{
  "status": "SUCCEEDED",
  "images": ["https://...url1...", "https://...url2..."]
}
```

**Returns on failure:**
```
{
  "status": "FAILED",
  "reason": "DataInspectionFailed"   // or other error code
}
```

**Notes:**
- Generation typically takes 30–90 seconds; the skill handles polling automatically (every 10 seconds)
- Image URLs expire 24 hours after generation
- Reads `DASHSCOPE_API_KEY` and `DASHSCOPE_REGION` from environment automatically

---

## prompt_templates_skill

**Purpose:** Save, list, load, and delete named prompt templates. Templates are stored in `templates.json` inside the agent workspace and persist across sessions.

**When to use:**
- When the user wants to save a prompt for future reuse (`save_template`)
- When the user asks to see saved templates (`/templates`)
- When the user wants to load a template (`/use_template`)
- When the user wants to delete a saved template

**Important:** Always confirm with the user before calling `save()` or `delete()`.

### list()

Returns all saved templates with name and a short prompt preview.

```
Returns: [{ "name": "...", "preview": "..." }, ...]
Returns: [] if no templates saved
```

### get(name)

Returns the full template by name (case-insensitive match).

```
Returns: { "name": "...", "prompt": "...", "parameters": { "size": "...", "model": "...", "n": 1 } }
Returns: null if not found
```

### save(name, prompt, parameters)

Saves or overwrites a named template. Call only after user has confirmed.

```
Parameters:
  name        string   Template name (free text, e.g. "cinematic landscape")
  prompt      string   The full prompt text
  parameters  object   { "size": "1280*1280", "model": "wan2.6-t2i", "n": 1 }

Returns: { "saved": true }
```

### delete(name)

Removes a template by name. Call only after user has confirmed.

```
Parameters:
  name   string   Template name to remove

Returns: { "deleted": true }  or  { "deleted": false, "reason": "not found" }
```
