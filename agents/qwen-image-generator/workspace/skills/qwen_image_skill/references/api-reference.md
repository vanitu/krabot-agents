# DashScope Image Generation API Reference

Complete API reference for the DashScope Wan text-to-image API.

## Base URLs

| Region | URL |
|--------|-----|
| singapore | `https://dashscope-intl.aliyuncs.com` |
| virginia | `https://dashscope-us.aliyuncs.com` |

## Create Async Task

**Endpoint:** `POST /api/v1/services/aigc/image-generation/generation`

**Headers:**
```
Authorization: Bearer {DASHSCOPE_API_KEY}
Content-Type: application/json
X-DashScope-Async: enable
```

**Request Body:**
```json
{
  "model": "wan2.6-t2i",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [{ "text": "your prompt here" }]
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

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model` | string | Yes | Model name: `wan2.6-t2i` or `wan2.5-t2i-preview` |
| `input.messages` | array | Yes | Array of message objects with role and content |
| `parameters.size` | string | No | Image dimensions (see Supported Sizes) |
| `parameters.n` | integer | No | Number of images (1-4, default: 1) |
| `parameters.negative_prompt` | string | No | Elements to exclude from generation |

**Response (Success):**
```json
{
  "output": {
    "task_id": "abc123def456",
    "task_status": "PENDING"
  },
  "request_id": "xxx"
}
```

## Poll Task Status

**Endpoint:** `GET /api/v1/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer {DASHSCOPE_API_KEY}
```

**Response (Success):**
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
            { "image_url": "https://..." }
          ]
        },
        "finish_reason": "stop"
      }
    ],
    "image_count": 1
  }
}
```

**Response (Failure):**
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

## Task Status Values

| Status | Description |
|--------|-------------|
| `PENDING` | Task queued, waiting to start |
| `RUNNING` | Task is processing |
| `SUCCEEDED` | Task completed successfully |
| `FAILED` | Task failed (see `code` and `message`) |

## Error Codes

| Code | Description |
|------|-------------|
| `DataInspectionFailed` | Content blocked by moderation |
| `IPInfringementSuspect` | Potential IP violation detected |
| `InvalidApiKey` | API key invalid or expired |
| `Throttling` | Rate limit exceeded |

## Supported Models

| Model | Notes |
|-------|-------|
| `wan2.6-t2i` | Latest, recommended |
| `wan2.5-t2i-preview` | Previous generation |

## Supported Sizes

| Size | Aspect Ratio |
|------|--------------|
| `1280*1280` | 1:1 |
| `1104*1472` | 3:4 |
| `1472*1104` | 4:3 |
| `1696*960` | 16:9 |
| `960*1696` | 9:16 |

## Notes

- Image URLs expire after 24 hours
- Poll every 10 seconds recommended
- Typical generation time: 30-120 seconds
