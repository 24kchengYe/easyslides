# -*- coding: utf-8 -*-
"""
easyslides figures module
=========================

Three ways to make a figure for a slide or paper, each with its own tool:

1. DATA figures (real numbers -> matplotlib): use `figstyle` (talk/projector theme)
   or `style_presets` (journal themes) + `figure_export`. Produces PNG/PDF/EPS.
       from figures import figstyle, style_presets, figure_export

2. CONCEPT / flow / framework diagrams (boxes + arrows + text, NO data):
   hand-author an SVG at viewBox="0 0 1280 720" and inject it as NATIVE editable
   DrawingML shapes via `svg_inject.inject_svg_shapes(slide, "diagram.svg")`.
   Template examples live in ../../templates/figures/svg_examples/.
       from figures.svg_inject import inject_svg_shapes
       from figures import gloss_helpers   # title blocks, dividers, gloss boxes

3. Complex illustration / cover art: use the skill's AI image generation
   (scripts/image_gen.py) — raster, not editable.

See references/scientific-figures.md for the full decision tree and the house rules
(numbers must be source-traceable, no clipping, symmetry, don't split shared flows).
"""

__all__ = [
    "figstyle",
    "style_presets",
    "figure_export",
    "color_palettes",
    "svg_inject",
    "gloss_helpers",
]
