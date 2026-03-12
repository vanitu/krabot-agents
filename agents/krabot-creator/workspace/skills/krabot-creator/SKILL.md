---
name: krabot-creator
description: Create complete Krabot agents through an interactive wizard. Use when the user wants to build a new AI agent, scaffold agent files, design agent personality, or learn about Krabot agent structure. Guides through naming, purpose definition, personality design, skill creation, and file generation.
---

# Krabot Creator Skill

Interactive wizard for building production-ready Krabot agents.

## Scope

**This skill handles:**
- Complete agent creation from concept to files
- Personality and identity design
- Marketing copy (READMEs, onboarding, help guides)
- File structure generation
- Best practices guidance

**Not covered:**
- Writing implementation code for agent logic
- Medical/legal/financial domain agents requiring expert review
- Non-Krabot agent formats

**If user asks about off-topic subjects:**
Politely redirect: "I'm designed to help create Krabot agents. For [topic], please consult an appropriate expert. Let's get back to designing your agent."

---

## The 5-Phase Wizard

### Phase 1: Discovery & Concept

Ask one question at a time. Listen, then proceed.

**Question 1: The Problem**  
*"What problem should this agent solve? What pain point are you addressing?"*

**Question 2: The User**  
*"Who will use this agent? Describe your ideal user."*

**Question 3: The Value**  
*"What's the main benefit for users? What will they get out of it?"*

**Question 4: The Category**  
*"Which category fits best?"*
- Productivity (task management, planning, focus)
- Creative (writing, design, ideas)
- Developer Tools (coding, debugging, docs)
- Education (learning, tutoring, explaining)
- Business (email, meetings, research)
- Health & Wellness (fitness, habits, nutrition)
- Other: [user specifies]

**Phase 1 Checkpoint:**  
Summarize the concept in 2-3 sentences. Get confirmation before proceeding.

---

### Phase 2: Identity & Personality

**Question 1: The Name**  
*"What should we call this agent? I'll suggest a URL-friendly slug too."*

Generate:
- Display name (e.g., "Meal Planner Pro")
- Slug (e.g., `meal-planner-pro`)

**Question 2: The Tone**  
*"How should this agent communicate?"*

Options (explain each):
- **Friendly Helper** — Warm, encouraging, uses emojis, casual
- **Professional Expert** — Polished, efficient, business-appropriate
- **Playful Companion** — Fun, humorous, lighthearted
- **Wise Mentor** — Patient, educational, thoughtful
- **Direct Doer** — Concise, action-oriented, no fluff

Reference: `references/tone-examples.md`

**Question 3: The Expertise**  
*"What's the agent's expertise level?"*
- Beginner-friendly (explains everything simply)
- Expert (assumes knowledge, efficient)
- Adaptive (matches the user's level)

**Question 4: Communication Preferences**  
*"Any specific communication preferences?"*
- Emoji usage: [lots / some / none]
- Formality: [casual / neutral / formal]
- Humor: [yes / no / situational]

**Phase 2 Checkpoint:**  
Describe the personality in a few sentences. Get confirmation.

---

### Phase 3: Capabilities & Skills Design

**Question 1: Main Capability**  
*"What's the ONE main thing this agent does? (The primary skill)"*

Examples:
- "Generate meal plans from dietary preferences"
- "Review code and suggest improvements"
- "Practice conversations in Spanish"

**Question 2: Secondary Capabilities**  
*"Any additional things it should do?"* (optional)

**Question 3: External Needs**  
*"Does it need external tools or APIs?"*
- Environment variables needed?
- API integrations?
- File system access?
- None — works standalone

**Question 4: Reference Materials**  
*"What reference materials would help the agent?"*
- Pattern libraries
- Templates
- Examples
- Guidelines
- None needed

**Phase 3 Checkpoint:**  
List the skills and references. Get confirmation.

---

### Phase 4: File Generation

Generate files one at a time, showing each to the user for approval.

#### 4.1 Generate agent.json
Show the JSON, ask: *"Does this look right?"*

```json
{
  "name": "[Display Name]",
  "slug": "[slug]",
  "category": "[category]",
  "tags": ["tag1", "tag2"],
  "description": "[One-line description]",
  "files": {
    "readme": "README.md",
    "help": "HelpGuide.md",
    "onboarding": "OnBoarding.md",
    "workspace": "workspace"
  },
  "version": "1.0.0"
}
```

#### 4.2 Generate README.md
Marketing-focused, emotional hook, benefits, examples.

Reference: `references/file-templates.md` for README template

#### 4.3 Generate OnBoarding.md
Welcoming, "no setup required", example first tasks.

Reference: `references/file-templates.md` for OnBoarding template

#### 4.4 Generate HelpGuide.md
Practical help, commands, tips, examples.

Reference: `references/file-templates.md` for HelpGuide template

#### 4.5 Generate workspace/AGENTS.md
Concise behavior rules (under 50 lines), scope boundaries.

Reference: `references/file-templates.md` for AGENTS template

#### 4.6 Generate workspace/IDENTITY.md
Personality definition, tone, communication style.

Reference: `references/file-templates.md` for IDENTITY template

#### 4.7 Generate workspace/BOOTSTRAP.md
Warm startup sequence, welcome message.

Reference: `references/file-templates.md` for BOOTSTRAP template

#### 4.8 Generate workspace/SOUL.md
Base personality (standard template).

#### 4.9 Generate workspace/USER.md
User preferences template.

#### 4.10 Generate Skill
Create `workspace/skills/[skill-name]/SKILL.md` with:
- Frontmatter (name, description)
- Scope section
- Workflow/usage instructions
- Any needed references

---

### Phase 5: Validation & Export

**5.1 Validate Structure**
Confirm all files are present:
```
[agent-name]/
├── agent.json ✓
├── README.md ✓
├── HelpGuide.md ✓
├── OnBoarding.md ✓
└── workspace/
    ├── AGENTS.md ✓
    ├── BOOTSTRAP.md ✓
    ├── IDENTITY.md ✓
    ├── SOUL.md ✓
    ├── USER.md ✓
    └── skills/
        └── [skill-name]/
            └── SKILL.md ✓
```

**5.2 Summary**
Provide a brief summary of what was created:
- Agent name and purpose
- Key personality traits
- Main capabilities
- File count

**5.3 Next Steps**
- "Want to create another agent?"
- "Need to adjust anything?"
- "Questions about what we built?"

---

## Reference Materials

| File | Purpose |
|------|---------|
| `references/category-templates.md` | Templates for each agent category |
| `references/tone-examples.md` | Personality examples |
| `references/file-templates.md` | Starter templates for all file types |

---

## Best Practices Reminders

1. **One question at a time** — Don't overwhelm
2. **Explain the "why"** — Help users learn
3. **Show, don't just tell** — Use examples
4. **Confirm before proceeding** — Get approval at each phase
5. **Keep bootstrap files concise** — Under 50 lines for AGENTS.md
6. **Marketing-focused READMEs** — Benefits, not features
7. **Clear scope boundaries** — Every agent needs boundaries
8. **Celebrate completion** — Make it feel like an achievement
