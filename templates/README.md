# Template Resources

## Directory Map

- `layouts/`: page layout packs only.
- `style_packs/`: reusable visual systems and editable-PPT style migrations.
- `charts/`: chart, diagram, and framework SVG templates.
- `icons/`: shared icon libraries.
- `reference/`: reusable authoring references and generated lookup assets.

## Design Specification & Outline Reference

`design_spec_reference.md` is an all-in-one reference template for defining:
1.  **Visual Specifications**: Canvas dimensions, color scheme, typography, layout principles
2.  **Content Outline**: Slide-by-slide page structure planning
3.  **Technical Constraints**: Hard requirements for SVG generation and PPT compatibility

[View Design Spec Reference](./reference/design_spec_reference.md)

## Page Layout Templates

The `layouts/` directory is now a slim academic-only active library. It keeps
five repeatable academic template packs: `academic_general`, `academic_scqa`,
`defense_leftnav`, `defense_topnav`, and `literature_minimal`.

The broader brand, government, enterprise, domain-specific, and special-style PPT Master packs
were moved out of the active library for review because EasySlides is focused
on academic scenarios.

- **Human browsing**: [layouts/README.md](./layouts/README.md)
- **Slim lookup (discovery only)**: [layouts/layouts_index.json](./layouts/layouts_index.json) — used to answer "what academic templates exist?". Step 3 triggers on an explicit directory path supplied by the user, not on names from this index.

## Local Style Packs

These are lightweight editable-PPT style migrations kept outside
`templates/layouts/` so they do not change the PPT Master page-template index:

- `style_packs/l001_notebook_defense/`: wine-red notebook defense style pack.
- `style_packs/guizang_ppt/`: Guizang HTML deck style migration, covering Style A
  editorial ink and Style B Swiss internationalism as native SVG shells,
  including 22 Swiss `S01-S22` skeletons under `swiss/`. It can be
  bound through `spec_lock.md` `style_pack` and validated with
  `scripts/style_pack_contract.py`.

## Template Asset Bank

Use a Template Asset Bank when the source is a large set of real `.pptx`
template files and the goal is manual-template-substitution quality: fixed page
structure, fixed decorative geometry, and only text/image/chart data replaced.

Build it from `pptx_template_import.py` workspaces:

```bash
python scripts/template_asset_bank.py build tmp/template_imports/<template_id> \
  --output templates/reference/template_asset_bank.json
```

The bank is a module harness, not a style pack. Each source slide becomes an
exact-reuse module with `flat_svg`, `layered_svg`, slot metadata, and explicit
allowed/forbidden edit rules. See
[`workflows/template-asset-bank.md`](../workflows/template-asset-bank.md).

## Visualization Templates

The `charts/` directory contains 71 standardized visualization templates. For backward compatibility, the directory name remains `charts/`, but its scope includes charts, infographics, process diagrams, relationship diagrams, strategic frameworks, and system architecture diagrams:

- KPI Cards
- Bar Chart / Stacked Bar Chart
- Line Chart / Dual-Axis Line Chart
- Donut Chart
- Radar Chart
- Funnel Chart
- Matrix (2x2)
- Timeline
- Gantt Chart
- Process Flow
- Org Chart
- Layered Architecture / Module Composition / Hub with Described Spokes / Pipeline with Stages / Client-Server Flow

- **Library index (single source of truth)**: [charts/charts_index.json](./charts/charts_index.json)
- **Directory overview**: [charts/README.md](./charts/README.md)

## Icon Library

The `icons/` directory contains 11,600+ vector icons across six libraries:

| Library | Style | Count |
|---------|-------|-------|
| `chunk-filled` | fill / straight-line geometry | 640 |
| `lucide` | stroke / clean interface icons | 3 |
| `tabler-filled` | fill / bezier-curve forms | 1000+ |
| `tabler-outline` | stroke / line | 5000+ |
| `phosphor-duotone` | duotone / single color + 0.2 opacity backplate | 1200+ |
| `simple-icons` | brand logos (company / product marks) | 3400+ |

- **Usage & style rules**: [icons/README.md](./icons/README.md)
- **Search icons**: `ls templates/icons/<library>/ | grep <keyword>`
