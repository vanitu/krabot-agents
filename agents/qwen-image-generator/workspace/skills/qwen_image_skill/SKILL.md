---
name: qwen-image-skill
description: Generate images from text prompts using Alibaba Cloud DashScope Wan text-to-image API. Async workflow with 3 scripts. Requires DASHSCOPE_API_KEY and DASHSCOPE_REGION environment variables.
---

# Qwen Image Skill

Generate images from text prompts using the Alibaba Cloud DashScope Wan text-to-image API.

## Prerequisites

Set environment variables:
- `DASHSCOPE_API_KEY` - Your API key (starts with `sk-`)
- `DASHSCOPE_REGION` - `singapore` or `virginia`

## Async Workflow (3 Scripts)

The API uses async pattern. Use these 3 scripts in sequence:

### 1. Create Task

Creates the generation task and returns a `task_id` immediately:

```bash
python3 scripts/create_task.py "a fox in snowy forest" --size "1280*1280" --n 1
```

**Output:** `{"task_id": "abc-123", "status": "PENDING"}`

| Option | Description |
|--------|-------------|
| `--size` | Image size: `"1280*1280"`, `"1104*1472"`, `"1472*1104"`, `"1696*960"`, `"960*1696"` |
| `--n` | Number of images (1-4, default: 1) |
| `--negative` | Negative prompt (what to exclude) |
| `--model` | Model: `wan2.6-t2i` (default) or `wan2.5-t2i-preview` |

### 2. Check Status

Poll until status is `SUCCEEDED` or `FAILED`:

```bash
python3 scripts/check_status.py <task_id>
```

**Output examples:**

Pending/Running:
```json
{"status": "PENDING"}
{"status": "RUNNING"}
```

Success:
```json
{"status": "SUCCEEDED", "urls": ["https://...", "https://..."]}
```

Failed:
```json
{"status": "FAILED", "error": "DataInspectionFailed: Content blocked"}
```

**Typical timing:** Check every 10-15 seconds. Usually takes 30-90 seconds.

### 3. Download Images

Download each URL to a file:

```bash
python3 scripts/download_image.py "<url>" "./output.png"
```

**Output:** `{"success": true, "path": "./output.png"}`

## Full Example Workflow

```bash
# Step 1: Create task
TASK=$(python3 scripts/create_task.py "colorful avatar" --size "1280*1280" --n 1)
TASK_ID=$(echo $TASK | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")

# Step 2: Wait and check (repeat until SUCCEEDED)
sleep 30
STATUS=$(python3 scripts/check_status.py "$TASK_ID")
# Parse: echo $STATUS | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])"

# Step 3: Download each URL
python3 scripts/download_image.py "<url_from_status>" "./avatar.png"
```

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `DataInspectionFailed` | Content blocked | Rephrase prompt |
| `IPInfringementSuspect` | IP violation detected | Avoid trademarked names |
| `InvalidApiKey` | Bad API key | Check DASHSCOPE_API_KEY |
| `Throttling` | Rate limited | Wait and retry |

## Size Reference

| Size | Aspect |
|------|--------|
| `1280*1280` | 1:1 |
| `1104*1472` | 3:4 (portrait) |
| `1472*1104` | 4:3 (landscape) |
| `1696*960` | 16:9 (widescreen) |
| `960*1696` | 9:16 (mobile) |

## Reference

See [references/api-reference.md](references/api-reference.md) for full API details.
