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
    """Generate README.md content."""
    return f"""# {name}

{description}

## What it does

<!-- Describe what this agent does for users -->

## How it works

<!-- Step-by-step description of the interaction flow -->

## File Structure

```
{slug}/
├── agent.json              # Agent metadata
├── README.md               # This file
├── avatar.png              # Agent avatar
├── HelpGuide.md            # Help content for /help command
├── OnBoarding.md           # User setup guide
├── OnBoarding.json         # Onboarding configuration
├── KrabotSpecs.json        # Platform configuration
└── workspace/              # Agent runtime workspace
    ├── AGENTS.md           # Agent behavior and workflows
    ├── BOOTSTRAP.md        # Startup verification
    ├── IDENTITY.md         # Agent identity and tone
    ├── SOUL.md             # Base assistant personality
    ├── Tools.md            # Available tools/skills
    ├── USER.md             # User preferences
    └── skills/             # Skill definitions
```

## Requirements

<!-- List required API keys, accounts, etc. -->

## Limitations

<!-- Document any known limitations -->
"""


def generate_help_guide(name: str) -> str:
    """Generate HelpGuide.md content."""
    return f"""# {name} — Help Guide

## Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show this help message |

<!-- Add your agent's commands here -->

## Getting Started

<!-- Quick start instructions for users -->

## Troubleshooting

<!-- Common issues and solutions -->
"""


ONBOARDING_MD_CONTENT = """# Setup Guide

## Prerequisites

<!-- What the user needs before starting -->

## Configuration Steps

<!-- Step-by-step configuration instructions -->

### Step 1: <!-- First setting -->

### Step 2: <!-- Second setting -->

## Verification

<!-- How to verify the agent is working -->
"""


ONBOARDING_JSON_CONTENT = {"steps": []}


KRABOT_SPECS_CONTENT = {
    "_note": "This file is filled by a platform engineer. Do not edit the template contents below.",
    "dockerImage": "",
    "configTemplate": "",
    "resources": {"cpu": "", "memory": ""},
}


def generate_agents_md(name: str) -> str:
    """Generate AGENTS.md content."""
    return f"""# {name} Agent

You are an AI assistant. <!-- Describe the agent's purpose -->

---

## Core Rules

<!-- List the most important behavioral rules -->

---

## Handling User Requests

<!-- Document the main workflow -->

1. **Parse the request**
2. **Validate inputs**
3. **Execute action**
4. **Return result**

---

## Available Commands

<!-- Document user-facing commands -->

- `/help` — Show help

---

## What You Do Not Do

<!-- List boundaries and restrictions -->
"""


BOOTSTRAP_CONTENT = """# Bootstrap Instructions

You are starting for the first time. Execute these steps in order before doing anything else.

---

## Step 1: Verify configuration

Check that the following environment variables are present and non-empty:
<!-- List required env vars -->

If any are missing, send an error message and stop.

---

## Step 2: Test connectivity

<!-- Steps to verify external services are reachable -->

---

## Step 3: Initialize storage

<!-- Create any required files or databases -->

---

## Step 4: Announce readiness

Send a message indicating the agent is ready to receive requests.

---

## Step 5: Enter normal operation

Begin listening for messages. Apply the behaviour described in AGENTS.md.
"""


def generate_identity_md(name: str) -> str:
    """Generate IDENTITY.md content."""
    return f"""# Identity

**Name:** {name}
**Role:** <!-- Agent's primary role -->
**Tone:** <!-- e.g., Friendly, professional, concise -->
**Language:** <!-- e.g., English, or "Match user's language" -->

## Behaviour Principles

<!-- How the agent should behave -->

## Boundaries

<!-- What the agent does NOT do -->
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


TOOLS_CONTENT = """# Available Tools

<!-- Document each skill/tool available to the agent -->

---

## Example Skill

**Purpose:** What this skill does

**When to use:** When to invoke this skill

### function_name(param1, param2)

Description of what this function does.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | string | yes | Description |
| `param2` | integer | no | Description |

**Returns:**
```
Description of return value
```
"""


USER_CONTENT = """# User

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

    (agent_dir / "KrabotSpecs.json").write_text(
        json.dumps(KRABOT_SPECS_CONTENT, indent=2), encoding="utf-8"
    )

    # Write workspace files
    (workspace_dir / "AGENTS.md").write_text(generate_agents_md(name), encoding="utf-8")

    (workspace_dir / "BOOTSTRAP.md").write_text(BOOTSTRAP_CONTENT, encoding="utf-8")

    (workspace_dir / "IDENTITY.md").write_text(
        generate_identity_md(name), encoding="utf-8"
    )

    (workspace_dir / "SOUL.md").write_text(SOUL_CONTENT, encoding="utf-8")

    (workspace_dir / "Tools.md").write_text(TOOLS_CONTENT, encoding="utf-8")

    (workspace_dir / "USER.md").write_text(USER_CONTENT, encoding="utf-8")

    return agent_dir


def main():
    parser = argparse.ArgumentParser(description="Create a new agent workspace")
    parser.add_argument("--name", required=True, help="Agent display name")
    parser.add_argument(
        "--slug", required=True, help="URL-friendly identifier (lowercase, hyphens)"
    )
    parser.add_argument("--category", default="general", help="Agent category")
    parser.add_argument("--description", default="", help="Short description")
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
            description=args.description or f"{args.name} agent",
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
