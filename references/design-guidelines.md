# Academic Design Guidelines

## Color System

### Academic Blue Theme (Default)

| Role | Color | Hex | Use |
|------|-------|-----|-----|
| Primary | Dark blue | `#003366` | Headers, chapter backgrounds |
| Accent | Blue | `#0066CC` | Links, highlights, tags |
| Emphasis | Red | `#CC0000` | Key findings, warnings |
| Light bg | Light blue-gray | `#E8F4FC` | Card backgrounds |
| White | White | `#FFFFFF` | Main backgrounds |
| Text primary | Dark gray | `#333333` | Body text |
| Text secondary | Medium gray | `#666666` | Captions |
| Text tertiary | Light gray | `#999999` | Footnotes |
| Neutral bg | Off-white | `#F5F7FA` | Alternate backgrounds |
| Border | Gray | `#D0D7E0` | Dividers, table borders |

### Functional Colors

| Function | Color | Hex |
|----------|-------|-----|
| Success | Green | `#28A745` |
| Warning | Orange | `#FFA500` |
| Info | Teal | `#17A2B8` |

### Color Usage (60-30-10 Rule)

- **60%**: Neutral backgrounds (`#FFFFFF`, `#F5F7FA`)
- **30%**: Primary color (`#003366`)
- **10%**: Accent color (`#0066CC`, `#CC0000`)

## Typography

### Font Stack

```
"Microsoft YaHei", "微软雅黑", Arial, sans-serif
```

### Size Hierarchy (1280x720 canvas)

| Level | Size | Weight | Use |
|-------|------|--------|-----|
| H1 | 56px | Bold | Cover title |
| H2 | 36px | Bold | Section headers |
| H3 | 28px | Bold | Subsection headers |
| H4 | 24px | Bold | Card titles |
| Body | 20px | Regular | Main content |
| Body-sm | 18px | Regular | Secondary content |
| Caption | 16px | Regular | Labels, annotations |
| Footnote | 12px | Regular | Page numbers, sources |

### Font Size Ramp for CJK Text

| Character Count | Title Font Size |
|----------------|----------------|
| ≤ 8 chars | 36px |
| 9-12 chars | 32px |
| 13-16 chars | 28px |
| 17+ chars | 24px |

## Layout System

### Page Structure (1280x720)

```
┌─────────────────────────────────────┐
│ Header (y=0, h=70)                  │
├─────────────────────────────────────┤
│ Key Message Bar (y=70, h=50)        │
├─────────────────────────────────────┤
│                                     │
│ Content Area (y=135, h=515)         │
│                                     │
├─────────────────────────────────────┤
│ Footer (y=665, h=55)               │
└─────────────────────────────────────┘
```

- Left/Right margins: 40px
- Safe area: x:40-1240, y:70-665

### Spacing System

| Element | Value |
|---------|-------|
| Card gap | 20px |
| Content block gap | 24px |
| Card padding | 20px |
| Border radius | 8px |
| Section padding | 40px |

### Content Layout Patterns

**Single column centered**:
- For key statements, quotes, definitions
- Text centered in content area

**Two-column cards**:
- For comparisons, pros/cons, before/after
- Equal width columns with 20px gap

**Left-right split**:
- 5:5 or 4:6 ratio
- Text on left, image/chart on right

**Card grid**:
- 2x2 or 3x2 grid
- For multiple items with equal weight

**Timeline**:
- Horizontal or vertical
- For processes, milestones, chronological data

**Table**:
- Structured data comparison
- Header row with accent color

## Page Rhythm

### Theme Alternation

Alternate between light, dark, and hero pages:
- No 3+ consecutive same-theme pages
- Chapter dividers break up content sections
- Cover and ending are always "hero" pages

### Visual Weight Distribution

```
Cover (hero) → TOC (light) → Chapter (dark) → Content (light) → Content (light) → Chapter (dark) → Content (light) → Ending (hero)
```

## Component Specs

### Tags

Blue tag: rounded rect (`rx=4`) + white text, 16px
Red tag: rounded rect (`rx=4`) + white text, 16px

### Flow Arrows

SVG path with arrowhead marker, stroke `#D0D7E0`, width 2px

### Data Highlight Boxes

Rounded rect with light background, key number in 36px bold, label in 16px

### Cards

```
┌─────────────────────────┐
│ ● Icon    Title         │  ← 20px padding
│                         │
│ Description text that   │  ← 18px body
│ wraps within the card.  │
│                         │
│ [Tag]                   │  ← optional tag
└─────────────────────────┘
  ↑ 8px border radius
  ↑ #FFFFFF or #E8F4FC background
```

## Speaker Notes Style

### Academic Mode

- Formal, structured narration
- Key statistics and citations
- Transition phrases between sections
- Time allocation guidance per slide
- Backup points for Q&A

### Notes Structure per Slide

```markdown
## Slide N: [Title]

**Key points:**
- Point 1 with supporting data
- Point 2 with citation

**Transition:** "Moving on to..."

**Time:** ~2 minutes

**Q&A prep:** Anticipate questions about...
```
