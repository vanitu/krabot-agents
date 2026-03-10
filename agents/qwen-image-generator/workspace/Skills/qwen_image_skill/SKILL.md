# Qwen Image Skill

Generate images from text prompts using the Alibaba Cloud DashScope Wan text-to-image API.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DASHSCOPE_API_KEY` | Your DashScope API key (starts with `sk-`) |
| `DASHSCOPE_REGION` | `singapore` or `virginia` |

### Base URL by region

```
singapore → https://dashscope-intl.aliyuncs.com
virginia  → https://dashscope-us.aliyuncs.com
```

---

## Step 1: Create an Async Image Generation Task

**Endpoint:** `POST <base_url>/api/v1/services/aigc/image-generation/generation`

**Headers:**
```
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
X-DashScope-Async: enable
```

**Request body:**
```json
{
  "model": "wan2.6-t2i",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          { "text": "<your prompt here>" }
        ]
      }
    ]
  },
  "parameters": {
    "size": "1280*1280",
    "n": 1,
    "negative_prompt": ""
  }
}
```

**Example (curl):**
```bash
curl -X POST "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "wan2.6-t2i",
    "input": {
      "messages": [
        { "role": "user", "content": [{ "text": "a fox in a snowy forest, cinematic lighting" }] }
      ]
    },
    "parameters": { "size": "1280*1280", "n": 1 }
  }'
```

**Successful response:**
```json
{
  "output": {
    "task_id": "abc123def456",
    "task_status": "PENDING"
  },
  "request_id": "xxx"
}
```

Save the `task_id` — you need it to poll for the result.

---

## Step 2: Poll for Task Completion

**Endpoint:** `GET <base_url>/api/v1/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer $DASHSCOPE_API_KEY
```

**Example (curl):**
```bash
curl "https://dashscope-intl.aliyuncs.com/api/v1/tasks/abc123def456" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Poll every 10 seconds.** Task status transitions:

```
PENDING → RUNNING → SUCCEEDED
                  → FAILED
```

---

## Step 3: Handle the Result

### On SUCCEEDED

```json
{
  "output": {
    "task_id": "abc123def456",
    "task_status": "SUCCEEDED",
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": [
            { "image_url": "https://...generated-image-1.png" }
          ]
        },
        "finish_reason": "stop"
      }
    ],
    "image_count": 1
  }
}
```

Extract image URLs from `output.choices[*].message.content[*].image_url`.

**Note:** Image URLs expire after 24 hours.

### On FAILED

```json
{
  "output": {
    "task_id": "abc123def456",
    "task_status": "FAILED",
    "code": "DataInspectionFailed",
    "message": "Output data may contain inappropriate content."
  }
}
```

Common failure codes:

| Code | Meaning |
|------|---------|
| `DataInspectionFailed` | Output blocked by content moderation |
| `IPInfringementSuspect` | Prompt flagged for potential IP infringement |
| `InvalidApiKey` | API key invalid or expired |
| `Throttling` | Rate limit exceeded — retry after a delay |

---

## Supported Models

| Model | Async | Notes |
|-------|-------|-------|
| `wan2.6-t2i` | Yes | Latest, recommended |
| `wan2.5-t2i-preview` | Yes | Previous generation |

## Supported Sizes

| Size string | Aspect ratio |
|-------------|-------------|
| `1280*1280` | 1:1 |
| `1104*1472` | 3:4 |
| `1472*1104` | 4:3 |
| `1696*960`  | 16:9 |
| `960*1696`  | 9:16 |
