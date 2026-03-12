# UI Design Patterns Library

Reference guide for common UI patterns with ASCII visualizations.

## Navigation Patterns

### Top Navigation Bar
```
┌─────────────────────────────────────────────────────────────┐
│  Logo      Home   Features   Pricing   About      [Sign In] │
└─────────────────────────────────────────────────────────────┘
```

### Sidebar Navigation
```
┌────────┬──────────────────────────────────────────────────┐
│        │                                                  │
│  Logo  │              Main Content Area                   │
│        │                                                  │
├────────┤                                                  │
│ Dashboard                                                  │
│ Projects │                                                  │
│ Team     │                                                  │
│ Settings │                                                  │
│          │                                                  │
└────────┴──────────────────────────────────────────────────┘
```

### Tab Navigation
```
┌─────────┬─────────┬─────────┬─────────┐
│  Tab 1  │  Tab 2  │  Tab 3  │  Tab 4  │
├─────────┴─────────┴─────────┴─────────┤
│                                       │
│         Tab Content Area              │
│                                       │
└───────────────────────────────────────┘
```

### Breadcrumb
```
Home > Category > Subcategory > Current Page
```

### Bottom Navigation (Mobile)
```
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│   🏠    │   🔍    │    ➕   │   💬    │   👤    │
│  Home   │ Search  │   Add   │  Chat   │ Profile │
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

## Form Patterns

### Single Input Field
```
Label
┌────────────────────────────┐
│ placeholder text           │
└────────────────────────────┘
```

### Input with Icon
```
Email
┌────────────────────────────┐
│ ✉️  user@example.com       │
└────────────────────────────┘
```

### Input with Validation
```
Password
┌────────────────────────────┐
│ ••••••••••••               │
└────────────────────────────┘
✓ At least 8 characters
✓ Contains number
✗ Needs special character
```

### Multi-Step Form Progress
```
Step 1 of 3: Personal Info
══════════════════════════════════════════
●───────○───────○
Account  Profile  Confirm
```

### Search with Filters
```
┌────────────────────────────┐ ┌────────────┐
│ Search...                  │ │ Filters ▼  │
└────────────────────────────┘ └────────────┘
```

## Card Patterns

### Basic Card
```
┌────────────────────────────┐
│  [Image]                   │
│                            │
│  Card Title                │
│  Brief description text    │
│  goes here.                │
│                            │
│  [Learn More]              │
└────────────────────────────┘
```

### Card with Actions
```
┌────────────────────────────┐
│  📄 Document Name          │
│  Modified 2 days ago       │
│                            │
│  [Edit] [Share] [Delete]   │
└────────────────────────────┘
```

### Stat Card
```
┌────────────────────────────┐
│  Total Users               │
│  ┌────────────────────┐    │
│  │     12,345         │    │
│  └────────────────────┘    │
│  ↑ 12% from last month     │
└────────────────────────────┘
```

## List Patterns

### Simple List
```
┌────────────────────────────┐
│  ● Item One                │
│  ───────────────────────── │
│  ● Item Two                │
│  ───────────────────────── │
│  ● Item Three              │
└────────────────────────────┘
```

### List with Meta
```
┌────────────────────────────┐
│  👤 John Doe           2m  │
│     john@example.com       │
│  ───────────────────────── │
│  👤 Jane Smith         1h  │
│     jane@example.com       │
└────────────────────────────┘
```

## Modal/Dialog Patterns

### Confirmation Dialog
```
┌────────────────────┐
│  Delete Item?   ✕  │
├────────────────────┤
│                    │
│  Are you sure you  │
│  want to delete    │
│  this item?        │
│                    │
│  [Cancel] [Delete] │
└────────────────────┘
```

### Form Modal
```
┌────────────────────────────┐
│  Edit Profile           ✕  │
├────────────────────────────┤
│  Name                      │
│  ┌────────────────────┐    │
│  │ John Doe           │    │
│  └────────────────────┘    │
│                            │
│  Email                     │
│  ┌────────────────────┐    │
│  │ john@example.com   │    │
│  └────────────────────┘    │
│                            │
│  [Cancel]    [Save Changes]│
└────────────────────────────┘
```

## Button Patterns

### Button Hierarchy
```
Primary:   ╔══════════╗
           ║  Action  ║
           ╚══════════╝

Secondary: ┌──────────┐
           │  Action  │
           └──────────┘

Tertiary:  Action >
```

### Button States
```
Normal:    ╔══════════╗
           ║  Submit  ║
           ╚══════════╝

Hover:     ╔══════════╗ ▓▓▓
           ║  Submit  ║
           ╚══════════╝

Disabled:  ▒▒▒▒▒▒▒▒▒▒▒▒
           ▒ Submit  ▒
           ▒▒▒▒▒▒▒▒▒▒▒▒

Loading:   ╔══════════╗
           ║ ◐ Saving ║
           ╚══════════╝
```

## Feedback Patterns

### Toast Notification
```
┌──────────────────────────┐
│  ✓ Changes saved         │
└──────────────────────────┘
```

### Inline Error
```
Email
┌────────────────────────────┐
│ user@invalid               │
└────────────────────────────┘
⚠ Please enter a valid email
```

### Empty State
```
┌────────────────────────────┐
│                            │
│        [📭 Icon]           │
│                            │
│     No messages yet        │
│                            │
│  When you receive messages │
│  they will appear here     │
│                            │
│     [Start Conversation]   │
│                            │
└────────────────────────────┘
```

### Loading State
```
┌────────────────────────────┐
│  ◐ Loading...              │
│                            │
│  ┌────────────────────┐    │
│  │ ░░░░░░░░░░░░░░░░░░ │    │
│  └────────────────────┘    │
│                            │
│  ┌────────────────────┐    │
│  │ ░░░░░░░░░░░░░░░░░░ │    │
│  └────────────────────┘    │
└────────────────────────────┘
```

## Dashboard Patterns

### Stats Overview
```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Users    │ │ Revenue  │ │ Orders   │ │ Growth   │
│ 12,345   │ │ $45.2K   │ │   892    │ │  +23%    │
│ ↑ 12%    │ │ ↑ 8%     │ │ ↑ 15%    │ │ vs last  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Chart Layout
```
┌─────────────────────────────────────────────────┐
│  Revenue Overview              [Week ▼] [Export]│
├─────────────────────────────────────────────────┤
│                                                 │
│    ▲                                          ╱ │
│    │                                    ╱╲╱   │
│    │                              ╱╲╱        │
│    │                        ╱╲╱               │
│    └──────────────────────────────────────▶   │
│       Mon  Tue  Wed  Thu  Fri  Sat  Sun         │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Data Table
```
┌─────────────────────────────────────────────────────┐
│ Name        │ Role      │ Status   │ Last Active   │
├─────────────┼───────────┼──────────┼───────────────┤
│ John Doe    │ Admin     │ ● Active │ 2 min ago     │
│ Jane Smith  │ Editor    │ ● Active │ 1 hour ago    │
│ Bob Johnson │ Viewer    │ ○ Away   │ 2 days ago    │
└─────────────────────────────────────────────────────┘
```

## Mobile-Specific Patterns

### Mobile Header
```
┌────────────────────────────┐
│ ☰  Page Title         🔍 🔔│
└────────────────────────────┘
```

### Pull to Refresh
```
┌────────────────────────────┐
│      ↓ Pull to refresh     │
├────────────────────────────┤
│                            │
│      Content Area          │
│                            │
└────────────────────────────┘
```

### Swipe Actions
```
┌────────────────────────────┐
│  [Archive] [Delete] │ Item │
│◄────────────────────┤     │
│                     │     │
└────────────────────────────┘
```

## Responsive Breakpoints Reference

| Breakpoint | Width | Common Usage |
|------------|-------|--------------|
| Mobile | < 640px | Single column, stacked layout |
| Tablet | 640px - 1024px | 2-column grid, adjusted nav |
| Desktop | > 1024px | Full layout, multi-column |
| Wide | > 1280px | Maximum content width |
