# L001 Notebook Defense Rules

This is a minimal EasySlides style pack migrated from EasyPPT's locked
`l001_notebook_defense` mode. Keep it small: do not copy the full EasyPPT asset
registry into this project.

## Hard Rules

- The primary wine red is exactly `#8B0012`.
- Do not use the academic blue `#003366` in this style pack.
- SVGs must use `viewBox="0 0 1280 720"`.
- Use `Microsoft YaHei` / `微软雅黑` for visible text.
- TOC, section, and closing pages keep the original L001 band proportions.
- Closing title defaults to `恳请老师批评指正！` unless the user explicitly asks
  for different wording.
- Run `python scripts/validate_l001.py templates/style_packs/l001_notebook_defense` after
  editing this pack.

## Files

- `design_tokens.json`: colors, fonts, typography roles, shape roles, and core
  coordinate contracts.
- `layouts.json`: five lightweight page shells mapped back to L001 source
  layouts.
- `01_cover.svg` to `05_closing.svg`: editable SVG templates for EasySlides'
  SVG-to-PPTX path.
- `scripts/validate_l001.py`: repository-local style pack validator.
