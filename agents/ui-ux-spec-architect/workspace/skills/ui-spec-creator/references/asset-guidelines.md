# Asset Guidelines Reference

Guidelines for preparing assets for image generation, development, and design handoff.

## For AI Image Generation

### Writing Effective Prompts

**Structure:**
```
[Subject] + [Style] + [Mood/Atmosphere] + [Technical specs] + [Avoid]
```

**Example:**
```
Modern SaaS dashboard interface, clean minimal design, 
blue and white color scheme, professional business software, 
UI mockup, high quality, sharp focus --ar 16:9
```

### Prompt Patterns by Asset Type

#### Hero Illustrations
```
Subject: Abstract technology concept illustration / Isometric workspace 
         / Diverse team collaborating
Style: Flat vector, 3D render, isometric, hand-drawn
Mood: Professional, friendly, innovative, trustworthy
Technical: White background, scalable, minimal details

Example: "Isometric illustration of people working at computers, 
collaborative workspace, modern office, blue and purple gradient, 
clean vector style, white background, minimal design"
```

#### Icons
```
Subject: [Specific object/concept] icon
Style: Line icons / Solid icons / Duotone
Mood: Simple, recognizable, consistent
Technical: 24x24px grid, 2px stroke, rounded corners

Example: "Shopping cart icon, line style, 2px stroke, 
rounded corners, minimalist, black on white, 24px grid"
```

#### Backgrounds
```
Subject: Abstract gradient / Geometric pattern / Subtle texture
Style: Soft, non-distracting
Mood: Professional, calming
Technical: Seamless if pattern, low contrast

Example: "Subtle geometric pattern, very light gray and white, 
minimal texture, seamless, low contrast, background"
```

#### Product Mockups
```
Subject: Device showing [content] / Product in context
Style: Realistic / Stylized
Mood: Professional, aspirational
Technical: High resolution, proper lighting

Example: "MacBook Pro on clean white desk, screen showing dashboard UI, 
soft natural lighting, minimal workspace, professional photography style"
```

### Negative Prompts (What to Avoid)
```
--no text, words, letters, watermark, signature, blurry, 
low quality, distorted, ugly, duplicate, cropped, out of frame
```

## Image Specifications

### Standard Sizes

| Use Case | Width | Height | Aspect Ratio | Format |
|----------|-------|--------|--------------|--------|
| Hero (web) | 1920px | 1080px | 16:9 | JPG/PNG/WebP |
| Hero (mobile) | 750px | 1334px | 9:16 | JPG/PNG/WebP |
| Feature illustrations | 800px | 600px | 4:3 | PNG/SVG |
| Icons | 24px | 24px | 1:1 | SVG/PNG |
| App store screenshots | Per platform | Per platform | Device | PNG |
| Social media | 1200px | 630px | 1.91:1 | JPG/PNG |
| Avatars | 256px | 256px | 1:1 | JPG/PNG |

### Responsive Image Strategy

**Srcset for Web:**
```html
<img src="image-800.jpg"
     srcset="image-400.jpg 400w,
             image-800.jpg 800w,
             image-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px,
            (max-width: 1000px) 800px,
            1200px"
     alt="Description">
```

### Color Palette Documentation

**Format:**
```
Primary:   #0066FF (RGB: 0, 102, 255)   - Buttons, links, CTAs
Secondary: #6B7280 (RGB: 107, 114, 128) - Secondary text
Success:   #10B981 (RGB: 16, 185, 129)  - Success states
Warning:   #F59E0B (RGB: 245, 158, 11)  - Warnings
Error:     #EF4444 (RGB: 239, 68, 68)   - Errors

Background: #FFFFFF - Main background
Surface:    #F9FAFB - Cards, elevated surfaces
Border:     #E5E7EB - Dividers, borders
Text:       #111827 - Primary text
TextMuted:  #6B7280 - Secondary text
```

## Typography Specifications

### Font Selection Guidelines

**For Web:**
- Primary: System fonts or Google Fonts
- Fallback stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Load: Use `font-display: swap`

**For Mobile:**
- iOS: San Francisco (system)
- Android: Roboto (system)
- Custom: Bundle font files

### Type Scale

| Level | Size | Line Height | Letter Spacing | Usage |
|-------|------|-------------|----------------|-------|
| H1 | 48px / 3rem | 1.1 | -0.02em | Hero headlines |
| H2 | 36px / 2.25rem | 1.2 | -0.01em | Section titles |
| H3 | 24px / 1.5rem | 1.3 | 0 | Subsection titles |
| H4 | 20px / 1.25rem | 1.4 | 0 | Card titles |
| Body | 16px / 1rem | 1.6 | 0 | Main text |
| Small | 14px / 0.875rem | 1.5 | 0 | Secondary text |
| Caption | 12px / 0.75rem | 1.4 | 0.01em | Labels, help text |

**Mobile Adjustments:**
- H1: 32px (down from 48px)
- H2: 24px (down from 36px)
- Body: 16px (keep readable)

## Icon Specifications

### Icon System Design

**Grid:** 24x24px base grid
**Stroke:** 2px (consistent)
**Corners:** Rounded (2px radius)
**End caps:** Rounded

**Sizes:**
- xs: 16px
- sm: 20px
- md: 24px (default)
- lg: 32px
- xl: 48px

### Icon Requirements for Development

**SVG Format:**
```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" 
     xmlns="http://www.w3.org/2000/svg">
  <path d="..." stroke="currentColor" stroke-width="2" 
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

**Sprite Sheet:**
- Combine icons into single SVG sprite
- Use `<use>` reference
- Reduces HTTP requests

### Icon Libraries (Recommended)

| Library | Style | Count | License |
|---------|-------|-------|---------|
| Lucide | Clean, consistent | 1000+ | MIT |
| Heroicons | Friendly | 500+ | MIT |
| Phosphor | Flexible weights | 7000+ | MIT |
| Tabler | Minimal | 4000+ | MIT |

## Asset Checklist by Phase

### Pre-Design Phase
- [ ] Mood board/images for inspiration
- [ ] Competitor screenshots for reference
- [ ] Brand guidelines (colors, fonts, voice)
- [ ] Stock photo requirements list

### Design Phase
- [ ] Logo variations (light/dark, icon only)
- [ ] Color palette (with accessibility checks)
- [ ] Typography scale
- [ ] Icon set (all required icons)
- [ ] Illustration concepts
- [ ] Photography direction

### Pre-Development Phase
- [ ] All images optimized (TinyPNG/Squoosh)
- [ ] Icons exported as SVG
- [ ] Fonts licensed and bundled
- [ ] Favicon set (all sizes)
- [ ] Social preview images (Open Graph)

### Pre-Launch Phase
- [ ] App store screenshots
- [ ] Loading/splash screen images
- [ ] Error state illustrations
- [ ] Empty state illustrations
- [ ] Email template assets

## File Naming Conventions

**Format:**
```
[type]-[name]-[variant]-[size].[ext]
```

**Examples:**
```
icon-search-24.svg
icon-search-24-white.svg
img-hero-home-1920.jpg
img-hero-home-1920@2x.jpg
logo-primary-horizontal.svg
logo-white-vertical.svg
illustration-onboarding-step1.svg
```

## Delivery Formats

### For Developers

**Images:**
- Format: WebP (with JPG/PNG fallback)
- Optimization: 80% quality
- Responsive: Multiple sizes

**Icons:**
- Format: SVG (inline or sprite)
- Optimization: SVGO

**Fonts:**
- Format: WOFF2 (primary), WOFF (fallback)
- Subsetting: Remove unused characters

### For Designers

**Source Files:**
- Format: Figma (.fig) or Sketch (.sketch)
- Organization: Pages by flow/feature
- Components: Properly named and organized

**Exports:**
- Format: PDF (for review), PNG (for preview)
- Resolution: 2x for retina displays

### For AI Image Generators

**Prompts:**
- Format: Text file (.txt) or markdown (.md)
- Structure: One prompt per line
- Parameters: Aspect ratio, style refs, negative prompts

**Reference Images:**
- Format: JPG/PNG
- Purpose: Style reference, composition guide
- Quantity: 3-5 examples per style
