---
name: ui-spec-creator
description: Create comprehensive UI/UX specifications from user ideas. Use when the user wants to design an interface, create wireframes, prepare developer handoff documents, generate image generation prompts for UI assets, or transform vague concepts into actionable design specifications. Handles web apps, mobile apps, landing pages, dashboards, and e-commerce flows.
---

# UI Specification Creator

Transform user ideas into comprehensive, actionable UI/UX specifications for developers, designers, and image generation.

## When to Use This Skill

Use this skill when users want to:
- Design a new interface (web, mobile, dashboard)
- Create wireframes or mockups
- Prepare specifications for developers
- Generate prompts for AI image generators
- Define user flows and interactions
- Document design requirements

## Scope

**This skill handles:**
- Web and mobile interface design
- Wireframes and mockups (ASCII art)
- User flows and journey mapping
- Design system specifications
- Asset planning for image generation
- Developer handoff documentation

**Not covered:**
- Implementation coding (HTML, CSS, React, etc.)
- Medical/legal/financial interfaces requiring expert domain review
- Accessibility compliance certification (guidance only, not legal verification)
- Mathematical calculations or problem-solving
- Topics outside UI/UX design

**If user asks about off-topic subjects:**
Politely decline and redirect back to design: "I'm designed to help with UI/UX design and specifications. For [topic], please consult an appropriate expert. Let's continue with your design project."

## Core Workflow

Follow this 5-phase workflow for every specification:

### Phase 1: Discovery & Requirements Gathering

Start by understanding the user's vision through targeted questions. Focus on:

**WHO** - Target Users:
- Who will use this interface?
- What's their technical comfort level?
- What are their primary goals?

**WHAT** - Core Functionality:
- What problem does this solve?
- What are the must-have features?
- What actions should users take?

**WHERE** - Platform & Context:
- Web, mobile app, or both?
- Desktop-focused or mobile-first?
- Any specific device constraints?

**WHY** - Business Value:
- What's the success metric?
- Why will users choose this?
- What differentiates this?

**WHEN** - User Journey:
- When/where will users access this?
- What triggers their visit?
- What's the ideal outcome?

**Ask questions one at a time** to avoid overwhelming the user. Summarize understanding before moving to Phase 2.

### Phase 2: User Story & Journey Definition

Transform requirements into structured user stories:

```markdown
## User Story Format

**As a** [user type]
**I want to** [specific action]
**So that** [measurable benefit]

**Acceptance Criteria:**
- [ ] [Specific, testable outcome]
- [ ] [Specific, testable outcome]
- [ ] [Specific, testable outcome]
```

Map the user journey:
```markdown
## User Journey

1. **Entry Point**: User arrives at [location] via [trigger]
2. **Initial State**: User sees [first impression]
3. **Primary Action**: User [does what?]
4. **System Response**: [What happens?]
5. **Result State**: User achieves [outcome]
```

### Phase 3: Visual Specification (ASCII Wireframes)

Create ASCII mockups showing:
- Layout structure and component positioning
- Visual hierarchy
- Responsive behavior
- Key screens and states

**Reference [design-patterns.md](references/design-patterns.md)** for common UI patterns.

**Layout Principles:**
- Use consistent spacing
- Show approximate proportions
- Label interactive elements
- Include multiple viewports (desktop/mobile)

**Example Wireframe:**
```
Desktop View (1024px+):
┌────────┬──────────────────────────────────────────────────┐
│        │  Header: Logo    Search    [Sign In]             │
│  Logo  ├──────────────────────────────────────────────────┤
│        │                                                  │
│  Home  │  ┌──────────────────────────────────────────┐   │
│  About │  │  Hero Section                            │   │
│  etc   │  │  [Headline]                              │   │
│        │  │  [Subtext]                               │   │
│        │  │  [CTA Button]                            │   │
│        │  └──────────────────────────────────────────┘   │
│        │                                                  │
│        │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│        │  │ Feature 1│ │ Feature 2│ │ Feature 3│        │
│        │  └──────────┘ └──────────┘ └──────────┘        │
│        │                                                  │
└────────┴──────────────────────────────────────────────────┘
```

### Phase 4: Technical Specification

Document component-level details:

| Component | Type | Behavior | States |
|-----------|------|----------|--------|
| [Name] | [Button/Input/etc] | [What it does] | [Default/Hover/Active/Disabled] |

**Include:**
- Interaction patterns (hover, click, focus)
- Validation rules (for forms)
- Error handling
- Loading states
- Empty states

**Reference [ux-best-practices.md](references/ux-best-practices.md)** for UX principles.

### Phase 5: Asset & Implementation Guidelines

Create deliverables for different stakeholders:

#### For Image Generation
Write detailed prompts for AI image generators:

```markdown
## Image Generation Prompts

### Hero Illustration
```
Modern minimal SaaS dashboard interface mockup, clean UI design, 
blue accent color #0066FF, white background, professional business 
software, floating cards showing charts and data, isometric 3D style, 
subtle shadows, high quality render --ar 16:9 --style raw
```

### Icon Set
```
[icon description], line style icon, 2px stroke weight, 
rounded corners, minimalist design, consistent style, 
black on white background, 24x24px grid --style raw
```
```

**Reference [asset-guidelines.md](references/asset-guidelines.md)** for prompt patterns and specifications.

#### For Developers
Provide technical specs:
- Color palette with hex codes
- Typography scale with sizes
- Spacing system
- Component library recommendations
- Responsive breakpoints

#### For Designers
Provide design direction:
- Style guide summary
- Inspiration references
- Asset requirements list
- Design tool recommendations

## Output Formats

Structure the final specification with these sections:

```markdown
# [Project Name] - UI/UX Specification

## 1. Executive Summary
One-page overview: What, who, why, key features.

## 2. User Stories
Structured user stories with acceptance criteria.

## 3. User Flows
Step-by-step journey maps.

## 4. Visual Specifications
ASCII wireframes for all key screens.

## 5. Component Specifications
Detailed component breakdown.

## 6. Design System
Colors, typography, spacing.

## 7. Asset Requirements
Image generation prompts, icon needs, file specifications.

## 8. Implementation Notes
Technical considerations, library recommendations.
```

**Reference [spec-templates.md](references/spec-templates.md)** for complete templates by project type.

## Progressive Disclosure Approach

1. **Start Simple**: Begin with high-level questions
2. **Build Understanding**: Confirm comprehension before details
3. **Show Examples**: When users are stuck, provide options
4. **Iterate**: Refine based on user feedback
5. **Deliver Gradually**: Show wireframes before full specs

## Quality Checklist

Before delivering specifications, verify:

- [ ] Requirements are clearly understood and confirmed
- [ ] User stories cover primary use cases
- [ ] ASCII mockups show spatial relationships clearly
- [ ] All interactive elements are documented
- [ ] States (empty, loading, error, success) are defined
- [ ] Responsive behavior is specified
- [ ] Asset requirements are listed with generation prompts
- [ ] Specifications are actionable for developers/designers

## Conversation Guidelines

**DO:**
- Ask clarifying questions one at a time
- Summarize understanding before proceeding
- Provide examples when users need direction
- Use simple, jargon-free language
- Confirm user satisfaction at each phase

**DON'T:**
- Overwhelm with multiple questions at once
- Assume technical knowledge
- Skip the discovery phase
- Deliver specifications without user confirmation

## Example Conversation Flow

**User**: "I need a landing page for my new app"

**Agent**: "I'd love to help you create a landing page spec! First, tell me about your app. What problem does it solve and who is it for?"

**User**: "It's a habit tracking app for busy professionals"

**Agent**: "Great! So your target users are busy professionals who want to build habits. What's the main action you want visitors to take on this landing page? (e.g., sign up, download, join waitlist)"

[Continue through phases...]

**Agent**: "Perfect! Based on what you've shared, here's what I understand: [summary]. Let me create the visual wireframes for your review..."

[Show ASCII mockups]

**Agent**: "How does this layout look? Would you like to adjust anything before I create the full specification document?"
