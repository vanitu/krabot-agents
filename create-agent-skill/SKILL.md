---
name: create-agent-workspace
description: Create a new agent workspace with all required files and folder structure for the Krabot platform. Use when the user wants to scaffold a new agent with proper workspace configuration, including agent.json, README.md, onboarding files, and the workspace folder with AGENTS.md, BOOTSTRAP.md, IDENTITY.md, SOUL.md, USER.md, and the skills/ folder.
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
├── agent.json              # Agent metadata
├── README.md               # User-facing description (marketing focused)
├── avatar.png              # Agent avatar
├── HelpGuide.md            # Help content for /help command
├── OnBoarding.md           # User setup guide
└── OnBoarding.json         # Onboarding configuration
└── workspace/
    ├── AGENTS.md           # Agent behavior and workflows
    ├── BOOTSTRAP.md        # Startup verification
    ├── IDENTITY.md         # Agent identity and tone
    ├── SOUL.md             # Base assistant personality
    ├── USER.md             # User preferences
    └── skills/             # Agent skills (REQUIRED)
```

## Required Files

### Root Level

| File | Purpose |
|------|---------|
| `agent.json` | Agent metadata: name, slug, category, tags, file references |
| `README.md` | **Marketing-focused** user-facing description. Should sell the benefits! |
| `avatar.png` | Agent avatar image (128x128 recommended) |
| `HelpGuide.md` | Simple, friendly help content when user sends /help |
| `OnBoarding.md` | Easy, welcoming setup guide for new users |
| `OnBoarding.json` | Structured onboarding configuration (optional) |

### Workspace Level

| File | Purpose |
|------|---------|
| `AGENTS.md` | Core behavior: how the agent handles requests, learns from users |
| `BOOTSTRAP.md` | Warm startup sequence and welcome message |
| `IDENTITY.md` | Agent personality: role, tone, communication style |
| `SOUL.md` | Base personality (picoclaw) — usually kept standard |
| `USER.md` | User preferences and learning goals |
| `skills/` | **Required folder for all agent skills** — see Skills section below |

## Script Options

```bash
python scripts/create_agent.py [options]

Required:
  --name TEXT           Agent display name
  --slug TEXT           URL-friendly identifier (lowercase, hyphens)

Optional:
  --category TEXT       Agent category (default: general)
  --description TEXT    Marketing description — focus on user benefits!
  --tags TEXT           Comma-separated tags
  --output DIR          Output directory (default: ./)
```

## Example

```bash
# Create a meal planning agent
python scripts/create_agent.py \
  --name "Meal Planner" \
  --slug meal-planner \
  --category productivity \
  --description "Your personal meal planning assistant that creates weekly menus, generates shopping lists, and helps you eat healthier without the stress" \
  --tags "meal-planning,recipes,shopping,nutrition"
```

## Customizing Your Agent

After creation, edit these files to make your agent unique:

### 1. **README.md** — Make it Marketing-Focused

The README is what users see first. Make it compelling!

**Include:**
- **Emotional hook** — What pain does this solve?
- **Key benefits** — What will users get?
- **Example conversations** — Show, don't just tell
- **Comparison table** — Before vs after using your agent
- **Testimonials** — Real use cases (or anticipated ones)
- **Clear call-to-action** — How to get started

**Avoid:**
- Technical jargon
- File structure diagrams (boring!)
- Requirements lists (sounds like work)
- "Limitations" sections (negative!)

### 2. **OnBoarding.md** — Keep it Welcoming

Make new users feel comfortable:
- Emphasize "no setup required"
- Give example first tasks
- Explain "how to talk to me" in simple terms
- Reassure users that there's no "wrong way" to ask

### 3. **HelpGuide.md** — Make it Practical

Focus on helping users succeed:
- Show example conversations (good vs poor requests)
- List what the agent can do in plain language
- Give tips for best results
- Keep it friendly and encouraging

### 4. **workspace/IDENTITY.md** — Define Personality

Set how your agent communicates:
- **Role** — What kind of companion is this?
- **Tone** — Friendly? Professional? Warm? Playful?
- **Educational approach** — How does it learn from users?
- **Communication style** — Simple language, no jargon

### 5. **workspace/AGENTS.md** — Define Behavior

Document how the agent handles different situations:
- **Learning process** — How it adapts to users
- **Core rules** — What principles guide its actions?
- **Task categories** — How it handles different types of requests
- **Boundaries** — What it won't do

### 6. **workspace/skills/** — Add Required Skills

All agent capabilities must be implemented as **skills** in this folder. Each skill:
- Has its own subdirectory (e.g., `skills/my-skill/`)
- Contains a `SKILL.md` file with skill definition
- Follows the [skill standard](../../agents/qwen-image-generator/workspace/skills/skill-creator/SKILL.md)
- Is documented with purpose, usage, and examples

**No Tools.md needed** — agent capabilities come entirely from skills.

See [references/workspace-structure.md](references/workspace-structure.md) for detailed file format specifications.

## Writing Tips for User-Facing Agents

### Do:
- ✅ Use simple, everyday language
- ✅ Focus on benefits, not features
- ✅ Include emotional hooks and pain points
- ✅ Show real examples and conversations
- ✅ Make it welcoming for non-technical users
- ✅ Emphasize "no setup required"
- ✅ Use friendly, conversational tone

### Don't:
- ❌ Use jargon, acronyms, or technical terms
- ❌ Focus on implementation details
- ❌ Include "Requirements" or "Limitations" sections
- ❌ Assume technical knowledge
- ❌ Be dry or overly formal
- ❌ Show file structures or code

## Example: Good vs Bad README

### ❌ Bad (Technical Focus)

```markdown
# Meal Planner

An agent for meal planning using recipe APIs.

## Requirements
- Node.js 16+
- Spoonacular API key
- MongoDB connection

## File Structure
```
meal-planner/
├── agent.json
├── src/
│   └── index.js
...
```

## Limitations
- Requires internet connection
- Limited to 150 API calls/day
```

### ✅ Good (User Focus)

```markdown
# Meal Planner

## Stop Stressing About Dinner. Start Enjoying It.

This agent plans your meals, creates shopping lists, and even suggests recipes based on what you already have. No more "what's for dinner?" panic.

### ✨ What You Get

- 🍽️ **Weekly meal plans** tailored to your preferences
- 🛒 **Smart shopping lists** organized by store section
- ⏱️ **Quick recipes** for busy weeknights
- 🥗 **Balanced nutrition** without counting calories

## How It Works

Just tell me what you need:

**You:** *"Plan dinners for this week — something healthy but quick"*  
**Agent:** Creates a 7-day plan with 30-minute recipes

**You:** *"I have chicken, broccoli, and rice. What can I make?"*  
**Agent:** Suggests 3 recipes using those ingredients

**You:** *"Make me a shopping list for the meal plan"*  
**Agent:** Organized list ready for your grocery trip

## Ready to Eat Better?

Just say "Plan my meals for this week" and let's get started!
```

See the difference? The good example focuses on **what the user gets**, not how it's built.
