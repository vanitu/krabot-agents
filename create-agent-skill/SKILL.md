---
name: create-agent-workspace
description: Create a new agent workspace with all required files and folder structure for the Krabot platform. Use when the user wants to scaffold a new agent with proper workspace configuration, including agent.json, README.md, onboarding files, and the workspace folder with AGENTS.md, BOOTSTRAP.md, IDENTITY.md, SOUL.md, Tools.md, and USER.md.
---

# Create Agent Workspace Skill

Create a complete agent workspace structure for the Krabot platform.

## Quick Start

```bash
python scripts/create_agent.py --name "My Agent" --slug my-agent --category productivity
```

This creates:
```
my-agent/
├── agent.json
├── README.md
├── avatar.png (placeholder)
├── HelpGuide.md
├── OnBoarding.md
├── OnBoarding.json
├── KrabotSpecs.json
└── workspace/
    ├── AGENTS.md
    ├── BOOTSTRAP.md
    ├── IDENTITY.md
    ├── SOUL.md
    ├── Tools.md
    └── USER.md
```

## Required Files

### Root Level

| File | Purpose |
|------|---------|
| `agent.json` | Agent metadata: name, slug, category, tags, file references |
| `README.md` | User-facing description of what the agent does |
| `avatar.png` | Agent avatar image (128x128 recommended) |
| `HelpGuide.md` | Content shown when user sends /help |
| `OnBoarding.md` | Setup guide for configuring the agent |
| `OnBoarding.json` | Structured onboarding configuration |
| `KrabotSpecs.json` | Platform-specific settings (filled by engineer) |

### Workspace Level

| File | Purpose |
|------|---------|
| `AGENTS.md` | Core behavior: commands, workflows, confirmation flows |
| `BOOTSTRAP.md` | Startup verification: env vars, API tests, initialization |
| `IDENTITY.md` | Agent identity: name, role, tone, language, boundaries |
| `SOUL.md` | Base personality (picoclaw): helpful, friendly, concise |
| `Tools.md` | Available skills and their function documentation |
| `USER.md` | User preferences: style, timezone, language |

## Script Options

```bash
python scripts/create_agent.py [options]

Required:
  --name TEXT           Agent display name
  --slug TEXT           URL-friendly identifier (lowercase, hyphens)

Optional:
  --category TEXT       Agent category (default: general)
  --description TEXT    Short description
  --tags TEXT           Comma-separated tags
  --output DIR          Output directory (default: ./)
```

## Example

```bash
# Create a weather agent
python scripts/create_agent.py \
  --name "Weather Assistant" \
  --slug weather-assistant \
  --category utility \
  --description "Get weather forecasts and alerts" \
  --tags "weather,forecast,alerts"
```

## File Templates

After creation, edit these files to customize the agent:

1. **workspace/IDENTITY.md** — Set the agent's role, tone, and boundaries
2. **workspace/AGENTS.md** — Define command handlers and workflows
3. **workspace/Tools.md** — Document available skills
4. **workspace/BOOTSTRAP.md** — Add startup verification steps
5. **OnBoarding.md** — Write user setup instructions
6. **HelpGuide.md** — Create user-facing command reference

See [references/workspace-structure.md](references/workspace-structure.md) for detailed file format specifications.
