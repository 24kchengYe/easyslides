#!/usr/bin/env python3
"""Lightweight SVG helpers for the L001 notebook-defense style pack."""

from __future__ import annotations

from html import escape


VIEWBOX = "0 0 1280 720"
PRIMARY = "#8B0012"
PRIMARY_DIM = "#68000E"
SURFACE = "#FFFFFF"
SURFACE_ALT = "#F9F9F9"
LINE = "#E7E6E6"
INK = "#000000"
MUTED = "#44546A"
PALE_DOT = "#FBD7B3"
FONT = "Microsoft YaHei, 微软雅黑, Arial, sans-serif"
FONT_LIGHT = "Microsoft YaHei Light, Microsoft YaHei, 微软雅黑, Arial, sans-serif"
DEFAULT_CLOSING_TITLE = "恳请老师批评指正！"


def _text(value: str) -> str:
    return escape(str(value), quote=False)


def _svg(body: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}">\n'
        f"{body}\n"
        "</svg>"
    )


def draw_l001_brand(text: str = "{{BRAND}}", *, x: int = 54, y: int = 58, anchor: str | None = None) -> str:
    """Return the small L001 brand slot used on non-cover pages."""
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text x="{x}" y="{y}"{anchor_attr} fill="{INK}" '
        f'font-family="{FONT}" font-size="18" font-weight="700">{_text(text)}</text>'
    )


def draw_l001_dots(x: int, y: int, *, cols: int = 3, rows: int = 3, gap: int = 22) -> str:
    """Return an L001 corner dot matrix."""
    circles = []
    for row in range(rows):
        for col in range(cols):
            circles.append(f'<circle cx="{x + col * gap}" cy="{y + row * gap}" r="4" opacity="0.8"/>')
    return f'<g id="corner-dots" fill="{PALE_DOT}">' + "".join(circles) + "</g>"


def draw_l001_toc(
    items: list[tuple[str, str]] | None = None,
    *,
    brand: str = "{{BRAND}}",
    toc_title: str = "{{TOC_TITLE}}",
    toc_subtitle: str = "{{TOC_SUBTITLE}}",
) -> str:
    """Return a full SVG for the strict L001-S02 table-of-contents shell."""
    if items is None:
        items = [
            ("{{ITEM_1}}", "{{ITEM_1_EN}}"),
            ("{{ITEM_2}}", "{{ITEM_2_EN}}"),
            ("{{ITEM_3}}", "{{ITEM_3_EN}}"),
            ("{{ITEM_4}}", "{{ITEM_4_EN}}"),
            ("{{ITEM_5}}", "{{ITEM_5_EN}}"),
        ]
    if len(items) != 5:
        raise ValueError("L001 TOC requires exactly five items")

    rows = []
    for idx, (title, subtitle) in enumerate(items, start=1):
        base_y = 106 + (idx - 1) * 112
        rows.append(
            f'<text x="704" y="{base_y + 48}" fill="{PRIMARY}" font-size="38" font-weight="700">{idx:02d}</text>'
            f'<rect x="765" y="{base_y}" width="2" height="60" fill="{PRIMARY}"/>'
            f'<text x="782" y="{base_y + 40}" fill="{INK}" font-size="27" font-weight="700">{_text(title)}</text>'
            f'<text x="782" y="{base_y + 78}" fill="{INK}" font-size="15">{_text(subtitle)}</text>'
        )

    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{SURFACE}"/>',
            draw_l001_brand(brand),
            draw_l001_dots(1200, 24),
            draw_l001_dots(12, 636),
            f'<rect x="0" y="233" width="507" height="255" fill="{PRIMARY}"/>',
            f'<polygon points="480,344 523,360 480,376" fill="{PRIMARY}"/>',
            f'<text x="253" y="352" text-anchor="middle" fill="{SURFACE}" font-family="{FONT}" font-size="58" font-weight="700">{_text(toc_title)}</text>',
            f'<text x="253" y="424" text-anchor="middle" fill="{SURFACE}" font-family="{FONT_LIGHT}" font-size="19" letter-spacing="3">{_text(toc_subtitle)}</text>',
            f'<g id="l001-toc-items" font-family="{FONT}">' + "".join(rows) + "</g>",
        ]
    )
    return _svg(body)


def draw_l001_section(
    *,
    section_number: str = "{{SECTION_NUMBER}}",
    part_label: str = "{{PART_LABEL}}",
    section_title: str = "{{SECTION_TITLE}}",
    section_subtitle: str = "{{SECTION_SUBTITLE}}",
    brand: str = "{{BRAND}}",
) -> str:
    """Return a full SVG for L001 chapter transition pages."""
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{SURFACE}"/>',
            draw_l001_brand(brand),
            draw_l001_dots(1200, 24),
            draw_l001_dots(12, 636),
            f'<rect x="0" y="192" width="1280" height="259" fill="{PRIMARY}"/>',
            f'<text x="443" y="394" text-anchor="middle" fill="{SURFACE}" opacity="0.14" font-family="{FONT}" font-size="220" font-weight="700">{_text(section_number)}</text>',
            f'<text x="456" y="392" text-anchor="middle" fill="{SURFACE}" font-family="{FONT}" font-size="92" font-weight="700">{_text(section_number)}</text>',
            f'<text x="456" y="424" text-anchor="middle" fill="{SURFACE}" font-family="{FONT_LIGHT}" font-size="19" letter-spacing="2">{_text(part_label)}</text>',
            f'<text x="618" y="344" fill="{SURFACE}" font-family="{FONT}" font-size="42" font-weight="700">{_text(section_title)}</text>',
            f'<text x="624" y="396" fill="{SURFACE}" font-family="{FONT_LIGHT}" font-size="15">{_text(section_subtitle)}</text>',
            (
                f'<g id="l001-mortarboard" transform="translate(1066 564)" fill="{PRIMARY}" stroke="{PRIMARY}">'
                '<path d="M0 38 L78 0 L156 38 L78 76 Z"/>'
                f'<path d="M38 54 L38 94 C62 112 94 112 118 94 L118 54 L78 73 Z" fill="{PRIMARY_DIM}" stroke="none"/>'
                f'<line x1="126" y1="44" x2="126" y2="92" stroke="{PRIMARY}" stroke-width="6"/>'
                "</g>"
            ),
        ]
    )
    return _svg(body)


def draw_l001_content_shell(
    *,
    active_section: str = "{{ACTIVE_SECTION}}",
    page_title: str = "{{PAGE_TITLE}}",
    card_title: str = "{{CARD_TITLE}}",
    body_lines: list[str] | None = None,
    number: str = "{{NO}}",
    brand: str = "{{BRAND}}",
    nav_items: list[str] | None = None,
) -> str:
    """Return a full SVG for the L001 left-nav content shell."""
    if body_lines is None:
        body_lines = ["{{BODY_LINE_1}}", "{{BODY_LINE_2}}", "{{BODY_LINE_3}}"]
    if nav_items is None:
        nav_items = ["{{NAV_ITEM_1}}", "{{NAV_ITEM_2}}", "{{NAV_ITEM_3}}", "{{NAV_ITEM_4}}"]
    if len(nav_items) != 4:
        raise ValueError("L001 content shell requires exactly four nav items")
    tspans = "".join(
        f'<tspan x="384" dy="{0 if idx == 0 else 34}">{_text(line)}</tspan>'
        for idx, line in enumerate(body_lines[:3])
    )
    nav_rows = []
    for idx, item in enumerate(nav_items):
        cy = 254 + idx * 87
        ty = cy + 5
        nav_rows.append(
            f'<circle cx="60" cy="{cy}" r="6" fill="{PRIMARY}"/>'
            f'<text x="78" y="{ty}" fill="{INK}" font-family="{FONT}" font-size="13">{_text(item)}</text>'
        )
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{SURFACE}"/>',
            f'<rect x="0" y="0" width="291" height="720" fill="{SURFACE_ALT}"/>',
            f'<rect x="0" y="159" width="291" height="65" fill="{PRIMARY}"/>',
            draw_l001_brand(brand, x=40),
            f'<text x="40" y="198" fill="{SURFACE}" font-family="{FONT}" font-size="13" font-weight="700">{_text(active_section)}</text>',
            f'<g id="nav-items" font-family="{FONT}" font-size="13" fill="{INK}">' + "".join(nav_rows) + "</g>",
            f'<rect x="336" y="98" width="12" height="38" fill="{PRIMARY}"/>',
            f'<text x="366" y="129" fill="{INK}" font-family="{FONT}" font-size="24" font-weight="700">{_text(page_title)}</text>',
            f'<rect x="336" y="170" width="760" height="350" fill="{SURFACE_ALT}"/>',
            f'<rect x="348" y="158" width="760" height="350" fill="{SURFACE}" stroke="{LINE}" stroke-width="1.5"/>',
            f'<rect x="348" y="158" width="760" height="72" fill="{PRIMARY}"/>',
            f'<text x="384" y="205" fill="{SURFACE}" font-family="{FONT}" font-size="20" font-weight="700">{_text(card_title)}</text>',
            f'<text x="384" y="282" fill="{INK}" font-family="{FONT}" font-size="16">{tspans}</text>',
            f'<rect x="1128" y="170" width="74" height="74" fill="{SURFACE}" stroke="{LINE}"/>',
            f'<text x="1165" y="214" text-anchor="middle" fill="{PRIMARY}" font-family="{FONT}" font-size="20" font-weight="700">{_text(number)}</text>',
        ]
    )
    return _svg(body)


def draw_l001_closing(
    *,
    closing_title: str = DEFAULT_CLOSING_TITLE,
    respondent: str = "{{RESPONDENT}}",
    advisor: str = "{{ADVISOR}}",
    date: str = "{{DATE}}",
    brand: str = "{{BRAND}}",
) -> str:
    """Return a full SVG for the locked L001-S27 closing shell."""
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{SURFACE}"/>',
            draw_l001_dots(12, 24),
            draw_l001_dots(1196, 636),
            draw_l001_brand(brand, x=640, y=64, anchor="middle"),
            f'<rect x="0" y="192" width="1280" height="259" fill="{PRIMARY}"/>',
            f'<text x="640" y="356" text-anchor="middle" fill="{SURFACE}" font-family="{FONT}" font-size="46" font-weight="700">{_text(closing_title)}</text>',
            f'<text x="214" y="592" fill="{INK}" font-family="{FONT}" font-size="15">{_text(respondent)}</text>',
            f'<text x="565" y="592" fill="{INK}" font-family="{FONT}" font-size="15">{_text(advisor)}</text>',
            f'<text x="930" y="592" fill="{INK}" font-family="{FONT}" font-size="15">{_text(date)}</text>',
            f'<circle cx="190" cy="587" r="8" fill="{PRIMARY}"/>',
            f'<circle cx="542" cy="587" r="8" fill="{PRIMARY}"/>',
            f'<circle cx="908" cy="587" r="8" fill="{PRIMARY}"/>',
        ]
    )
    return _svg(body)


__all__ = [
    "DEFAULT_CLOSING_TITLE",
    "PRIMARY",
    "VIEWBOX",
    "draw_l001_brand",
    "draw_l001_dots",
    "draw_l001_toc",
    "draw_l001_section",
    "draw_l001_content_shell",
    "draw_l001_closing",
]
