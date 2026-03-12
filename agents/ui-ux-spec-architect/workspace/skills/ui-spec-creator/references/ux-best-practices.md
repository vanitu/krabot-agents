# UX Best Practices Reference

Guiding principles for creating user-centered designs.

## Nielsen's 10 Usability Heuristics

### 1. Visibility of System Status
Always keep users informed about what's happening.

**Do:**
- Show loading indicators during operations
- Display progress for multi-step processes
- Confirm actions with toast notifications
- Update UI immediately when state changes

**Examples:**
- "Saving..." → "Saved ✓"
- Upload progress: 45% complete
- "3 items in cart"

### 2. Match Between System and Real World
Use language and concepts familiar to users.

**Do:**
- Use natural, conversational labels
- Follow real-world conventions
- Use icons with clear meanings
- Avoid technical jargon

**Don't:**
- Use system error codes ("Error 0x80070057")
- Use developer terminology ("Execute POST request")
- Use ambiguous icons

### 3. User Control and Freedom
Provide clearly marked exits and undo options.

**Do:**
- Allow canceling operations
- Provide breadcrumbs for navigation
- Support undo for destructive actions
- Show "Back" buttons in multi-step flows

**Patterns:**
- Cancel button on all modals
- "Undo delete" for 5 seconds
- Breadcrumb: Home > Products > Electronics

### 4. Consistency and Standards
Maintain consistency internally and with platform conventions.

**Do:**
- Use same labels for same actions
- Position elements in predictable locations
- Follow platform design guidelines (iOS/Android/Web)
- Maintain consistent visual hierarchy

### 5. Error Prevention
Prevent problems from occurring rather than fixing them.

**Do:**
- Validate input in real-time
- Use constraints (date pickers vs text input)
- Show character limits
- Confirm destructive actions
- Disable submit until form is valid

### 6. Recognition Rather Than Recall
Minimize memory load by making options visible.

**Do:**
- Show recently used items
- Display search suggestions
- Use autocomplete
- Keep navigation visible
- Show selected filters

**Don't:**
- Require users to remember codes
- Hide important options in menus
- Force users to re-enter data

### 7. Flexibility and Efficiency of Use
Accommodate both novice and expert users.

**Do:**
- Provide keyboard shortcuts
- Support bulk operations
- Allow customization
- Remember user preferences

**Examples:**
- Cmd+S to save
- Select all + bulk delete
- Customizable dashboard layout

### 8. Aesthetic and Minimalist Design
Remove unnecessary elements.

**Do:**
- Prioritize content over chrome
- Use whitespace effectively
- Limit colors and fonts
- Remove decorative elements that don't add value

**Rule:** If an element doesn't support user goals, remove it.

### 9. Help Users Recognize, Diagnose, and Recover from Errors
Clear error messages with solutions.

**Do:**
- Use plain language (no codes)
- Explain what went wrong
- Suggest how to fix it
- Be specific and actionable

**Good:** "Password must be at least 8 characters with 1 number"
**Bad:** "Invalid input"

### 10. Help and Documentation
Provide easily accessible help.

**Do:**
- Use contextual help (tooltips)
- Provide empty state guidance
- Include inline hints
- Make help searchable

## Accessibility Guidelines (WCAG 2.1 Basics)

### Perceivable
- **Color Contrast**: Minimum 4.5:1 for normal text
- **Don't rely on color alone**: Use icons + color for status
- **Alt text**: Describe images meaningfully
- **Resizable text**: Support up to 200% zoom

### Operable
- **Keyboard navigation**: All functions available via keyboard
- **Focus indicators**: Visible focus states
- **Timing**: Allow users to extend time limits
- **Seizures**: No flashing content (>3 flashes/second)

### Understandable
- **Consistent navigation**: Keep menus in same location
- **Error identification**: Clearly mark errors
- **Labels**: Associate labels with form controls

### Robust
- **Valid HTML**: Use semantic markup
- **Screen readers**: Test with assistive technology

## Mobile UX Considerations

### Touch Targets
- Minimum 44x44pt (iOS) or 48x48dp (Android)
- Space between interactive elements
- Avoid placing buttons too close to screen edges

### Thumb Zone
```
┌────────────────────────────┐
│  Hard      Hard      Hard  │
│  to reach  to reach  to reach│
│                            │
│  Easy      Easy      Easy  │
│  to reach  to reach  to reach│
│  ┌──────────────────────┐  │
│  │    NATURAL ZONE      │  │
│  │   (thumb rests here) │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

### Input Considerations
- Show appropriate keyboard type (email, number, phone)
- Use native pickers for dates/times
- Support autocorrect appropriately
- Provide input masks for formatted data

### Performance
- Show skeleton screens during loading
- Optimize images for mobile
- Minimize data entry
- Support offline where possible

## Progressive Disclosure

Reveal information progressively to reduce cognitive load.

**Patterns:**
1. **Basic → Advanced**: Show simple options first, advanced on demand
2. **Summary → Detail**: Show overview, expand for details
3. **Step-by-step**: Break complex tasks into steps

**Example:**
```
[Simple Search Bar]
     ↓ Click "Advanced"
[Search Bar]
[Filter by Date: ______]
[Filter by Category: ▼]
[Filter by Location: ______]
```

## Feedback Patterns

### Immediate Feedback
- Button press states
- Form validation on blur
- Character counters
- Upload progress

### Success Feedback
- Toast notifications (auto-dismiss 3-5s)
- Green checkmarks
- Success modals for important actions
- Animation for delight

### Error Feedback
- Inline field errors
- Error summaries at top of forms
- Red color + icon
- Clear recovery path

### Loading Feedback
- Skeleton screens (preferred over spinners)
- Progress bars for known duration
- Spinners for unknown duration
- "Loading..." text with context

## Information Architecture

### Visual Hierarchy
1. **Size**: Larger elements attract more attention
2. **Color**: High contrast draws focus
3. **Spacing**: Whitespace creates grouping
4. **Position**: Top-left gets most attention (F-pattern)

### F-Pattern Reading
```
┌────────────────────────────┐
│ ████████████████████████   │  ← Headline (read fully)
│ ████████████████████████   │
│                            │
│ ████████                   │  ← Subheading (read start)
│ ████████                   │
│                            │
│ ████   ████   ████         │  ← Scanning bullets
│ ████   ████   ████         │
└────────────────────────────┘
```

### Z-Pattern (Simple Pages)
```
┌────────────────────────────┐
│ 1. Logo        2. Nav/CTA  │
│                            │
│                            │
│                            │
│ 3. Content     4. CTA      │
└────────────────────────────┘
```

## Microinteractions

Small animations that enhance user experience:

- **Button hover**: Slight lift or color change
- **Toggle switch**: Smooth slide animation
- **Checkbox**: Satisfying check animation
- **Pull-to-refresh**: Elastic feedback
- **Infinite scroll**: Smooth content loading

## Cognitive Load Reduction

### Chunking
Break information into digestible chunks:
- Group related form fields
- Use step indicators for long forms
- Separate content into cards

### Defaults
- Pre-fill known information
- Suggest common options
- Remember previous selections

### Autocomplete
- Reduce typing with suggestions
- Use for search, addresses, tags
- Show recent/relevant options

## Trust and Credibility

### Security Indicators
- HTTPS lock icons
- Secure payment badges
- Privacy policy links
- Data protection messaging

### Social Proof
- User counts
- Testimonials
- Ratings and reviews
- Client logos

### Transparency
- Clear pricing
- No hidden fees
- Explain data usage
- Show system status
