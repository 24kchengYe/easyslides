# Scientific & presentation figures — house rules

How to make every figure in a deck or paper. Three workflows, one decision tree,
and the hard-won rules that keep figures correct, editable, and legible.

These rules were distilled from a real Nature-Communications talk build. Follow them
unless you have a specific reason not to — each one fixes a mistake that actually happened.

---

## 1. Decision tree — which workflow for which figure

| The figure is… | Workflow | Tool | Output | Editable after? |
|---|---|---|---|---|
| **Real numbers** (bar / scatter / line / heatmap / box, with values) | DATA | matplotlib + `scripts/figures/figstyle.py` (talk/projector) or `style_presets.py` (journal) + `figure_export.py` | PNG / PDF / EPS | image (re-run script) |
| **Concept / flow / framework / mechanism** (boxes + arrows + text, NO data) | CONCEPT | hand-author an SVG → `scripts/figures/svg_inject.inject_svg_shapes()` | native DrawingML shapes in the slide | **yes — editable in PowerPoint** |
| **Cover / complex illustration / photo-like** | AI-GEN | `scripts/image_gen.py` (16 backends) + optional super-res | raster PNG | no (regenerate) |

**Default for a method/mechanism/conceptual slide is CONCEPT (SVG → native shapes)**, not
matplotlib and not AI-gen. The author wants diagrams that are *natively editable* in the
deck. Only reach for matplotlib when there is real data to plot; only reach for AI-gen for
artwork where editability does not matter.

Do **not** draw box-and-arrow "flowcharts" in matplotlib — they come out ugly and are not
editable. That is what the SVG-native path is for.

---

## 2. DATA figures (matplotlib)

### Use a shared style, never per-figure tweaks
- Talk / projector / slide deck → `scripts/figures/figstyle.py`: `FS.apply_rc()` then build;
  big projector-readable fonts (`FS_SUPTITLE..FS_SMALL`), colourblind palette
  (`C_BLUE #0072B2`, `C_ORANGE #D55E00`, `C_GREEN #009E73`, `C_RED #D62728`),
  `FS.panel_title(ax, 'a', '…')` for titles ABOVE the axes, `FS.savefig(fig, path)` (300 dpi, tight).
- Journal submission → `scripts/figures/style_presets.apply_publication_style('nature'|'science'|…)`
  + `figure_export.save_for_journal(fig, name, journal=…, figure_type=…)` (auto size + DPI).
- Changing the look = edit the style module once, not each script. See `templates/figures/matplotlib_themes/`.

### Numbers must be source-traceable — never invent them
- Load values from a results file (CSV/JSON) so the figure points back to data. **Do not hand-type
  a number you cannot trace.** If a value only exists in an old figure and not in any data file,
  say so and do not put it in a new figure as if confirmed.
- This is non-negotiable: a wrong number in a figure is worse than a missing one.

### Bake the message into the figure
- Each publication/talk figure carries an embedded title + one take-home line, so it stands alone
  when lifted out of the deck. Title goes ABOVE the axes (Nature style), never on the data.

### Prevent the three classic failures
1. **No text overlap** — check labels/legend/annotations don't collide.
2. **No too-small fonts** — projector-readable (figstyle sizes are ~2× journal sizes on purpose).
3. **No clipping when placed in PPTX** — size the image by its true aspect ratio; never stretch.
   Compute height from width × (img_h / img_w).

### Make legends/axes legible to non-experts
- A scary axis label like `d[logP(high)−logP(low)]/dδ` either gets reworded, or a one-line
  "Reading the axes:" gloss is added next to the figure on the slide.
- Colourblind-safe palette always (Okabe-Ito / Paul Tol / the figstyle palette).

---

## 3. CONCEPT diagrams (hand-authored SVG → native editable shapes)

This is the workflow that makes flow/mechanism/framework diagrams **editable in PowerPoint**.
Author an SVG, then `inject_svg_shapes(slide, svg_path)` converts it to native `<p:sp>`/`<p:grpSp>`.

### Canvas & coordinates
- Author at `viewBox="0 0 1280 720"`. 1 SVG px = 9525 EMU = a full 13.333×7.5 in slide.
  So shapes land in full-slide coordinates with **no scaling** — just draw where you want it.
- Leave the top ~140 px for the slide's title block; put the diagram in y≈180–700.

### SVG authoring rules (what the converter supports)
- **Rounded rectangles**: `rx=…`.
- **Arrows**: `<line … marker-end="url(#id)">` + a `<marker>` def. **Do NOT** draw arrowheads as
  `<path>` — they get dropped in conversion.
- **Fonts**: `font-family="'Segoe UI', Arial"` → stays selectable/editable with that font.
- **Text anchoring**: `text-anchor="start|middle|end"` is honoured.
- **font-size**: unitless px (`font-size="14"`), not `pt`.
- **Opacity**: set on each child element, **not** on a `<g>` group (group opacity is unsupported).
- **Avoid `<image>`** in these diagrams — embedded images need media wiring that `svg_inject` doesn't do.

### Composition rules (the ones that matter most)
- **Don't split a shared flow by object.** If several things follow the *same* process (e.g. three
  symbolic theories all do input → hidden state → linear readout → target), draw **one** flow and
  annotate the differences (input / target) in a side note. Only draw a **second** flow when the
  process genuinely differs — e.g. a different modality (image input vs text input).
- **Symmetry across a level.** If a level has N members, show all N (don't give one tier four cards
  and the next tier only two). Keep parallel things parallel.
- **Semantic colour.** Fix one colour per recurring entity across the whole deck (e.g. Scaling=blue,
  Decay=orange, Vitality=green, Perception=red) so the audience tracks by colour.
- **Internalise jargon, don't stack a glossary page.** Explain a term in one line where it first
  appears; don't add a separate "terms" slide. Keep prose tight — wordiness usually lives in the
  dense new diagram pages, not the original content; trim repetitive subtitles, not the data.

### Ready-made templates
`templates/figures/svg_examples/` has 9 proven diagrams to copy and adapt: `probe_flow.svg`
(shared flow + a separate modality flow), `memory_vs_causal_concept.svg` (vertical layer stack with
two highlighted layers + callouts), `causal_4theories.svg` / `memory_4theories.svg` (2×2 symmetric
summaries), `sampling_paradigm.svg`, `blueprint.svg`, `prompt_gen.svg`, `what_probes_4.svg`, `causal_flow.svg`.

### Helpers (`scripts/figures/gloss_helpers.py`)
`add_titled_blank_slide()` (white slide + standard title block), `add_divider_slide()` (dark
section cover), `add_gloss_box()` / `add_plain_caption()` (annotation boxes), `add_pagenum()`,
`renumber_pages()`, and palette constants (`BLUE/ORANGE/GREEN/RED/DARK/TINT`, `FONT="Segoe UI"`).

---

## 4. AI-generated illustration
For covers / rich illustration where editability is irrelevant, use the skill's own image
generation (`scripts/image_gen.py`, 16 backends, watermark removal). For framework diagrams that
need iteration, the optional EDSR super-resolution / img2img refinement / CS-venue presets can be
layered on. Prefer CONCEPT (editable SVG) for anything that is really boxes-and-arrows.

---

## 5. Verification — every figure, every slide

- **Render and look**: `soffice --headless --convert-to pdf` → `pdftoppm -png` → open the PNG and
  actually check it. Don't trust that it's fine without looking.
- **Native-editable check** (CONCEPT path): after injecting, unpack the .pptx and confirm the new
  shapes are `<p:sp>`/`<p:grpSp>`, **not** `<p:pic>` (a `<p:pic>` means it became a raster image).
- **Contact sheet** for a whole deck: tile all slide PNGs to scan structure + page-number continuity.

### python-pptx slide add/remove gotchas (will bite you)
- **Deleting a slide**: remove the `sldId` from `prs.slides._sldIdLst` **and** drop the rel:
  `prs.part.drop_rel(rId)`. Removing only the `sldIdLst` entry resurrects/duplicates the slide on save.
- **Mixing deletes + inserts in one session** causes part-name collisions
  (`Duplicate name 'ppt/slides/slideN.xml'`). After each structural change, **save then reopen**
  (`prs.save(p); prs = Presentation(p)`) before the next op, so part names are recomputed cleanly.
- **Blank-layout notes**: a Blank slide's `notes_slide.notes_text_frame` is `None` (no body
  placeholder). Inject a `<p:sp>` with `<p:ph type="body" idx="1"/>` into the notes spTree before
  setting notes text. (`gloss_helpers` shows the pattern.)
- **Page numbers**: 2-digit page-number text boxes need `word_wrap=False` + zero internal margins,
  or "09" wraps to two lines.

---

## TL;DR
Data → matplotlib (shared style, traceable numbers, no clipping). Concept/flow → hand-authored
SVG → native editable shapes (don't split shared flows, keep tiers symmetric, semantic colour).
Illustration → AI-gen. Always render-and-look; for concept diagrams confirm `<p:sp>` not `<p:pic>`.
