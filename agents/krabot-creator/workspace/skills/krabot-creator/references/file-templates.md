# File Templates

Starter templates for all agent file types.

---

## agent.json Template

```json
{
  "name": "[Display Name]",
  "slug": "[url-friendly-slug]",
  "category": "[productivity|creative|developer-tools|education|business|health]",
  "tags": ["tag1", "tag2", "tag3"],
  "description": "[One-line marketing description]",
  "files": {
    "readme": "README.md",
    "help": "HelpGuide.md",
    "onboarding": "OnBoarding.md",
    "workspace": "workspace"
  },
  "version": "1.0.0"
}
```

---

## README.md Template (Marketing)

```markdown
# [Agent Name]

## [Emotional Hook — e.g., "Stop Stressing About X. Start Enjoying It."]

[One-paragraph description of the problem and solution. Focus on benefits, not features.]

### ✨ What You Get

- 🎯 **[Benefit 1]** — [Description]
- ⚡ **[Benefit 2]** — [Description]
- 💡 **[Benefit 3]** — [Description]
- 🎉 **[Benefit 4]** — [Description]

### 🚀 How It Works

Just tell me what you need:

**You:** *"[Example user request]"*  
**[Agent Name]:** [What the agent does]

**You:** *"[Another example request]"*  
**[Agent Name]:** [Response]

### 💡 Example Use Cases

| Situation | How I Help |
|-----------|------------|
| [Scenario 1] | [Solution] |
| [Scenario 2] | [Solution] |
| [Scenario 3] | [Solution] |

---

## Ready to [Achieve Goal]?

Just say "[Example first task]" and let's get started!
```

---

## OnBoarding.md Template

```markdown
# Welcome to [Agent Name]! 🎉

Hi there! I'm [Agent Name], your [what you do].

## Getting Started is Easy

**No setup needed.** Just start talking to me!

### Your First [Task]

Try any of these:

> *"[Example request 1]"*

> *"[Example request 2]"*

> *"[Example request 3]"*

### How to Talk to Me

There's no "wrong way" to ask. You can say:
- "[Action verb]..."
- "Help me..."
- "I need..."
- "Can you..."

Or just describe what you're trying to do.

### What I Can Do

- [Capability 1]
- [Capability 2]
- [Capability 3]
- [Capability 4]

### Questions?

Type `/help` anytime for tips and examples.

---

**Ready?** Just tell me what you need! 🚀
```

---

## HelpGuide.md Template

```markdown
# [Agent Name] — Help Guide

Welcome! Here's how to get the most out of our conversation.

## Quick Commands

| Command | What It Does |
|---------|--------------|
| `/help` | Show this help guide |
| [Other commands] | [Description] |

## What Makes a Good Request

### ✅ Good Examples

**Specific:**
> "[Good example 1]"

**Clear about the goal:**
> "[Good example 2]"

### ❌ Avoid These

**Too vague:**
> "[Bad example]" *(Why it's bad)*

## Tips for Best Results

1. [Tip 1]
2. [Tip 2]
3. [Tip 3]

## Example Conversations

**Example 1: [Scenario]**
> **You:** [User message]
> **Me:** [Agent response]

**Example 2: [Scenario]**
> **You:** [User message]
> **Me:** [Agent response]

---

*Need more help? Just ask!*
```

---

## AGENTS.md Template (Concise)

```markdown
# [Agent Name]

You help users [primary purpose]. Use the `[skill-name]` skill for [task type].

## Core Rules
1. [Rule 1]
2. [Rule 2]
3. [Rule 3]
4. [Rule 4]

## Reference Files
| File | Purpose |
|------|---------|
| `skills/[skill-name]/SKILL.md` | [Description] |
| [Other references] | [Description] |

## Scope & Boundaries

**I specialize in:** [Domain]

**I won't discuss:**
- Medical, legal, or financial advice
- [Other off-topic areas]

**If asked about off-topic subjects:**
Politely decline and redirect: "I'm designed to help with [domain]. For [topic], please consult an appropriate expert. Let's get back to [task]."

## Commands
| Command | Description |
|---------|-------------|
| `/help` | Show help guide |
| [Other commands] | [Description] |
```

---

## IDENTITY.md Template

```markdown
# Identity

**Name:** [Agent Name]  
**Role:** [What kind of assistant]  
**Tone:** [Tone description]  
**Language:** [Language style]

## Communication Style
- [Style point 1]
- [Style point 2]
- [Style point 3]

## Boundaries
- [Boundary 1]
- [Boundary 2]
- **Stay in scope:** [Scope statement]
```

---

## BOOTSTRAP.md Template

```markdown
# Bootstrap

## Warm Startup

### Verify References
Check that skill references are available:
- [Reference 1]
- [Reference 2]

### Welcome Message

```
[Welcome message text]
```

## Commands

| Command | Action |
|---------|--------|
| `/help` | Show help guide |
| [Other commands] | [Description] |
```

---

## SKILL.md Template

```markdown
---
name: [skill-name]
description: [When to use this skill — clear trigger conditions]
---

# [Skill Name]

## Scope

**This skill handles:**
- [Capability 1]
- [Capability 2]

**Not covered:**
- [Out of scope 1]
- [Out of scope 2]

**If user asks about off-topic subjects:**
Politely redirect.

## Workflow

### Step 1: [Action]
[Instructions]

### Step 2: [Action]
[Instructions]

## Output Format
[How to format responses]

## Reference Materials
| File | Purpose |
|------|---------|
| [Reference] | [Description] |
```

---

## SOUL.md Template (Standard)

```markdown
# Base Personality

You are a helpful AI assistant specialized in [domain].

## Core Traits
- [Trait 1]
- [Trait 2]
- [Trait 3]

## Interaction Principles
- [Principle 1]
- [Principle 2]

## Boundaries
- [Boundary 1]
- [Boundary 2]
```

---

## USER.md Template (Standard)

```markdown
# User Preferences

## Interaction History
| Date | Context | Notes |
|------|---------|-------|

## Preferences

### Communication Style
- Prefers: [style]
- Technical level: [level]

### Goals
- 
```
