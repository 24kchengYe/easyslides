# Guizang Migration Notes

Source: https://github.com/op7418/guizang-ppt-skill at commit `3d87acc`.

## What Carries Over

- Style A: editorial ink/paper themes, magazine chrome, large narrative type,
  framed image slots, and alternating light/dark pacing.
- Style B: Swiss grid discipline, single saturated accent, hairline dividers,
  square fills, and the upstream `S01-S22` registered layout vocabulary.
- Image rules: generated images are treated as slide assets only; they should
  not include page titles, footers, navigation chrome, borders, or logos.

## What Changes

- HTML sections become SVG page shells.
- CSS variables become locked JSON tokens.
- Browser layout and WebGL/canvas effects are omitted.
- Animation recipes are not migrated in this pack; PPT animations should be
  added through the EasySlides animation configuration layer when needed.
- Text remains SVG text so the PPTX exporter can create editable DrawingML text.

## Current Scope

This is a first native migration layer, not a full one-to-one reconstruction of
every upstream HTML layout. Style A's 10 layout roles are covered by four shell
families. Style B's `S01-S22` layout IDs are preserved in `layouts.json`,
mapped into five editable shell families, and also generated as 22 native SVG
layout skeletons in `swiss/`.

## Harness Contract

Guizang can now be selected as a reusable `spec_lock.md` style pack instead of
being copied into a project-local template folder:

```markdown
## style_pack
- package: guizang_ppt
- variant: style_b_swiss
- theme: ikb
- layout_source: templates/style_packs/guizang_ppt
- validator: scripts/validate_guizang.py

## page_layouts
- P01: S01
- P02: S08
- P03: swiss/S22_image_hero
```

The contract parser resolves those layout IDs to real SVG files and fails on
unknown variants, themes, or layout names:

```bash
python scripts/style_pack_contract.py <project_path>/spec_lock.md --json
python scripts/validate_guizang.py templates/style_packs/guizang_ppt --spec-lock <project_path>/spec_lock.md --json
```

Regenerate the Swiss skeletons after changing
`scripts/generate_guizang_swiss_layouts.py`:

```bash
python scripts/generate_guizang_swiss_layouts.py
```

## Validation

Run both validators after edits:

```bash
python scripts/validate_guizang.py templates/style_packs/guizang_ppt
python scripts/svg_quality_checker.py templates/style_packs/guizang_ppt
```
