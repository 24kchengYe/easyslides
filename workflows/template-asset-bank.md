---
description: Build a Template Asset Bank from many real PPTX templates for exact slide-module reuse
---

# Template Asset Bank Workflow

Use this workflow when the user has many polished `.pptx` template files and
wants AI-generated decks to look like manual template substitution: fixed page
structure, fixed decorative geometry, and only text/image/chart data replaced.

This is different from a Style Pack. A Style Pack teaches the agent a visual
language. A Template Asset Bank gives the agent real pages to choose from and
reuse as locked modules.

## Contract

Primary mode: `exact_template_reuse`

The agent may:

- select a source slide module by content fit
- copy its flat SVG as the starting point for a project page
- replace visible text inside existing text elements
- replace images inside existing picture/media slots
- update chart/table labels only when the original module already contains
  that structure

The agent must not:

- move, resize, recolor, or delete fixed geometry
- invent a new grid or decorative system inside a chosen module
- turn a real template module into a free-form Style Pack page

If content does not fit a module, choose another module, split the content
across pages, or warn before simplifying.

## Step 1: Import PPTX Templates

Run the normal PPTX import for each source template:

```bash
python scripts/pptx_template_import.py "path/to/premium.pptx" \
  --output "tmp/template_imports/premium" \
  --inheritance-mode both
```

Required import outputs:

- `manifest.json`
- `svg-flat/slide_NN.svg`
- `svg/slide_NN.svg`
- `assets/`

For exact reuse, `svg-flat/slide_NN.svg` is the authoring reference because it
contains what PowerPoint shows: master, layout, and slide-local content in one
self-contained page.

## Step 2: Build The Asset Bank

Build a single searchable manifest from one or more import workspaces:

```bash
python scripts/template_asset_bank.py build \
  tmp/template_imports/premium \
  tmp/template_imports/annual_report \
  --output templates/reference/template_asset_bank.json \
  --bank-id local_pptx_template_bank
```

The generated JSON contains:

- bank-level reuse policy
- one `template_id` per source PPTX
- one page module per source slide
- source paths for flat and layered SVGs
- slide type, text samples, asset references, and rough metrics
- placeholder-derived slots from the source layout/master
- allowed and forbidden edit rules per module

## Step 3: Use During Deck Generation

When planning a deck:

1. Read `templates/reference/template_asset_bank.json`.
2. Match each content page to a module by `page_type`, `text_samples`,
   `search_hints`, and slot count.
3. Write the selected module basename into the project `spec_lock.md`
   `page_layouts` equivalent, or record it in the page plan.
4. During SVG generation, copy the module's `source.flat_svg`.
5. Edit text/image content in place while preserving fixed geometry.

Fallback order:

1. Exact Template Reuse from Template Asset Bank.
2. Mirror-mode template page from `templates/layouts/<template_id>/`.
3. PPT Master template shell from `templates/layouts/`.
4. Style Pack only when no exact page module fits.

## Validation

Focused tests:

```bash
python tests/test_template_asset_bank.py -v
```

CLI smoke check:

```bash
python scripts/template_asset_bank.py --help
python scripts/template_asset_bank.py build tmp/template_imports/premium --output tmp/template_asset_bank.json
```
