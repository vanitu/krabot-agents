# Setup Guide

## Step 1: DashScope API Key

**What it is**
Your personal API key for Alibaba Cloud Model Studio (DashScope). The agent uses this to submit image generation jobs on your behalf.

**Where to find it**

1. Go to [Alibaba Cloud Model Studio console](https://bailian.console.aliyun.com/)
2. Sign in (or create a free account)
3. In the left sidebar, go to **API Key** → **Create API Key**
4. Copy the generated key — it starts with `sk-`

Keep this key secret. Anyone with your key can generate images charged to your account.

---

## Step 2: Region

Choose the DashScope region closest to you or your users.

| Region | Endpoint |
|--------|----------|
| Singapore (default) | dashscope-intl.aliyuncs.com |
| Virginia (US East) | dashscope-us.aliyuncs.com |

If you are unsure, use **Singapore** — it is the default international endpoint.

---

## Step 3: Default Image Size (optional)

Choose the default output resolution for generated images. You can always override this per-request.

| Option | Resolution | Best for |
|--------|-----------|----------|
| 1:1 — 1280×1280 (default) | Square | General purpose, social media |
| 3:4 — 1104×1472 | Portrait | Mobile wallpapers, portraits |
| 16:9 — 1696×960 | Landscape | Desktop wallpapers, banners |
| 9:16 — 960×1696 | Tall portrait | Stories, Reels |

---

## Step 4: Default Model (optional)

| Model | Description |
|-------|-------------|
| wan2.6-t2i (default) | Latest model, best quality, supports sync and async |
| wan2.5-t2i-preview | Previous generation, async only |

Use **wan2.6-t2i** unless you have a specific reason to use an older model.
