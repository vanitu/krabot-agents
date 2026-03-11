# Agent Template Authoring Specification

> **Audience:** AI agents creating new KrabotTemplate repositories.
> This document covers everything you need to know to author a complete, working agent template. You do not need to know anything about Docker, containers, or platform infrastructure — that is handled separately by a platform engineer using `picoclaw_platform_spec.md`.

---

## What Is a KrabotTemplate?

A **KrabotTemplate** is a git repository that describes a specialized AI agent: what it does, what it needs from the customer to work, and how it should behave when it starts. The Krabot platform reads this repository and uses it to:

1. Show customers a catalog card with the agent's name, description, and category.
2. Walk the customer through a setup form to collect credentials and settings.
3. Deliver the agent's working files to the agent process on first start.

You — the template author — are responsible for files 1–3. A platform engineer handles the container and runtime wiring separately.

---

## How a Launched Agent Receives Its Configuration

This is the lifecycle your agent goes through, from template to live:

```
1. Customer fills the onboarding form (driven by OnBoarding.json)
   → Each field they fill in becomes an ENVIRONMENT VARIABLE available to the agent at runtime.
   → Example: a field with key "OZON_API_KEY" → agent reads env var OZON_API_KEY

2. Customer connects their Telegram bot (separate setup step)
   → TELEGRAM_TOKEN becomes available as an env var at runtime.
   → Do NOT include TELEGRAM_TOKEN in OnBoarding.json — it is handled automatically.

3. Agent process starts for the first time
   → The workspace/ directory contents are loaded into the agent's working environment.
   → Agent reads Bootstrap.md and executes its instructions (self-check, announce readiness, first run).

4. Agent enters normal operation
   → Responds to Telegram messages, runs scheduled tasks, etc.
   → All OnBoarding.json field values are readable as env vars throughout the agent's lifetime.
```

**Key rule:** If your agent needs a value at runtime, it must either appear as a field in `OnBoarding.json` (so the customer provides it), or it must be derived from values the agent already has. There is no other way to inject configuration.

---

## Repository Structure

```
template-repo/
├── agent.json          ← Agent manifest: name, slug, category, tags, avatar path
├── avatar.png          ← Agent avatar image (referenced by agent.json)
├── README.md           ← What this agent does (shown to customer before launch)
├── HelpGuide.md        ← How to use the running agent (day-to-day reference)
├── OnBoarding.md       ← Step-by-step human explanation of what the customer must provide
├── OnBoarding.json     ← Machine-readable form schema (drives the setup wizard UI)
├── KrabotSpecs.json    ← Container and runtime config — filled by platform engineer, not you
└── workspace/          ← Agent's working files, delivered on first start
    ├── Agent.md        ← Core agent instructions (who you are, what you do, how you decide)
    ├── Tools.md        ← Tools available to the agent and how to use them
    ├── Identity.md     ← Persona: name, role, tone, language, boundaries
    ├── Bootstrap.md    ← First-start instructions: verify, announce, run
    └── Skills/         ← Pre-loaded skill folders (optional)
        └── <skill_name>/
```

> **`workspace/`** — The `workspace/` directory is the source of truth. There is no need to commit a `workspace.zip` — the platform builds it on the fly from the directory contents when the template is imported or synced.

> **`KrabotSpecs.json`** — you must create this file with the correct filename and valid JSON structure, but its contents are filled by a platform engineer who knows which Docker image and config template to use. Leave it as a placeholder or ask a platform engineer to fill it. See `picoclaw_platform_spec.md` for full details.

---

## `agent.json` — Agent Manifest

The `agent.json` file is the machine-readable manifest for your agent — analogous to `package.json` for NPM or a `.gemspec` for Ruby gems. It contains the catalog metadata that the Krabot platform uses to create a template record automatically from the GitHub repository.

**Where it lives:** `agents/{agent-id}/agent.json` — at the root of your agent folder.

### Schema

```json
{
  "name": "Display Name",
  "slug": "url-friendly-slug",
  "category": "category-name",
  "short_description": "One-sentence description shown on the catalog card.",
  "tags": ["tag1", "tag2"],
  "avatar": "avatar.png",
  "readme": "README.md",
  "help_guide": "HelpGuide.md",
  "onboarding_md": "OnBoarding.md",
  "onboarding_json": "OnBoarding.json",
  "workspace": "workspace"
}
```

### Field Reference

#### Catalog metadata (required)

| Field | Type | Required | Rules |
|---|---|---|---|
| `name` | string | yes | Display name shown in the template catalog |
| `slug` | string | yes | Lowercase letters, numbers, hyphens only — **must match the agent folder name** |
| `category` | string | yes | Category shown in catalog, e.g. `"creative"`, `"e-commerce"`, `"productivity"` |
| `short_description` | string | yes | One sentence, max ~160 characters, shown on catalog cards |
| `tags` | string[] | no | Lowercase strings for search and filtering |
| `avatar` | string | no | Relative path to the avatar image within the agent folder. Default: `"avatar.png"` |

#### File path overrides (optional)

All paths are **relative to the agent folder**. If omitted, the defaults shown below are used. Override only if your files use different names.

| Field | Default | Description |
|---|---|---|
| `readme` | `"README.md"` | Product description page shown before launch |
| `help_guide` | `"HelpGuide.md"` | Day-to-day user guide shown on the krabot page |
| `onboarding_md` | `"OnBoarding.md"` | Human-readable setup instructions |
| `onboarding_json` | `"OnBoarding.json"` | Machine-readable setup form schema |
| `workspace` | `"workspace"` | Directory zipped and delivered to the agent on first start |

> **`slug` must match the folder name.** If the agent folder is `agents/qwen-image-generator`, the slug must be `qwen-image-generator`. This creates a single source of truth.

> **`krabot_specs`** is intentionally not in `agent.json` — it is managed by the admin in the web UI, not by the agent author.

### Example

```json
{
  "name": "Qwen Image Generator",
  "slug": "qwen-image-generator",
  "category": "creative",
  "short_description": "Generate stunning AI images from text descriptions using Alibaba Cloud Wan AI — directly in Telegram.",
  "tags": ["image-generation", "ai", "alibaba-cloud", "wan"],
  "avatar": "avatar.png",
  "readme": "README.md",
  "help_guide": "HelpGuide.md",
  "onboarding_md": "OnBoarding.md",
  "onboarding_json": "OnBoarding.json",
  "workspace": "workspace"
}
```

### Avatar

Commit a square PNG image at the path specified in `agent.json` (e.g. `avatar.png` in the agent folder root). Recommended size: 256×256px.

---

## File Specifications

### README.md

Displayed to the customer on the template detail page **before** they fill the onboarding form. This is the agent's "sales page" — write it for a non-technical business user.

Cover:
- What problem this agent solves
- What it does automatically vs. what requires user action
- Expected outputs, reports, or notifications
- Prerequisites and limitations

```markdown
# OZON Review Assistant

Automatically replies to customer reviews on your OZON Seller account using AI.

## What it does
- Monitors new reviews every N hours (schedule is configurable)
- Drafts polite, on-brand replies using your company rules
- Submits replies to OZON automatically

## Requirements
- An active OZON Seller account
- OZON API credentials (Client ID + API Key)
- A Telegram bot for notifications

## Limitations
- Replies only to 4–5 star reviews by default (configurable)
- Does not handle refund or complaint escalations automatically
```

---

### HelpGuide.md

Shown on the **krabot page** after the agent is active. This is the customer's day-to-day reference once the agent is running.

Cover:
- Telegram commands the agent understands
- How to check status or request reports
- How to adjust settings or rules after launch
- Common troubleshooting tips

```markdown
# OZON Review Assistant — Help Guide

## Telegram Commands
- `/status` — show current agent status and last run time
- `/report` — request a summary of replies sent today
- `/pause` — pause automatic processing
- `/resume` — resume automatic processing

## Adjusting Rules
Send your new company rules as a Telegram message:
> "Update rules: [paste new rules here]"

## Schedule
The agent checks for new reviews at the interval you configured during setup.
To change it, contact support or reconfigure from the settings panel.
```

---

### OnBoarding.md

Plain-language explanation of every credential and setting the customer must provide. This is shown alongside the form during setup.

For each field, explain:
- What it is and why it is needed
- Where the customer can find it (step-by-step)

```markdown
# Setup Guide

## Step 1: OZON API Credentials

**Client ID**
Your numeric seller identifier. Find it at:
OZON Seller → Settings → API → Client ID

**API Key**
A secret key that gives the agent access to your reviews.
OZON Seller → Settings → API → Generate New Key
Assign the "Reviews" permission.

## Step 2: Company Rules (optional)
Paste your brand voice or response style guidelines.
The agent uses these to match your tone. Leave blank for default polite style.

## Step 3: Schedule
How often the agent checks for new reviews. Default: every 4 hours.
```

---

### OnBoarding.json

Machine-readable schema that drives the setup wizard in the Krabot web UI. Each field the customer fills in is stored and made available to the agent as an **environment variable** at runtime.

**⚠️ Never include `TELEGRAM_TOKEN` here.** Telegram setup is a separate step handled automatically.

#### Schema

```json
{
  "steps": [
    {
      "title": "Step title shown in the wizard",
      "description": "Optional subtitle shown under the step title.",
      "fields": [
        {
          "key": "ENV_VAR_NAME",
          "label": "Human-readable label",
          "required": true,
          "secret": false,
          "type": "text",
          "default": "",
          "placeholder": "Example value",
          "hint": "Short help text shown below the input"
        }
      ]
    }
  ]
}
```

#### Field Properties

| Property      | Type      | Required | Description |
|---------------|-----------|----------|-------------|
| `key`         | string    | yes      | The environment variable name your agent reads at runtime. Use SCREAMING_SNAKE_CASE. |
| `label`       | string    | yes      | Human-readable label shown above the input field. |
| `required`    | boolean   | yes      | If `true`, the wizard blocks "Next" until this field has a value. |
| `secret`      | boolean   | no       | If `true`, renders as a password input (value hidden on screen). Default: `false`. |
| `type`        | string    | no       | `"text"` (default), `"textarea"`, `"select"`. |
| `default`     | string    | no       | Pre-filled default value. |
| `placeholder` | string    | no       | Placeholder text inside the input. |
| `hint`        | string    | no       | Short help text rendered below the input. |
| `options`     | string[]  | select only | Option values for `type: "select"`. |

#### Full Example (OZON Reviews)

```json
{
  "steps": [
    {
      "title": "OZON Credentials",
      "description": "Found in OZON Seller → Settings → API.",
      "fields": [
        {
          "key": "OZON_CLIENT_ID",
          "label": "Client ID",
          "required": true,
          "secret": false,
          "type": "text",
          "placeholder": "123456789",
          "hint": "Your numeric seller identifier from OZON Seller settings."
        },
        {
          "key": "OZON_API_KEY",
          "label": "API Key",
          "required": true,
          "secret": true,
          "type": "text",
          "placeholder": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "hint": "Generate at OZON Seller → Settings → API. Assign the 'Reviews' permission."
        }
      ]
    },
    {
      "title": "Company Rules",
      "description": "Optional. Paste your brand voice or response style guidelines.",
      "fields": [
        {
          "key": "COMPANY_RULES",
          "label": "Company rules",
          "required": false,
          "type": "textarea",
          "placeholder": "Be polite. Never offer refunds. Sign replies with 'Team Support'.",
          "hint": "Leave blank to use default professional response style."
        }
      ]
    },
    {
      "title": "Schedule",
      "fields": [
        {
          "key": "CHECK_INTERVAL",
          "label": "Check for new reviews every",
          "required": true,
          "type": "select",
          "options": ["1h", "2h", "4h", "6h", "12h", "24h"],
          "default": "4h"
        }
      ]
    }
  ]
}
```

---

## workspace/ Directory

The workspace is the agent's working directory. It is delivered to the agent on first start and is **frozen after that** — the agent may modify files inside its running workspace, but those changes do not affect the template and are not re-delivered on restart.

**Never put secrets in workspace files.** Workspace files live in git and are visible to anyone with repo access. All credentials come from `OnBoarding.json` fields, which are injected as env vars at runtime.

### workspace/Agent.md

The agent's core operating instructions. Write in first person, as if you are writing a prompt for the agent itself.

Cover:
- What the agent's job is
- What it does autonomously vs. what it escalates to the user
- How it uses each available tool or skill
- Behavioral rules and constraints
- How to reference configurable values (use env var names)

```markdown
# OZON Review Agent

You are an automated OZON marketplace review assistant for a seller.

## Your job
Every ${CHECK_INTERVAL} you:
1. Fetch all unread reviews with rating ≥ ${STAR_LEVEL_TO_REPLY} using the ozon_api skill.
2. For each review, draft a reply following ${COMPANY_RULES} (or default polite style if empty).
3. Submit the reply via ozon_api.
4. Report a summary via the krabot_reporting skill.

## Rules
- Never apologize for product quality unless explicitly stated in COMPANY_RULES.
- Never promise refunds.
- Keep replies under 300 characters.
- If you cannot determine an appropriate reply with high confidence, skip the review and flag it in the report.
```

### workspace/Tools.md

Description of every tool available to the agent. Explain what each tool does and how to use it correctly.

```markdown
# Available Tools

## ozon_api
Interacts with the OZON Seller API using credentials from env vars.
- `ozon_api.get_reviews(status="unread")` — fetch unread reviews
- `ozon_api.submit_reply(review_id, text)` — post a reply to a review

## krabot_reporting
Sends structured job reports back to the Krabot web interface.
- `krabot_reporting.report(summary, details)` — submit a job report
```

### workspace/Identity.md

Defines the agent's persona. This shapes how the agent communicates with the customer.

```markdown
# Identity

**Name:** OZON Review Assistant
**Role:** Automated customer review responder for OZON marketplace sellers
**Tone:** Professional, polite, concise
**Language:** Match the language of the review being replied to (Russian or English)
**Boundaries:**
- Does not discuss topics unrelated to OZON reviews
- Does not make promises about refunds, exchanges, or escalations
- Does not reveal internal API credentials or configuration
```

### workspace/Bootstrap.md

**Required.** Instructions the agent reads and executes **on first start only**, before entering normal operation. Think of this as the agent's startup checklist.

The Bootstrap.md is the mechanism that makes the agent self-initializing: it verifies it has what it needs, announces it is ready, and performs the first action — all without any human intervention.

Cover:
1. **Self-check** — verify required env vars are present and credentials are valid
2. **Announce readiness** — send a Telegram message confirming the agent is live
3. **First action** — perform the first real work (e.g. first data fetch, first scheduled run)
4. **Switch to normal operation** — describe how the agent transitions to its ongoing loop

```markdown
# Bootstrap Instructions

You are starting for the first time. Execute these steps in order before doing anything else.

## Step 1: Verify configuration
Check that the following environment variables are present and non-empty:
- OZON_CLIENT_ID
- OZON_API_KEY
- CHECK_INTERVAL

If any are missing, send a Telegram message:
> "⚠️ OZON Review Agent could not start. Missing configuration: [list missing vars]. Please contact support."
Then stop.

## Step 2: Test OZON credentials
Call ozon_api.get_reviews(limit=1) to verify the credentials work.
If the call fails, send a Telegram message:
> "⚠️ OZON Review Agent could not connect to OZON API. Please check your Client ID and API Key."
Then stop.

## Step 3: Announce readiness
Send a Telegram message:
> "✅ OZON Review Agent is online and ready. I will check for new reviews every CHECK_INTERVAL. Send /help to see available commands."

## Step 4: First run
Immediately perform the first review check (same as normal scheduled operation).
Report results via krabot_reporting.

## Step 5: Enter normal operation
Schedule the next review check for CHECK_INTERVAL from now.
Begin listening for Telegram commands.
```

### workspace/Skills/ (optional)

Pre-loaded skill directories. Each skill folder contains the files the agent needs to use that skill.

```
Skills/
  ozon_api_skill/         ← OZON Seller API integration
  krabot_secrets_skill/   ← Access to agent secrets
  krabot_reporting_skill/ ← Job reporting to Krabot web
```

---

## Environment Variables Available to Your Agent at Runtime

These variables are available as standard environment variables when your agent runs. You do not need to manage how they get there — just use them by name.

| Variable | Source | Description |
|----------|--------|-------------|
| `TELEGRAM_TOKEN` | Automatic (Telegram pairing) | Your Telegram bot token. Do NOT add to OnBoarding.json. |
| _any `key` from OnBoarding.json_ | Customer-provided during onboarding | Available with the exact `key` name you defined. |

**Example:** If your OnBoarding.json has a field with `"key": "OZON_API_KEY"`, then at runtime your agent reads `process.env.OZON_API_KEY` (or equivalent for its runtime).

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Template slug (in Krabot admin) | lowercase, hyphens only | `ozon-reviews` |
| `OnBoarding.json` field keys | SCREAMING_SNAKE_CASE | `OZON_API_KEY` |
| Workspace skill folder names | snake_case | `ozon_api_skill` |

---

## Authoring Checklist

- [ ] `agent.json` — name, slug, category, short_description filled; slug matches folder name; avatar path set
- [ ] `avatar.png` (or referenced image) — square PNG committed to git
- [ ] `README.md` — written for a non-technical business user; covers what the agent does, prerequisites, limitations
- [ ] `HelpGuide.md` — covers Telegram commands, daily usage, how to adjust settings
- [ ] `OnBoarding.md` — step-by-step instructions for every credential/setting; includes where to find each value
- [ ] `OnBoarding.json` — valid JSON; no `TELEGRAM_TOKEN` field; all `key` values SCREAMING_SNAKE_CASE; required fields marked
- [ ] `KrabotSpecs.json` — file exists (contents filled by platform engineer)
- [ ] `workspace/Agent.md` — first-person agent instructions; references env var names for configurable values
- [ ] `workspace/Tools.md` — lists and explains every available tool
- [ ] `workspace/Identity.md` — persona, name, tone, language, boundaries
- [ ] `workspace/Bootstrap.md` — self-check, readiness announcement, first action, transition to normal operation
- [ ] `workspace/Skills/` — pre-loaded skills if the agent needs them
- [ ] No hardcoded secrets in any file — all credentials come from env vars at runtime
- [ ] Workspace files do not rely on being re-delivered after first start

---

## Workflow for Creating a New Template

1. **Start from the business use case** — understand what the customer wants to automate.
2. **List all required external credentials** — every API key, ID, or setting the agent needs. These become `OnBoarding.json` fields.
3. **Write `OnBoarding.md` first** — forces clarity on what the customer must provide and why.
4. **Derive `OnBoarding.json` from `OnBoarding.md`** — each human-facing step becomes one JSON step object.
5. **Write `workspace/Agent.md`** — the agent's core operating prompt, referencing env var names for any configurable behavior.
6. **Write `workspace/Bootstrap.md`** — the agent's startup checklist: verify, announce, first run.
7. **Write `workspace/Identity.md` and `workspace/Tools.md`**.
8. **Write `README.md` and `HelpGuide.md`** for the customer.
9. **Create `KrabotSpecs.json`** as a placeholder — hand off to platform engineer to fill.
