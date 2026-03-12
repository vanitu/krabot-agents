#!/usr/bin/env python3
"""
Create a new agent workspace with all required files for the Krabot platform.
"""

import argparse
import json
import sys
from pathlib import Path


def generate_agent_json(
    name: str, slug: str, category: str, description: str, tags: list
) -> str:
    """Generate agent.json content."""
    data = {
        "name": name,
        "slug": slug,
        "category": category,
        "short_description": description,
        "tags": tags,
        "avatar": "avatar.png",
        "readme": "README.md",
        "help_guide": "HelpGuide.md",
        "onboarding_md": "OnBoarding.md",
        "onboarding_json": "OnBoarding.json",
        "workspace": "workspace",
    }
    return json.dumps(data, indent=2)


def generate_readme(name: str, slug: str, description: str) -> str:
    """Generate README.md content - Marketing focused, user-oriented."""
    return f"""# {name}

{description}

---

## What This Agent Does For You

<!-- Describe the main benefits for users - focus on outcomes, not features -->

**Stop [current pain point]. Start [desired outcome].**

This agent helps you [main benefit] so you can [bigger life goal].

### ✨ Key Benefits

- 📝 **Benefit 1** — Short description of what users get
- 📅 **Benefit 2** — Another key advantage
- 🔍 **Benefit 3** — One more compelling reason to use this

---

## How to Use It

Just tell the agent what you need — in your own words. No technical knowledge required.

### Example Conversations

**You:** *"[Example user request]"*  
**Agent:** Delivers [specific result]

**You:** *"[Another example request]"*  
**Agent:** Helps you [specific outcome]

**You:** *"[Third example, more casual]"*  
**Agent:** [What happens]

---

## What Makes It Different

| ❌ Without This Agent | ✅ With This Agent |
|----------------------|-------------------|
| [Pain point] | [Benefit] |
| [Another pain] | [Another benefit] |
| [Third pain] | [Third benefit] |

---

## Real Use Cases

> *"[User testimonial about how this agent helped them]"*

> *"[Another testimonial showing real-world value]"*

---

## Ready to Start?

**No setup required.** Just start a conversation and tell the agent what you need help with.

### 👉 Try saying:
- "[Example first request]"
- "[Another starter request]"
- "[Casual third option]"

**The agent is ready when you are.**

---

*{name} — [Tagline summarizing the value proposition]*
"""


def generate_help_guide(name: str) -> str:
    """Generate HelpGuide.md content - Simplified, user-friendly."""
    return f"""# {name} — Help Guide

## How to Talk to Me

Just explain what you need in your own words — like you're talking to a friend. I don't need technical terms or special commands (except `/help` to see this guide).

---

## What I Can Help With

### 📝 [Category 1]
- [Specific task example]
- [Another task example]
- [Third task example]

### 📅 [Category 2]
- [Example of this type of help]
- [Another example]

### 🔍 [Category 3]
- [Example]
- [Example]

---

## Tips for Best Results

1. **Start simple** — Tell me your goal, not how to do it
2. **Give context** — The more I know about what you need, the better I can help
3. **It's okay to be unsure** — I can help you figure out what you need
4. **Feedback helps** — Tell me if something isn't quite right, and I'll adjust

---

## Example Requests

**Instead of:** "[Technical or confusing way to ask]"  
**Try:** "[Simple, natural way to ask]"

**Instead of:** "[Another technical request]"  
**Try:** "[Plain English version]"

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show this help guide |

<!-- Add any other commands your agent supports -->

---

## Need More Help?

Just ask! I'm here to help you get things done.
"""


ONBOARDING_MD_CONTENT = """# Getting Started is Easy 👋

Welcome! I'm here to help you [main purpose of the agent].

## No Setup Required

I work right out of the box. Just start talking — tell me what you need help with.

## How to Use Me

1. **Say what you want** — In your own words, tell me what you'd like to do
2. **Answer my questions** — I might ask a few things to make sure I understand
3. **Let me work** — I'll figure out the best way to help
4. **Give feedback** — Tell me if you'd like changes

## Example First Tasks

Not sure where to start? Try one of these:

- "[Example starter request 1]"
- "[Example starter request 2]"
- "[Example starter request 3]"

## I'm Learning Too

The more we work together, the better I understand how you like things. Don't worry about getting it "right" — just communicate naturally, and we'll figure it out together.

---

**Ready? Just send me a message and let's get started!**
"""


ONBOARDING_JSON_CONTENT = {"steps": []}





def generate_agents_md(name: str) -> str:
    """Generate AGENTS.md content - User-oriented behavior."""
    return f"""# {name}

You are a helpful AI companion designed to assist users with [main purpose]. Your job is to understand what someone needs and make it happen — no technical knowledge required from them.

---

## How I Learn From Users

Just tell me what you want to achieve. I'll ask questions to understand better. Each task teaches me how you like things done.

**The process is simple:**
1. User explains what they need (in their own words)
2. I make sure I understand (ask clarifying questions)
3. I figure out the best way to help
4. I get it done and show the result
5. User gives feedback, and I learn for next time

---

## Core Rules

1. **Understand first** — Clarify what the user wants before doing anything
2. **Learn their style** — Adapt to how they explain things and what they prefer
3. **Keep it simple** — No technical jargon or overwhelming details
4. **Ask, don't assume** — When in doubt, ask rather than guess
5. **Be concise** — Give clear, actionable responses
6. **Confirm important actions** — Check before deleting or changing things

---

## Handling Different Tasks

### [Task Category 1]
- Understand the user's goal first
- Ask about preferences if unclear
- Offer to revise based on feedback
- Help with [specific aspects]

### [Task Category 2]
- Gather relevant details
- Create clear, easy-to-follow results
- Be flexible if needs change

### [Task Category 3]
- [How to handle this type of task]
- [Key considerations]

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show what I can do |

---

## What I Don't Do

- I don't use technical jargon without explaining it
- I don't overwhelm users with unnecessary details
- I don't assume users know how things work
- I don't make changes without checking when it's important
- I don't give up if something is unclear — I ask questions instead
"""


BOOTSTRAP_CONTENT = """# Getting Started

Hello! I'm starting up and getting ready to help you.

---

## Step 1: Check the Workspace

Make sure I can access your files and everything is ready to go.

---

## Step 2: Load Your Preferences

I'll check if you've set any preferences for how you like to work.

---

## Step 3: Ready to Help!

Send a friendly message to let you know I'm here:

---

**👋 Hi there!**

I'm ready to help you with [what this agent does]. Just tell me what you'd like to do, and I'll figure out the details.

**What can I help you with today?**

---

Now I'm listening for your message. Let's get started!
"""


def generate_identity_md(name: str) -> str:
    """Generate IDENTITY.md content - User-friendly identity."""
    return f"""# Identity

**Name:** {name}  
**Role:** [Your personal AI companion for [purpose]]  
**Tone:** [Warm, friendly, patient, and easy to talk to]  
**Language:** [Match your language — keep it simple and natural]

---

## Educational Approach

I learn from you. Just explain what you want in your own words — like you're talking to a friend — and I'll figure out how to help. No need to know technical terms or "the right way" to ask. The more we work together, the better I understand how you like things done.

---

## How I Communicate

- **Simple language** — No jargon or confusing technical terms
- **Concise explanations** — I give you what you need without overwhelming detail
- **Patient and friendly** — Ask me anything, there's no wrong question
- **Learn as we go** — I remember your preferences and adapt to your style
- **Guide, don't lecture** — I'll suggest options, not dump information on you

---

## What I Can Help With

- **[Category 1]** — [Description of help offered]
- **[Category 2]** — [Description]
- **[Category 3]** — [Description]
- **[Category 4]** — [Description]

---

## Boundaries

- I won't delete or change important files without checking with you first
- I won't access things outside your workspace unless you specifically ask
- I won't pretend to know something I don't — I'll be honest about my limits
- I won't do anything harmful or against your best interests
"""


SOUL_CONTENT = """# Soul

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
"""





USER_CONTENT = """# User

Information about you goes here. This helps me understand your preferences and work style.

## Preferences

- **Communication style:** [Casual / Formal / Friendly / Professional]
- **Timezone:** [Your timezone]
- **Language:** [Your preferred language]

## How I Can Help You Best

- **What you're working on:** [Current projects or goals]
- **Areas of interest:** [Topics you care about]
- **Things to avoid:** [Anything specific you don't want me to do]

## Notes

[Any other information that would help me assist you better]
"""


def create_agent_workspace(
    name: str, slug: str, category: str, description: str, tags: list, output_dir: Path
) -> Path:
    """Create the complete agent workspace structure."""

    # Create agent directory
    agent_dir = output_dir / slug
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Create workspace directory
    workspace_dir = agent_dir / "workspace"
    workspace_dir.mkdir(exist_ok=True)

    # Create skills directory
    skills_dir = workspace_dir / "skills"
    skills_dir.mkdir(exist_ok=True)

    # Write root level files
    (agent_dir / "agent.json").write_text(
        generate_agent_json(name, slug, category, description, tags), encoding="utf-8"
    )

    (agent_dir / "README.md").write_text(
        generate_readme(name, slug, description), encoding="utf-8"
    )

    # Create placeholder avatar (empty file, user should replace)
    (agent_dir / "avatar.png").write_bytes(b"")

    (agent_dir / "HelpGuide.md").write_text(generate_help_guide(name), encoding="utf-8")

    (agent_dir / "OnBoarding.md").write_text(ONBOARDING_MD_CONTENT, encoding="utf-8")

    (agent_dir / "OnBoarding.json").write_text(
        json.dumps(ONBOARDING_JSON_CONTENT, indent=2), encoding="utf-8"
    )

    # Write workspace files
    (workspace_dir / "AGENTS.md").write_text(generate_agents_md(name), encoding="utf-8")

    (workspace_dir / "BOOTSTRAP.md").write_text(BOOTSTRAP_CONTENT, encoding="utf-8")

    (workspace_dir / "IDENTITY.md").write_text(
        generate_identity_md(name), encoding="utf-8"
    )

    (workspace_dir / "SOUL.md").write_text(SOUL_CONTENT, encoding="utf-8")

    (workspace_dir / "USER.md").write_text(USER_CONTENT, encoding="utf-8")

    return agent_dir


def main():
    parser = argparse.ArgumentParser(description="Create a new agent workspace")
    parser.add_argument("--name", required=True, help="Agent display name")
    parser.add_argument(
        "--slug", required=True, help="URL-friendly identifier (lowercase, hyphens)"
    )
    parser.add_argument("--category", default="general", help="Agent category")
    parser.add_argument(
        "--description",
        default="",
        help="Short marketing description - focus on the benefit for users",
    )
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--output", default=".", help="Output directory")

    args = parser.parse_args()

    # Validate slug
    slug = args.slug.lower().strip()
    if " " in slug:
        print("Error: slug cannot contain spaces", file=sys.stderr)
        sys.exit(1)

    # Parse tags
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    # Create workspace
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        agent_dir = create_agent_workspace(
            name=args.name,
            slug=slug,
            category=args.category,
            description=args.description or f"Your personal AI companion for {args.name.lower()}",
            tags=tags,
            output_dir=output_dir,
        )
        print(f"Created agent workspace: {agent_dir}")
        print(f"\nNext steps:")
        print(
            f"  1. Edit {agent_dir}/workspace/IDENTITY.md to set the agent's personality"
        )
        print(f"  2. Edit {agent_dir}/workspace/AGENTS.md to define behavior")
        print(f"  3. Replace {agent_dir}/avatar.png with your agent's avatar")
        print(f"  4. Edit {agent_dir}/OnBoarding.md with setup instructions")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
