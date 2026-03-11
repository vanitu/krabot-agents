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

## File Structure

```
qwen-image-generator/
├── agent.json              # Agent metadata (name, slug, category, etc.)
├── README.md               # This file — user-facing description
├── avatar.png              # Agent avatar image
├── HelpGuide.md            # Help content for /help command
├── OnBoarding.md           # User setup guide (API key, region, settings)
├── OnBoarding.json         # Structured onboarding configuration
├── KrabotSpecs.json        # Platform-specific configuration (filled by engineer)
└── workspace/              # Agent runtime workspace
    ├── AGENTS.md           # Agent behavior, rules, and workflows
    ├── BOOTSTRAP.md        # Startup verification steps
    ├── IDENTITY.md         # Agent identity, tone, personality
    ├── SOUL.md             # Base assistant personality (picoclaw)
    ├── Tools.md            # Available tools/skills documentation
    ├── USER.md             # User preferences storage
    └── skills/             # Skill definitions
        ├── qwen_image_skill/
        │   ├── SKILL.md
        │   ├── scripts/
        │   └── references/
        ├── prompt_templates_skill/
        │   ├── SKILL.md
        │   └── scripts/
        └── ...
```

### Workspace Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Core agent behavior: command handling, confirmation flows, error handling |
| `BOOTSTRAP.md` | Startup checklist: verify env vars, test API connectivity, initialize storage |
| `IDENTITY.md` | Agent identity: name, role, tone, language, boundaries |
| `SOUL.md` | Base assistant personality (picoclaw) — helpful, friendly, concise |
| `Tools.md` | Documentation for available skills and their functions |
| `USER.md` | User preferences: communication style, timezone, language |

### Agent Configuration (agent.json)

```json
{
  "name": "Qwen Image Generator",
  "slug": "qwen-image-generator",
  "category": "creative",
  "short_description": "...",
  "tags": ["image-generation", "ai", "alibaba-cloud", "wan"],
  "avatar": "avatar.png",
  "readme": "README.md",
  "help_guide": "HelpGuide.md",
  "onboarding_md": "OnBoarding.md",
  "onboarding_json": "OnBoarding.json",
  "workspace": "workspace"
}
```

## Requirements

- An Alibaba Cloud account with Model Studio (DashScope) enabled
- A DashScope API key (takes ~2 minutes to create)
- A Telegram bot for interacting with the agent

### Environment Variables

- `DASHSCOPE_API_KEY` — Your DashScope API key (starts with `sk-`)
- `DASHSCOPE_REGION` — Region: `singapore` or `virginia`

## Limitations

- Image generation takes 30 seconds to 2 minutes per request
- Generated image URLs expire after 24 hours — download any images you want to keep
- Content moderation is enforced by the API; prompts with prohibited content will be rejected
- Free-tier quotas apply; see Alibaba Cloud pricing for details
