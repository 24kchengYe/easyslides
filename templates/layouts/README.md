# Academic Layout Template Library (5 Active Templates)

`templates/layouts/` is the active, discoverable layout library for academic
PPT work. It is intentionally slim: old brand, government, enterprise, special
effect, and retired slot-guided packs are no longer part of the active library.

- **Slim index**: [layouts_index.json](./layouts_index.json) lists only active
  template IDs used for discovery.
- **Selection rule**: templates are opt-in. A deck uses a layout only when the
  user gives an explicit directory path such as
  `templates/layouts/literature_minimal/`. Bare names remain discovery hints, not
  triggers.
- **Legacy aliases**: [aliases.json](./aliases.json) maps old IDs such as
  `defense_s01` and `literature_s01` to their maintained replacements.

## Quick Template Index

<!-- quick-index:begin -->
| Template Name | Category | Use Cases | Primary Color | Design Tone |
|---------------|----------|-----------|---------------|-------------|
| `academic_general` | General | Research talks, course reports, progress reviews, paper explainers, scholarly exchange | `#003366` | Professional, rigorous, audience-facing, AST/SCQA-guided |
| `academic_scqa` | Scenario | Academic reports, laboratory technical briefings, research progress reviews, project reviews | `#0046A5` | Formal, institutional, data-driven, audience-facing, AST/SCQA-structured |
| `defense_leftnav` | Scenario | Thesis defense, graduation defense, proposal defense, research progress reports | `#8B0012` | Compact, formal, burgundy, left navigation, reusable |
| `defense_topnav` | Scenario | Thesis defense, proposal defense, opening defense, research progress reports | `#183A6A` | Academic, calm, blue-white, structured, source-faithful |
| `literature_minimal` | Scenario | Literature reports, paper reading, academic reports, research progress reviews | `#0D5DBE` | Minimal, blue-white, restrained, spacious, academic |
<!-- quick-index:end -->

## Active Families

### Core Academic

| Template | Role |
|----------|------|
| `academic_general` | Neutral general academic shells with shared Audience-State-Transfer and SCQA orchestration. |
| `academic_scqa` | Blue-cyan structured academic and technical report shells with AST/SCQA body-variant guidance. |
| `defense_leftnav` | Compact left-navigation thesis defense shells with wine, academic-blue, academic-purple, and academic-green palettes. |
| `defense_topnav` | Academic-blue thesis defense shells with dynamic top navigation and flexible content canvas. |
| `literature_minimal` | Classic five-page minimal blue literature report shells. |

## Template Modes

| Mode | Use When | Core Contract |
|------|----------|---------------|
| `classic` | The template is a flexible visual style with reusable shells. | `design_spec.md` plus canonical placeholders. |
| `mirror` | A source PPTX deck must be visually preserved. | Fixed SVG roster, replace only existing text/image content. |
| `slot_guided_mirror` | A mirror template also needs story-role page selection. | `layouts.json`, `page_catalog.json`, `rules.md`, optional `story_structure.json`. |

The current active academic library uses compact classic shells for the defense,
academic-report, and literature-report families. Retired slot-guided packs should stay outside
`templates/layouts/` unless a future use case justifies restoring them.

## Development

Create new active templates only when they serve repeatable academic scenarios.
Run these checks after editing a template:

```bash
python scripts/svg_quality_checker.py templates/layouts/<template_id> --template-mode --format ppt169
python scripts/register_template.py <template_id>
```

`layouts_index.json` is a discovery index, not a routing gate. A template kept
outside `templates/layouts/` can still be used when the user provides its
explicit path.
