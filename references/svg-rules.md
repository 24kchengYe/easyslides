# SVG Authoring Rules

## Mandatory Constraints

### Canvas & ViewBox

- viewBox MUST match canvas dimensions exactly
- For 16:9 academic: `viewBox="0 0 1280 720"`
- Never use percentage-based positioning

### Allowed Elements

| Element | Use |
|---------|-----|
| `<rect>` | Backgrounds, cards, shapes |
| `<circle>` | Circles, dots, markers |
| `<ellipse>` | Elliptical shapes |
| `<line>` | Dividers, connectors |
| `<path>` | Complex shapes, icons |
| `<polygon>` | Triangles, polygons |
| `<polyline>` | Lines with multiple points |
| `<text>` | Text labels |
| `<tspan>` | Text wrapping within `<text>` |
| `<g>` | Grouping |
| `<defs>` | Reusable definitions |
| `<use>` | Icon references |
| `<image>` | Embedded images |
| `<linearGradient>` | Gradient fills |
| `<radialGradient>` | Radial gradients |
| `<pattern>` | Pattern fills |
| `<marker>` | Arrowheads |

### Forbidden Elements

- `foreignObject` — breaks PPTX conversion
- `<mask>` — not supported in DrawingML
- `<script>` — security risk
- `<style>` — use inline styles only
- `<switch>` — not supported
- `<a>` (hyperlinks) — add in PPTX post-processing

### Forbidden Attributes

- `rgba()` — use hex + opacity
- `calc()` — not supported
- CSS variables (`var()`) — not supported
- `mix-blend-mode` — not supported
- `filter` complex effects — limited support

## Text Rules

### Text Wrapping

Use `<tspan>` with `x`, `y`, `dy` attributes for multi-line text:

```xml
<text x="100" y="200" font-size="20" fill="#333333">
  <tspan x="100" dy="0">First line of text</tspan>
  <tspan x="100" dy="1.2em">Second line of text</tspan>
  <tspan x="100" dy="1.2em">Third line of text</tspan>
</text>
```

### Font Specification

Always specify both `font-family` and `font-size`:

```xml
<text font-family="Microsoft YaHei, Arial, sans-serif" font-size="20" fill="#333333">
```

### Text Alignment

Use `text-anchor` attribute:
- `text-anchor="start"` — left-aligned (default)
- `text-anchor="middle"` — centered
- `text-anchor="end"` — right-aligned

## Image Rules

### Embedded Images

Use `<image>` with `href` (not `xlink:href`):

```xml
<image href="images/photo.png" x="100" y="100" width="400" height="300"/>
```

### Image Paths

- Use relative paths: `images/filename.png`
- Images are base64-embedded during finalization
- Supported formats: PNG, JPG, SVG

## Icon Rules

### Referencing Icons

```xml
<use href="#tabler-filled/chart-bar" x="100" y="100" width="24" height="24"/>
```

Or with data-icon attribute (resolved during finalization):

```xml
<use data-icon="tabler-filled/chart-bar" x="100" y="100" width="24" height="24"/>
```

### Icon Library

Use one library per deck:
- `tabler-filled` — solid/filled icons
- `tabler-outline` — outline icons

Never mix libraries within a single deck.

## Color Rules

### Fill & Stroke

Always use hex colors:

```xml
<!-- Correct -->
<rect fill="#003366" stroke="#0066CC" stroke-width="2"/>

<!-- Wrong -->
<rect fill="rgba(0,51,102,0.5)"/>
<rect fill="rgb(0,51,102)"/>
```

### Opacity

Use `opacity` attribute (0-1):

```xml
<rect fill="#003366" opacity="0.5"/>
```

### Gradients

```xml
<defs>
  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#003366"/>
    <stop offset="100%" stop-color="#0066CC"/>
  </linearGradient>
</defs>
<rect fill="url(#grad1)" .../>
```

## Shape Rules

### Rounded Rectangles

Use `rx` and `ry` attributes:

```xml
<rect x="100" y="100" width="200" height="100" rx="8" ry="8"/>
```

### Coordinate Precision

- Use integers for pixel-perfect alignment
- Avoid sub-pixel coordinates unless necessary

## Animation Annotations

For post-processing animation hints, use `data-anim` attributes:

```xml
<g data-anim="fade-in" data-anim-delay="0.5">
  <text>Animated content</text>
</g>
```

## Quality Checklist

Before finalizing, verify:

- [ ] viewBox matches canvas dimensions
- [ ] No forbidden elements or attributes
- [ ] All text has font-family and font-size
- [ ] All colors are hex format
- [ ] Images use relative paths
- [ ] Icons from single library only
- [ ] No inline styles (use attributes)
- [ ] Text wrapping uses `<tspan>`
