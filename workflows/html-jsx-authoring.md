---
description: Evaluate HTML/JSX as an upstream authoring path while keeping EasySlides SVG-to-DrawingML as the production backend
---

# HTML/JSX Authoring Workflow

Use this workflow when the source is a rendered HTML page, dashboard, report,
SVG-heavy technical slide, or when an agent would author a complex layout more
reliably in HTML/JSX than by hand-writing SVG.

This is an upstream authoring workflow, not a replacement backend. EasySlides
keeps one production backend: normalized SVG/shape IR -> `svg_quality_checker.py`
-> `svg_to_pptx.py` -> editable DrawingML/PPTX.

## Architecture Contract

Primary mode: `html_jsx_upstream_to_easyslides_backend`

The agent may:

- use HTML/CSS/JSX to draft complex layouts and reusable components
- use browser measurement to read real rendered boxes instead of guessing
- study `@artifact-kit/pptxgenjs-jsx` and `html-to-pptx-skill` for authoring
  and DOM measurement patterns
- create isolated spikes under `experiments/` to compare output quality
- normalize measured objects into EasySlides-compatible SVG or a shape manifest

The agent must not:

- add `@artifact-kit/pptxgenjs-jsx`, PptxGenJS, React, Vite, or Babel as root
  EasySlides dependencies during exploration
- fork the main export path into a second production PPTX backend
- bypass `svg_quality_checker.py` before PPTX export
- keep browser-only features in the normalized SVG (`foreignObject`, `<style>`,
  CSS classes, scripts, masks, runtime layout dependencies)
- treat a raster screenshot as success when editable objects are required

## Lessons To Absorb From artifact-kit/html-to-pptx-skill

Adopt these strengths as Path C authoring discipline while keeping EasySlides'
SVG/shape IR and DrawingML exporter as the production backend:

- **copy-first exporter hygiene**: source HTML must stay clean. Put export
  buttons, measurement attributes, inline runtime helpers, and generated
  comments only in the copied exporter or measurement page.
- **visible vertical measuring surface**: flatten slides, tabs, carousels,
  routes, and inactive states so every page is visible in one stable
  top-to-bottom container before measuring.
- **measurement manifest before code**: list every slide root, panel, title,
  body block, SVG, chart, footer, and repeated primitive that will feed the
  normalized SVG or shape manifest. Each item needs a stable measurement id.
- **coordinate provenance**: every generated coordinate must come from browser
  measurement, explicit source HTML/CSS values, SVG `viewBox` geometry, chart
  data, or a small documented inset inside a measured object. Avoid inch or
  pixel values that only came from eyeballing a screenshot.
- **native reconstruction inventory**: before normalizing, inventory the source
  visuals and decide which objects become editable text, shapes, lines, tables,
  chart primitives, or image fallbacks. Cards, badges, arrows, matrices, icons,
  and diagram nodes should not collapse into text-only output.
- **SVG viewBox mapping**: for SVG-heavy pages, measure the SVG element once and
  map source primitives from their `viewBox` into EasySlides SVG/shape IR. Lines
  and arrows should preserve endpoints; heatmaps and matrices should become
  editable cell grids rather than raster images when data or primitives exist.
- **API and backend legality gate**: check planned constructs against
  EasySlides SVG rules and converter support before export. Do not keep browser
  features, invented chart types, unsupported SVG constructs, or screenshot-only
  shortcuts in the normalized output.
- **audit gate**: before handoff, verify that the source copy is untouched, all
  intended objects are measured or source-derived, the normalized SVG passes
  `svg_quality_checker.py`, and the final PPTX opens with selectable text and
  editable major shapes.

## Step 1: Decide Whether Path C Fits

Use Path C when at least one of these is true:

- layout complexity is high: dashboards, dense cards, nested grids, technical
  diagrams, report pages, or HTML already exists
- authoring would benefit from JSX components or repeated layout primitives
- a browser can measure final boxes more reliably than hand-coded coordinates
- the goal is to benchmark HTML/JSX against the current SVG authoring path

Stay on Path A when the slide is simple, template-led, or already has a clean
SVG shell. Use Path B when preserving an existing PPTX file is the real goal.

## Step 2: Run An Isolated Spike

Create experiments outside the main dependency graph:

```bash
mkdir -p experiments/pptxgenjs-jsx-spike
cd experiments/pptxgenjs-jsx-spike
pnpm init
pnpm add @artifact-kit/pptxgenjs-jsx
```

Keep any `package.json`, lockfile, generated HTML exporter, and downloaded
sample PPTX inside the experiment directory. Do not move those dependencies to
the repository root until there is a written decision to promote the path.

## Step 3: Measure, Then Normalize

For browser-authored pages:

1. Keep the source HTML clean.
2. Copy it to an exporter or measurement page.
3. Make every slide/page visible in a stable vertical document.
4. Add measurement attributes to slide roots and reusable objects.
5. Measure boxes, fonts, and SVG viewBox geometry in the browser.
6. Convert the measured result into normalized SVG or a shape manifest.

Preferred normalized output is SVG under the usual project folders:

```text
projects/<name>/svg_output/001_cover.svg
projects/<name>/svg_output/002_content.svg
```

The normalized SVG must follow the same EasySlides rules as hand-written SVG:
fixed `viewBox`, inline attributes, grouped semantic objects, XML-safe text,
no CSS/runtime dependencies, and no `foreignObject`.

## Step 4: Reuse The Existing Validation And Export Path

Run the normal pipeline after normalization:

```bash
python scripts/svg_quality_checker.py <project_dir>
python scripts/total_md_split.py <project_dir>
python scripts/finalize_svg.py <project_dir>
python scripts/svg_to_pptx.py <project_dir>
```

If the checker fails, fix the normalized SVG rather than weakening the checker.
The goal is to make HTML/JSX feed the existing backend, not to make the backend
accept arbitrary browser output.

## Step 5: Promotion Criteria

Promote Path C from spike to supported workflow only after a benchmark shows:

- editable text, shapes, lines, charts, and SVG primitives survive export
- output quality is at least as good as the current SVG path for representative
  slides such as attention architecture diagrams, heatmaps, line charts, and
  dense report pages
- PowerPoint, LibreOffice, and Google Slides compatibility are not worse
- maintenance cost is lower or the authoring quality gain is large enough to
  justify the new entry layer
- the final implementation still has a single production backend

Record any promotion decision in `SKILL.md` and add focused tests or fixtures
before making the path part of the default deck-generation flow.
