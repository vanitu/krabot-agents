---
name: qwen-image-skill
description: Generate images from text prompts using Alibaba Cloud DashScope Wan text-to-image API. Use when the user wants to create AI-generated images from text descriptions. Requires DASHSCOPE_API_KEY and DASHSCOPE_REGION environment variables.
---

# Qwen Image Skill

Generate images from text prompts using the Alibaba Cloud DashScope Wan text-to-image API.

## Prerequisites

Set environment variables:
- `DASHSCOPE_API_KEY` - Your API key (starts with `sk-`)
- `DASHSCOPE_REGION` - `singapore` or `virginia`

## Quick Start

Use the provided script to generate images:

```bash
python scripts/generate_image.py "a fox in a snowy forest, cinematic lighting" --output ./fox.png
```

### Script Options

```bash
python scripts/generate_image.py "<prompt>" [options]

Options:
  --output PATH       Save image to file (default: download to current directory)
  --size SIZE         Image size: 1280*1280, 1104*1472, 1472*1104, 1696*960, 960*1696
  --n NUM             Number of images (1-4, default: 1)
  --negative TEXT     Negative prompt to exclude elements
  --model MODEL       Model to use: wan2.6-t2i (default), wan2.5-t2i-preview
```

## Workflow

The API uses async pattern:

1. **Create task** → Receive `task_id`
2. **Poll for result** → Status: `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`
3. **Download images** → URLs expire after 24 hours

Default poll interval: 10 seconds.

## Error Handling

Common errors and solutions:

| Code | Solution |
|------|----------|
| `DataInspectionFailed` | Content blocked - rephrase prompt |
| `IPInfringementSuspect` | Avoid trademarked characters/names |
| `Throttling` | Wait and retry |
| `InvalidApiKey` | Check DASHSCOPE_API_KEY |

## Reference

- **Full API documentation**: See [references/api-reference.md](references/api-reference.md)
- **Supported sizes**: 1280*1280 (1:1), 1104*1472 (3:4), 1472*1104 (4:3), 1696*960 (16:9), 960*1696 (9:16)
- **Supported models**: `wan2.6-t2i` (recommended), `wan2.5-t2i-preview`
