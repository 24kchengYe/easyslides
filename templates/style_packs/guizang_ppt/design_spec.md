# Guizang PPT Editable Style Migration

> Native SVG style pack based on `op7418/guizang-ppt-skill`, adapted for the EasySlides editable PPTX pipeline.

## I. Template Overview

| Field | Value |
|---|---|
| Source | https://github.com/op7418/guizang-ppt-skill |
| Upstream commit | `3d87acc` |
| License | MIT |
| Use Cases | Narrative talks, product analysis, personal sharing, method decks, design-led internal presentations |
| Design Tone | Editorial, high-contrast, structured, modern, grid-driven |

This migration preserves the upstream style language but does not preserve the HTML runtime, keyboard navigation, canvas effects, or browser-only animations. The target is editable PPTX: all page shells are plain SVG geometry and text so `scripts/svg_to_pptx.py` can convert them into native DrawingML shapes.

## II. Canvas Specification

- Canvas: `1280 x 720`, 16:9.
- Safe area: keep primary content inside `x=64..1216`, `y=44..662`.
- Source HTML viewport units are resolved into fixed SVG coordinates.
- Avoid browser-only constructs: no `foreignObject`, scripts, CSS layout engines, WebGL, or HTML canvas.

## III. Style Variants

### Style A: Editorial Ink

Use for narrative, opinionated, or magazine-like talks. It carries the upstream electronic magazine and electronic ink mood through:

- Ink/paper palettes.
- Large editorial titles.
- Visible chrome metadata.
- Alternating dark and light section rhythm.
- Image slots as framed evidence, not decorative backgrounds.

Default theme: `monocle_classic`.

### Style B: Swiss Internationalism

Use for factual, product, analysis, and method decks. It carries the upstream Swiss mode through:

- 16-column grid logic.
- One saturated accent color per deck.
- Hairline dividers and rectangular color blocks.
- No gradients, shadows, or rounded cards.
- Registered layout IDs from `S01` to `S22` mapped in `layouts.json`.

Default theme: `ikb`.

## IV. Color Scheme

Colors are locked in `design_tokens.json`.

- Style A offers 5 upstream themes: `monocle_classic`, `indigo_porcelain`, `forest_ink`, `kraft_paper`, and `dune`.
- Style B offers 4 upstream themes: `ikb`, `lemon`, `lemon_green`, and `safety_orange`.
- A generated deck should use exactly one variant and one theme.
- Do not mix Style B accent colors on a single deck.

## V. Typography System

- Style A display: Georgia/Cambria-style editorial serif; body: Aptos/Arial/Microsoft YaHei.
- Style B display/body: Helvetica Neue/Inter/Arial; mono labels: JetBrains Mono/Consolas.
- Chinese titles should be shortened before shrinking. If they must wrap, lower title size before letting text collide with content.

## VI. Page Types

| Variant | Page Type | SVG |
|---|---|---|
| Style A | Cover | `style_a/01_cover.svg` |
| Style A | Section | `style_a/02_section.svg` |
| Style A | Content | `style_a/03_content.svg` |
| Style A | Closing | `style_a/04_closing.svg` |
| Style B | Cover | `style_b/01_cover.svg` |
| Style B | Statement | `style_b/02_statement.svg` |
| Style B | Content | `style_b/03_content.svg` |
| Style B | Image Hero | `style_b/04_image_hero.svg` |
| Style B | Closing | `style_b/05_closing.svg` |

Swiss also has exact native layout shells under `swiss/`:

- `S01_index_cover.svg` through `S22_image_hero.svg`.
- Each file declares `data-style="guizang-style-b"` and its own
  `data-layout="Sxx"` attribute.
- Use these when a slide should follow a specific upstream Swiss layout rather
  than one of the broader shell families above.

## VII. Migration Notes

- Upstream Style A has 10 common HTML layouts. This pack provides four editable SVG shells that cover the same narrative roles.
- Upstream Style B has 22 locked HTML layouts. This pack records all `S01-S22` IDs, maps them to five editable SVG shell families, and includes one native SVG skeleton per registered Swiss layout under `swiss/`.
- Image generation prompts from upstream should be used only for external image assets. The final slide shell must remain SVG geometry plus placed raster assets.

## VIII. Harness Contract

Use this pack through `spec_lock.md` when the deck should keep Guizang's style discipline:

```markdown
## style_pack
- package: guizang_ppt
- variant: style_b_swiss
- theme: ikb
- layout_source: templates/style_packs/guizang_ppt
- validator: scripts/validate_guizang.py
```

Then write `page_layouts` as Guizang registry IDs (`S01`-`S22`) or package-relative SVG basenames. Validate the contract with `scripts/style_pack_contract.py` before execution.

## IX. SVG Technical Constraints

- Root `viewBox` must be `0 0 1280 720`.
- Use SVG text and simple DrawingML-friendly shapes.
- Use `<tspan>` for wrapped text.
- Do not use `foreignObject`, `<script>`, HTML elements, CSS grid, SVG filters, masks, or browser canvas.
- Run:

```bash
python scripts/validate_guizang.py templates/style_packs/guizang_ppt
python scripts/svg_quality_checker.py templates/style_packs/guizang_ppt
```
