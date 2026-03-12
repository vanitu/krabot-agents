# Specification Output Templates

Templates for different types of UI/UX specifications.

## Template: Web Application

### 1. Executive Summary
```markdown
# [Project Name] - UI/UX Specification

## Overview
Brief description of what this application does and who it's for.

## Target Users
- Primary: [User type and their goals]
- Secondary: [Other user types]

## Key Features
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

## Platform
- Web application (responsive)
- Minimum supported resolution: 320px width
- Browsers: Chrome, Firefox, Safari, Edge (latest 2 versions)
```

### 2. User Stories
```markdown
## User Stories

### Story 1: [Action Name]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Story 2: [Action Name]
...
```

### 3. Information Architecture
```markdown
## Site Structure

```
Home
├── Dashboard
│   ├── Overview
│   ├── Analytics
│   └── Reports
├── Projects
│   ├── List View
│   ├── Grid View
│   └── Detail View
├── Settings
│   ├── Profile
│   ├── Notifications
│   └── Billing
└── Help
    ├── Documentation
    ├── FAQs
    └── Contact Support
```
```

### 4. Page Specifications
```markdown
## Page: [Page Name]

### Purpose
What this page does and why users visit it.

### Layout
[ASCII wireframe showing layout]

### Components
| Component | Type | Behavior |
|-----------|------|----------|
| Header | Navigation | Fixed position, shows user menu |
| Sidebar | Navigation | Collapsible on mobile |
| Data Table | Data display | Sortable, paginated, 10 rows default |
| Search | Input | Real-time filtering |

### Interactions
1. User clicks [element] → [result]
2. User hovers [element] → [result]
3. Form submission → [validation] → [result]

### States
- **Empty**: Show illustration + CTA
- **Loading**: Skeleton screens
- **Error**: Inline error message
- **Success**: Toast notification
```

### 5. Design Specifications
```markdown
## Design System

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| primary | #0066FF | Buttons, links, active states |
| secondary | #6B7280 | Secondary buttons, muted text |
| success | #10B981 | Success states, confirmations |
| warning | #F59E0B | Warnings, attention |
| error | #EF4444 | Errors, destructive actions |
| background | #FFFFFF | Main background |
| surface | #F9FAFB | Cards, elevated surfaces |

### Typography
| Level | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| H1 | System | 32px | Bold | Page titles |
| H2 | System | 24px | Semibold | Section headers |
| H3 | System | 18px | Semibold | Card titles |
| Body | System | 16px | Regular | Main text |
| Small | System | 14px | Regular | Secondary text |
| Caption | System | 12px | Regular | Labels, metadata |

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing |
| sm | 8px | Related elements |
| md | 16px | Default spacing |
| lg | 24px | Section separation |
| xl | 32px | Major sections |
| 2xl | 48px | Page sections |

### Elevation (Shadows)
| Level | Value | Usage |
|-------|-------|-------|
| none | none | Flat elements |
| sm | 0 1px 2px rgba(0,0,0,0.05) | Cards |
| md | 0 4px 6px rgba(0,0,0,0.1) | Dropdowns |
| lg | 0 10px 15px rgba(0,0,0,0.1) | Modals |
```

---

## Template: Mobile App

### 1. Executive Summary
```markdown
# [App Name] - Mobile UI/UX Specification

## Overview
Brief app description and value proposition.

## Target Platforms
- iOS (iPhone): iOS 15+
- Android: API Level 26+
- Tablet support: Yes/No

## Core User Flows
1. Onboarding → Registration → Home
2. Home → [Feature] → Completion
3. Settings → Profile → Edit
```

### 2. Screen Specifications
```markdown
## Screen: [Screen Name]

### Screen Purpose
What users do on this screen.

### Layout (Mobile Portrait)
```
┌────────────────────────────┐
│ Status Bar                 │
├────────────────────────────┤
│ Navigation Bar             │
├────────────────────────────┤
│                            │
│     Screen Content         │
│                            │
│                            │
│                            │
│                            │
│                            │
│                            │
│                            │
├────────────────────────────┤
│ Tab Bar (if applicable)    │
│ [Home][Search][Profile]    │
└────────────────────────────┘
```

### iOS Specifics
- Use system navigation bar
- Follow iOS Human Interface Guidelines
- Support Dynamic Type
- Handle notch/safe areas

### Android Specifics
- Use Material Design 3
- Support edge-to-edge
- Handle system bars
- Support different densities

### Gestures
| Gesture | Action |
|---------|--------|
| Pull down | Refresh |
| Swipe left | Delete/Archive |
| Long press | Context menu |
| Pinch | Zoom (if applicable) |
```

### 3. Navigation Structure
```markdown
## Navigation

### Primary Navigation (Tab Bar)
- Home (active icon: house.fill)
- Search (active icon: magnifyingglass)
- Create (center button, +)
- Notifications (active icon: bell.fill)
- Profile (active icon: person.fill)

### Secondary Navigation
- Settings: Profile → Gear icon
- Help: Profile → Question mark

### Deep Linking
| Route | Screen |
|-------|--------|
| /item/:id | Item Detail |
| /user/:id | User Profile |
| /settings/notifications | Notification Settings |
```

---

## Template: Landing Page

### 1. Executive Summary
```markdown
# [Product Name] - Landing Page Specification

## Goal
Primary conversion goal (signups, sales, downloads).

## Target Audience
- Demographics: [Age, location, profession]
- Pain points: [What problem they have]
- Motivations: [Why they need this solution]

## Key Messages
1. Primary headline value proposition
2. Secondary supporting message
3. Social proof elements
4. Call-to-action
```

### 2. Section Specifications
```markdown
## Sections (Top to Bottom)

### 1. Hero Section
**Purpose**: Grab attention and communicate value

**Elements**:
- Headline (H1): [Text]
- Subheadline: [Text]
- Primary CTA: [Button text]
- Secondary CTA: [Link text]
- Hero image/video: [Description]

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              [Headline - Max 60 chars]                      │
│                                                             │
│     [Subheadline - Max 120 chars explaining value]          │
│                                                             │
│         [Primary CTA Button]    [Secondary Link]            │
│                                                             │
│                    [Hero Image]                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Social Proof Section
**Elements**: Logos, testimonials, stats

### 3. Features Section
**Elements**: 3-6 feature cards with icons

### 4. How It Works
**Elements**: Step-by-step (3-4 steps)

### 5. Pricing Section
**Elements**: Plan cards, feature comparison

### 6. FAQ Section
**Elements**: Expandable questions

### 7. Final CTA Section
**Elements**: Repeated CTA with urgency

### 8. Footer
**Elements**: Links, social, legal
```

---

## Template: Dashboard

### 1. Executive Summary
```markdown
# [Dashboard Name] - Specification

## Dashboard Type
- Analytics/Reporting
- Management/Admin
- Monitoring/Status
- Personal/Profile

## Update Frequency
- Real-time: [Yes/No]
- Auto-refresh interval: [X seconds/minutes]

## Data Sources
- [Source 1]: [Description]
- [Source 2]: [Description]
```

### 2. Widget Specifications
```markdown
## Widgets

### Widget: [Widget Name]
**Type**: [Stat/Chart/Table/List/Activity]
**Data Source**: [API/Database]
**Update**: [Real-time/Polling/Manual]

**Layout**:
```
┌────────────────────────────┐
│ Widget Title          [⋮]  │
├────────────────────────────┤
│                            │
│     [Widget Content]       │
│                            │
│                            │
├────────────────────────────┤
│ Footer info          Link> │
└────────────────────────────┘
```

**Interactions**:
- Click: Navigate to detail view
- Hover: Show tooltip with details
- [⋮] Menu: Export, Refresh, Settings

**Empty State**: [Description]
**Error State**: [Description]
**Loading State**: [Description]
```

### 3. Layout Grid
```markdown
## Dashboard Layout

### Desktop (3-column grid)
```
┌──────────┬──────────┬──────────┐
│          │          │          │
│ Widget 1 │ Widget 2 │ Widget 3 │
│          │          │          │
├──────────┼──────────┼──────────┤
│                     │          │
│   Widget 4 (2col)   │ Widget 5 │
│                     │          │
└─────────────────────┴──────────┘
```

### Tablet (2-column)
- Stack widgets in 2 columns
- Full-width charts

### Mobile (1-column)
- Single column stack
- Collapsible widgets
```

---

## Template: E-commerce Flow

### 1. Executive Summary
```markdown
# [Store Name] - E-commerce Flow Specification

## Product Types
- Physical goods
- Digital products
- Services
- Subscription

## Payment Methods
- Credit/Debit cards
- PayPal
- [Other methods]

## Shipping
- Domestic/International
- Real-time rates
- Free shipping threshold
```

### 2. Key Flows
```markdown
## User Flow: Product Discovery → Purchase

### 1. Product Listing Page
**Elements**:
- Filter sidebar/top bar
- Sort options
- Product grid (3-4 columns desktop)
- Pagination or infinite scroll
- Quick view option

**Product Card**:
```
┌────────────────────────────┐
│  [Product Image]           │
│                            │
│  Product Name              │
│  $XX.XX                    │
│  ★★★★☆ (24 reviews)        │
│  [Add to Cart]             │
└────────────────────────────┘
```

### 2. Product Detail Page
**Sections**:
1. Image gallery (zoom, thumbnails)
2. Product info (name, price, description)
3. Variants (size, color)
4. Add to cart + Wishlist
5. Shipping info
6. Reviews
7. Related products

### 3. Cart Page
**Elements**:
- Item list with thumbnails
- Quantity controls
- Remove buttons
- Price breakdown
- Promo code input
- Checkout CTA

### 4. Checkout Flow
**Steps**:
1. Shipping information
2. Shipping method selection
3. Payment information
4. Review & confirm
5. Order confirmation

**Features**:
- Guest checkout option
- Address autocomplete
- Saved payment methods
- Order summary (sticky)
```

---

## Asset Delivery Checklist

### For Image Generation
- [ ] Hero image concept description
- [ ] Feature illustration concepts
- [ ] Icon set requirements (style, size)
- [ ] Background texture/pattern needs
- [ ] User avatar placeholders
- [ ] Empty state illustrations
- [ ] Error state illustrations

### For Development
- [ ] Logo files (SVG, various sizes)
- [ ] Icon library (or icon font)
- [ ] Color palette (hex codes)
- [ ] Typography (font files/families)
- [ ] Image assets with dimensions
- [ ] Animation specifications

### For Design Handoff
- [ ] Figma/Sketch file (if applicable)
- [ ] Style guide document
- [ ] Component library
- [ ] Prototype/interaction links
