#!/usr/bin/env python3
"""Reusable SVG helpers for the Guizang editable style migration."""

from __future__ import annotations

from html import escape


VIEWBOX = "0 0 1280 720"

STYLE_A_INK = "#0A0A0B"
STYLE_A_PAPER = "#F1EFEA"
STYLE_A_PAPER_TINT = "#E8E5DE"
STYLE_A_INK_TINT = "#18181A"

STYLE_B_ACCENT = "#002FA7"
STYLE_B_PAPER = "#FAFAF8"
STYLE_B_INK = "#0A0A0A"
STYLE_B_GREY_1 = "#F0F0EE"
STYLE_B_GREY_2 = "#D4D4D2"
STYLE_B_GREY_3 = "#737373"

FONT_A_DISPLAY = "Georgia, Cambria, serif"
FONT_A_BODY = "Aptos, Arial, Microsoft YaHei, sans-serif"
FONT_MONO = "Consolas, JetBrains Mono, monospace"
FONT_B = "Helvetica Neue, Inter, Arial, Microsoft YaHei, sans-serif"


def _text(value: str) -> str:
    return escape(str(value), quote=False)


def _svg(body: str, *, style: str, page: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VIEWBOX}" '
        f'data-style="{style}" data-page="{page}">\n'
        f"{body}\n"
        "</svg>"
    )


def draw_style_a_cover(
    *,
    title: str = "{{TITLE}}",
    title_line_2: str = "{{TITLE_LINE_2}}",
    subtitle: str = "{{SUBTITLE}}",
    kicker: str = "{{KICKER}}",
    meta: str = "{{META}}",
) -> str:
    """Return an editable SVG cover shell for Guizang Style A."""
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{STYLE_A_PAPER}"/>',
            f'<rect x="0" y="0" width="1280" height="22" fill="{STYLE_A_INK}"/>',
            f'<rect x="64" y="84" width="1152" height="552" fill="none" stroke="{STYLE_A_INK}" stroke-width="2"/>',
            f'<text x="96" y="126" fill="{STYLE_A_INK_TINT}" font-family="{FONT_MONO}" font-size="14" letter-spacing="3">{_text(kicker)}</text>',
            f'<text x="96" y="312" fill="{STYLE_A_INK}" font-family="{FONT_A_DISPLAY}" font-size="92" font-weight="700">'
            f'<tspan x="96" dy="0">{_text(title)}</tspan><tspan x="96" dy="96">{_text(title_line_2)}</tspan></text>',
            f'<line x1="96" y1="468" x2="768" y2="468" stroke="{STYLE_A_INK}" stroke-width="3"/>',
            f'<text x="96" y="518" fill="{STYLE_A_INK_TINT}" font-family="{FONT_A_BODY}" font-size="24">{_text(subtitle)}</text>',
            f'<text x="96" y="588" fill="{STYLE_A_INK_TINT}" font-family="{FONT_MONO}" font-size="13">{_text(meta)}</text>',
        ]
    )
    return _svg(body, style="guizang-style-a", page="cover")


def draw_style_a_content(
    *,
    page_title: str = "{{PAGE_TITLE}}",
    kicker: str = "{{KICKER}}",
    callout: str = "{{CALLOUT}}",
    body_lines: list[str] | None = None,
) -> str:
    """Return an editable SVG content shell for Guizang Style A."""
    if body_lines is None:
        body_lines = ["{{BODY_LINE_1}}", "{{BODY_LINE_2}}", "{{BODY_LINE_3}}"]
    tspans = "".join(
        f'<tspan x="680" dy="{0 if idx == 0 else 34}">{_text(line)}</tspan>'
        for idx, line in enumerate(body_lines[:4])
    )
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{STYLE_A_PAPER}"/>',
            f'<text x="64" y="54" fill="{STYLE_A_INK_TINT}" font-family="{FONT_MONO}" font-size="12" letter-spacing="3">{_text(kicker)}</text>',
            f'<text x="64" y="122" fill="{STYLE_A_INK}" font-family="{FONT_A_DISPLAY}" font-size="42" font-weight="700">{_text(page_title)}</text>',
            f'<line x1="64" y1="150" x2="1216" y2="150" stroke="{STYLE_A_INK}" stroke-width="1"/>',
            f'<rect x="64" y="196" width="508" height="326" fill="{STYLE_A_PAPER_TINT}"/>',
            f'<rect x="86" y="218" width="464" height="282" fill="{STYLE_A_PAPER}" stroke="{STYLE_A_INK}" stroke-width="1.5"/>',
            f'<rect x="640" y="196" width="576" height="326" fill="none" stroke="{STYLE_A_INK}" stroke-width="1.5"/>',
            f'<text x="680" y="254" fill="{STYLE_A_INK}" font-family="{FONT_A_BODY}" font-size="24" font-weight="700">{_text(callout)}</text>',
            f'<text x="680" y="316" fill="{STYLE_A_INK_TINT}" font-family="{FONT_A_BODY}" font-size="20">{tspans}</text>',
        ]
    )
    return _svg(body, style="guizang-style-a", page="content")


def draw_style_b_cover(
    *,
    title: str = "{{TITLE}}",
    title_line_2: str = "{{TITLE_LINE_2}}",
    subtitle: str = "{{SUBTITLE}}",
) -> str:
    """Return an editable SVG cover shell for Guizang Style B Swiss mode."""
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{STYLE_B_ACCENT}"/>',
            f'<text x="64" y="348" fill="#FFFFFF" font-family="{FONT_B}" font-size="104" font-weight="200">'
            f'<tspan x="64" dy="0">{_text(title)}</tspan><tspan x="64" dy="104">{_text(title_line_2)}</tspan></text>',
            '<line x1="64" y1="544" x2="1216" y2="544" stroke="#FFFFFF" stroke-width="1"/>',
            f'<text x="64" y="596" fill="#FFFFFF" font-family="{FONT_B}" font-size="24" font-weight="300">{_text(subtitle)}</text>',
        ]
    )
    return _svg(body, style="guizang-style-b", page="cover")


def draw_style_b_image_hero(
    *,
    page_title: str = "{{PAGE_TITLE}}",
    kpis: tuple[str, str, str] = ("{{KPI_1}}", "{{KPI_2}}", "{{KPI_3}}"),
    caption: str = "{{CAPTION}}",
) -> str:
    """Return an editable S22-compatible image hero shell for Swiss mode."""
    body = "\n".join(
        [
            f'<rect width="1280" height="720" fill="{STYLE_B_PAPER}"/>',
            f'<rect x="64" y="56" width="1152" height="330" fill="{STYLE_B_GREY_1}" stroke="{STYLE_B_GREY_2}"/>',
            f'<rect x="96" y="88" width="430" height="116" fill="#FFFFFF"/>',
            f'<text x="120" y="150" fill="{STYLE_B_INK}" font-family="{FONT_B}" font-size="36" font-weight="300">{_text(page_title)}</text>',
            f'<text x="64" y="426" fill="{STYLE_B_GREY_3}" font-family="{FONT_MONO}" font-size="12">{_text(caption)}</text>',
            f'<rect x="64" y="480" width="352" height="120" fill="#FFFFFF" stroke="{STYLE_B_GREY_2}"/>',
            f'<rect x="464" y="480" width="352" height="120" fill="{STYLE_B_ACCENT}"/>',
            f'<rect x="864" y="480" width="352" height="120" fill="#FFFFFF" stroke="{STYLE_B_GREY_2}"/>',
            f'<text x="96" y="548" fill="{STYLE_B_INK}" font-family="{FONT_B}" font-size="42" font-weight="200">{_text(kpis[0])}</text>',
            f'<text x="496" y="548" fill="#FFFFFF" font-family="{FONT_B}" font-size="42" font-weight="200">{_text(kpis[1])}</text>',
            f'<text x="896" y="548" fill="{STYLE_B_INK}" font-family="{FONT_B}" font-size="42" font-weight="200">{_text(kpis[2])}</text>',
        ]
    )
    return _svg(body, style="guizang-style-b", page="image-hero")


__all__ = [
    "STYLE_A_INK",
    "STYLE_B_ACCENT",
    "VIEWBOX",
    "draw_style_a_cover",
    "draw_style_a_content",
    "draw_style_b_cover",
    "draw_style_b_image_hero",
]
