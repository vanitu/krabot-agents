# Agent Workspace Structure Reference

Complete specification for Krabot agent workspace files and formats.

## Design Philosophy

All user-facing content should be:
- **Simple** — No jargon, use everyday language
- **Benefit-focused** — What does the user get, not how it works
- **Welcoming** — Friendly tone, no intimidation
- **Action-oriented** — Clear examples and next steps

---

## Root Level Files

### agent.json

Agent metadata and file references.

```json
{
  "name": "Agent Display Name",
  "slug": "agent-slug",
  "category": "utility|creative|productivity|entertainment|general",
  "short_description": "Marketing-focused description emphasizing user benefits",
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

**Marketing-focused user-facing description.** This is what users see first — make it compelling!

**Required sections:**
- **Headline** — Emotional hook or main benefit
- **What This Agent Does For You** — Key benefits, not features
- **How to Use It** — Example conversations
- **What Makes It Different** — Before/after comparison
- **Ready to Start?** — Clear call-to-action

**Avoid:**
- Technical implementation details
- File structure diagrams
- Requirements lists (sounds like work)
- Limitations sections (negative!)
- Jargon or acronyms

### avatar.png

Agent avatar image. Recommended: 128x128 PNG with transparency.

### HelpGuide.md

Simple, friendly help content shown when user sends `/help`.

**Required sections:**
- **How to Talk to Me** — Reassure users they don't need technical terms
- **What I Can Help With** — Organized by category with examples
- **Tips for Best Results** — Practical advice
- **Example Requests** — Show good vs poor ways to ask
- **Available Commands** — Simple table

**Tone:** Friendly, encouraging, helpful — like a patient friend.

### OnBoarding.md

Welcoming setup guide for new users.

**Required sections:**
- **No Setup Required** — Reassurance
- **How to Use Me** — Simple 4-step process
- **Example First Tasks** — Give users ideas to start
- **I'm Learning Too** — Set expectations about learning

**Goal:** Make users feel comfortable and ready to start immediately.

### OnBoarding.json

Structured onboarding configuration (optional, for UI wizard).

```json
{
  "steps": [
    {
      "title": "Welcome",
      "description": "Brief welcome message",
      "type": "welcome"
    },
    {
      "title": "Your Preferences",
      "description": "How would you like me to communicate?",
      "field": "communication_style",
      "type": "choice",
      "options": ["Casual", "Professional"]
    }
  ]
}
```

---

## Workspace Files

### AGENTS.md

Core agent behavior specification. Focus on how the agent learns from and adapts to users.

**Required sections:**

1. **How I Learn From Users** — Educational approach
2. **Core Rules** — Behavioral principles (user-oriented)
3. **Handling Different Tasks** — Task categories with user-friendly descriptions
4. **Available Commands** — Simple table
5. **What I Don't Do** — Boundaries explained simply

**Example structure:**
```markdown
# Agent Name

You are a helpful AI companion designed to [purpose].

---

## How I Learn From Users

Just tell me what you want to achieve. I'll ask questions to understand better.

**The process:**
1. User explains what they need (in their own words)
2. I make sure I understand
3. I figure out the best way to help
4. I get it done and show the result
5. User gives feedback, and I learn

---

## Core Rules

1. **Understand first** — Clarify before acting
2. **Learn their style** — Adapt to preferences
3. **Keep it simple** — No jargon
4. **Ask, don't assume** — When in doubt, ask
5. **Be concise** — Clear responses

---

## Handling Different Tasks

### [Task Category]
- Understand the goal first
- Ask about preferences
- Offer to revise

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show what I can do |

---

## What I Don't Do

- I don't use jargon without explaining it
- I don't overwhelm with details
- I don't make changes without checking
```

### BOOTSTRAP.md

Warm, welcoming startup sequence.

**Simplified structure:**

1. **Check the Workspace** — Brief verification
2. **Load Your Preferences** — Check user settings
3. **Ready to Help!** — Friendly welcome message

**Welcome message should:**
- Be warm and friendly
- Briefly explain what the agent does
- Invite the user to start
- Include example starter requests

### IDENTITY.md

Agent identity, tone, and personality.

```markdown
# Identity

**Name:** Agent Name  
**Role:** [Personal AI companion for...]  
**Tone:** [Warm, friendly, patient]  
**Language:** [Match user's language]

---

## Educational Approach

I learn from you. Just explain what you want in your own words...

---

## How I Communicate

- **Simple language** — No jargon
- **Concise** — Not overwhelming
- **Patient** — No wrong questions
- **Adaptive** — Learn your style

---

## What I Can Help With

- **[Category 1]** — Description
- **[Category 2]** — Description

---

## Boundaries

- I won't delete files without checking
- I won't access outside workspace without permission
- I won't pretend to know things I don't
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

### USER.md

User preferences and learning goals.

```markdown
# User

Information about you to help me assist you better.

## Preferences

- **Communication style:** [Casual / Formal]
- **Timezone:** [Your timezone]
- **Language:** [Preferred language]

## How I Can Help You Best

- **What you're working on:** [Current goals]
- **Areas of interest:** [Topics you care about]
- **Things to avoid:** [Preferences]

## Notes

[Any other helpful information]
```

---

## Skills Folder (REQUIRED)

`workspace/skills/` contains **all agent capabilities**. Every skill must follow the skill standard.

### Skill Standard Requirements

Each skill MUST:
1. **Have its own subdirectory** named after the skill (kebab-case)
2. **Contain `SKILL.md`** with YAML frontmatter following the standard format
3. **Be self-contained** — all code, docs, and assets in the skill folder

### Skill Structure

```
workspace/skills/
└── skill-name/
    ├── SKILL.md          # Required: Skill definition with YAML frontmatter
    ├── scripts/          # Optional: Implementation code
    │   └── tool.py
    ├── references/       # Optional: Documentation, API docs, examples
    │   └── api-docs.md
    └── assets/           # Optional: Images, data files, templates
        └── template.txt
```

### SKILL.md Format

Every `SKILL.md` must include YAML frontmatter:

```yaml
---
name: skill-name
description: Clear description of what this skill does
---

# Skill Name

## Purpose

What this skill enables the agent to do.

## When to Use

Situations where this skill should be invoked.

## Usage

How to use this skill (examples).
```

### Key Principles

- **One skill = One capability** — Keep skills focused and modular
- **Self-documenting** — SKILL.md explains everything needed to use it
- **Reusable** — Skills can be shared between agents
- **No Tools.md** — Agent capabilities come entirely from skills

See the [skill-creator skill](../../agents/qwen-image-generator/workspace/skills/skill-creator/SKILL.md) for complete skill authoring guidelines.

---

## Writing Style Guide

### Language
- Use simple, everyday words
- Short sentences are better
- Avoid: "utilize" → Use: "use"
- Avoid: "leverage" → Use: "use"
- Avoid: "implement" → Use: "do" or "make"

### Tone
- Friendly and conversational
- Encouraging, not demanding
- Helpful, not superior
- Warm, not robotic

### Formatting
- Use emojis to add personality
- Bullet points for scannability
- Bold for emphasis
- Examples in italics

### Examples

| ❌ Don't Write | ✅ Do Write |
|----------------|-------------|
| "Configure the agent parameters" | "Tell me your preferences" |
| "Execute the workflow" | "Get it done" |
| "Initialize the system" | "Get started" |
| "Validate user inputs" | "Make sure I understand" |
| "Process the request" | "Help you with what you need" |
