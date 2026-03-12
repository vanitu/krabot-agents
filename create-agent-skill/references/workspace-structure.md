# Agent Workspace Structure Reference

Complete specification for Krabot agent workspace files and formats.

## Root Level Files

### agent.json

Agent metadata and file references.

```json
{
  "name": "Agent Display Name",
  "slug": "agent-slug",
  "category": "utility|creative|productivity|entertainment|general",
  "short_description": "One-line description",
  "tags": ["tag1", "tag2"],
  "avatar": "avatar.png",
  "readme": "README.md",
  "help_guide": "HelpGuide.md",
  "onboarding_md": "OnBoarding.md",
  "onboarding_json": "OnBoarding.json",
  "workspace": "workspace"
}
```

### README.md

User-facing description of the agent. Should include:
- What the agent does
- How to use it
- File structure overview
- Requirements
- Limitations

### avatar.png

Agent avatar image. Recommended: 128x128 PNG with transparency.

### HelpGuide.md

Content shown when user sends `/help`. Should include:
- Command reference table
- Usage examples
- Troubleshooting section

### OnBoarding.md

Step-by-step setup guide for users. Include:
- Prerequisites
- Configuration steps
- Verification instructions

### OnBoarding.json

Structured onboarding configuration (optional, for UI wizard).

```json
{
  "steps": [
    {
      "title": "API Key",
      "description": "Enter your API key",
      "field": "api_key",
      "type": "string",
      "required": true
    }
  ]
}
```

### KrabotSpecs.json

Platform-specific configuration. Filled by platform engineers.

```json
{
  "_note": "This file is filled by a platform engineer...",
  "dockerImage": "",
  "configTemplate": "",
  "resources": {
    "cpu": "",
    "memory": ""
  }
}
```

---

## Workspace Files

### AGENTS.md

Core agent behavior specification.

**Sections to include:**

1. **Agent description** — What the agent does
2. **Core Rules** — Hard behavioral constraints (e.g., "Always confirm before action")
3. **Workflows** — Step-by-step handling of user requests
4. **Commands** — User-facing commands and their handling
5. **Boundaries** — What the agent does NOT do

**Example structure:**
```markdown
# Agent Name

Description of the agent's purpose.

---

## Core Rules

- Rule 1
- Rule 2

---

## Handling Requests

1. Step one
2. Step two
3. Step three

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |

---

## What You Do Not Do

- Don't do X
- Don't do Y
```

### BOOTSTRAP.md

Startup verification checklist. Executed once when agent starts.

**Standard sections:**

1. **Verify configuration** — Check required env vars
2. **Test connectivity** — Verify external services
3. **Initialize storage** — Create required files/databases
4. **Announce readiness** — Send "ready" message
5. **Enter normal operation** — Start processing requests

### IDENTITY.md

Agent identity, tone, and personality.

```markdown
# Identity

**Name:** Agent Name
**Role:** Primary role description
**Tone:** e.g., Friendly, professional, concise
**Language:** e.g., English, or "Match user's language"

## Behaviour Principles

- How to behave in interactions
- Response style guidelines

## Boundaries

- Topics to avoid
- Actions not to take
```

### SOUL.md

Base assistant personality (picoclaw). Usually kept standard.

```markdown
# Soul

I am picoclaw, a lightweight AI assistant powered by AI.

## Personality

- Helpful and friendly
- Concise and to the point
- Curious and eager to learn
- Honest and transparent

## Values

- Accuracy over speed
- User privacy and safety
- Transparency in actions
- Continuous improvement
```

### Tools.md

Documentation for available skills/tools.

```markdown
# Available Tools

---

## Skill Name

**Purpose:** What this skill does

**When to use:** When to invoke this skill

### function_name(param1, param2)

Description.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | string | yes | Description |

**Returns:**
```
Return value description
```
```

### USER.md

User preferences storage.

```markdown
# User

Information about user goes here.

## Preferences

- Communication style: (casual/formal)
- Timezone: (your timezone)
- Language: (preferred language)

## Personal Information

- Name: (optional)
- Location: (optional)
- Occupation: (optional)

## Learning Goals

- Preferred interaction style
- Areas of interest
```

---

## Skills Folder

`workspace/skills/` contains skill subdirectories.

Each skill:
- Has its own folder named after the skill
- Contains `SKILL.md` with YAML frontmatter
- May contain `scripts/`, `references/`, `assets/` subdirectories

Example:
```
skills/
└── my_skill/
    ├── SKILL.md
    ├── scripts/
    │   └── tool.py
    └── references/
        └── api-docs.md
```

See the [skill-creator skill](../../agents/qwen-image-generator/workspace/skills/skill-creator/SKILL.md) for skill authoring guidelines.
