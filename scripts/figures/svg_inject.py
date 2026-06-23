# -*- coding: utf-8 -*-
"""
Inject a hand-authored SVG as NATIVE editable DrawingML shapes into an existing
slide of an existing .pptx, via the easyslides converter.

Author SVGs at viewBox="0 0 1280 720"  (1 SVG px = 9525 EMU = full slide 13.333x7.5in),
so converted shapes land in full-slide coordinates with NO scaling needed — just
draw the diagram where you want it on that 1280x720 canvas.

Usage (as a module):
    from figures.svg_inject import inject_svg_shapes
    inject_svg_shapes(slide, "mydiagram.svg")     # grafts shapes into slide.shapes._spTree

Pure box/arrow/text SVGs need no media wiring. If the SVG embeds <image>, this
helper warns (media not wired) — avoid images in these diagrams.
"""
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

# This file lives at easyslides/scripts/figures/svg_inject.py.
# The SVG->DrawingML converter lives at easyslides/scripts/svg_to_pptx/.
# Add the parent `scripts/` dir to sys.path so `svg_to_pptx` imports resolve,
# regardless of where easyslides is installed.
_SCRIPTS = Path(__file__).resolve().parent.parent  # .../easyslides/scripts
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from svg_to_pptx.drawingml_converter import convert_svg_to_slide_shapes  # noqa: E402
from pptx.oxml import parse_xml  # noqa: E402

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


def svg_to_shape_xml_list(svg_path):
    """Return a list of shape-XML strings (<p:sp>/<p:grpSp>/<p:pic>) from an SVG."""
    slide_xml, media_files, rel_entries, _anim = convert_svg_to_slide_shapes(
        Path(svg_path), slide_num=1, verbose=False)
    if media_files:
        print(f"  [warn] SVG produced {len(media_files)} media file(s); "
              f"images are NOT wired up by this helper. Avoid <image> in diagrams.")
    root = ET.fromstring(slide_xml)
    sp_tree = root.find(f".//{{{P_NS}}}spTree")
    out = []
    for child in list(sp_tree):
        tag = child.tag.split("}")[-1]
        if tag in ("sp", "grpSp", "pic", "graphicFrame", "cxnSp"):
            out.append(ET.tostring(child, encoding="unicode"))
    return out


def inject_svg_shapes(slide, svg_path):
    """Graft an SVG's shapes into `slide` (python-pptx slide) as native DrawingML.
    Shapes are appended to the slide's spTree (drawn on top of existing content).
    Returns the count of shapes injected.
    """
    shape_xmls = svg_to_shape_xml_list(svg_path)
    sp_tree = slide.shapes._spTree
    n = 0
    for sx in shape_xmls:
        # strip any default ElementTree ns prefixes mismatch by re-parsing via pptx
        el = parse_xml(sx)
        sp_tree.append(el)
        n += 1
    return n
