# Qwen Image Generator

Generate stunning AI images from text descriptions — directly in Telegram.

## What it does

- Accepts any text description and generates a high-quality image using Alibaba Cloud's Wan AI model
- Shows you a preview of what will be generated and **waits for your confirmation** before spending any API credits
- Supports portrait, landscape, and square image formats
- Lets you save your favourite prompts as **named templates** — no need to retype the same description every time
- Works entirely on-demand: no scheduled tasks, no automatic generation

## How it works

1. Send a text prompt (e.g. "a fox in a snowy forest, cinematic lighting")
2. The agent summarises what it will generate and the settings it will use
3. Reply **yes** to confirm — the agent submits the job to the Wan API and sends back the image when ready (typically under 2 minutes)
4. Optionally save the prompt as a template for reuse

## Requirements

- An Alibaba Cloud account with Model Studio (DashScope) enabled
- A DashScope API key (takes ~2 minutes to create)
- A Telegram bot for interacting with the agent

## Limitations

- Image generation takes 30 seconds to 2 minutes per request
- Generated image URLs expire after 24 hours — download any images you want to keep
- Content moderation is enforced by the API; prompts with prohibited content will be rejected
- Free-tier quotas apply; see Alibaba Cloud pricing for details
