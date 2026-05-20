#!/usr/bin/env python3
"""Generate native SVG shells for Guizang Swiss S01-S22 layouts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "templates" / "style_packs" / "guizang_ppt" / "swiss"

PAPER = "#FAFAF8"
INK = "#0A0A0A"
GREY_1 = "#F0F0EE"
GREY_2 = "#D4D4D2"
GREY_3 = "#737373"
ACCENT = "#002FA7"
WHITE = "#FFFFFF"
FONT = "Helvetica Neue, Inter, Arial, Microsoft YaHei, sans-serif"
MONO = "Consolas, JetBrains Mono, monospace"


LAYOUTS = {
    "S01": ("index_cover", "Index Cover"),
    "S02": ("vertical_timeline_kpi", "Vertical Timeline + KPI"),
    "S03": ("split_statement", "Split Statement"),
    "S04": ("six_cells", "Six Cells"),
    "S05": ("three_layers", "Three Layers"),
    "S06": ("kpi_tower", "KPI Tower"),
    "S07": ("horizontal_bar", "Horizontal Bar"),
    "S08": ("duo_compare", "Duo Compare"),
    "S09": ("dot_matrix_statement", "Dot Matrix Statement"),
    "S10": ("split_closing", "Split Closing"),
    "S11": ("horizontal_timeline", "Horizontal Timeline"),
    "S12": ("manifesto_ink_banner", "Manifesto + Ink Banner"),
    "S13": ("three_forces", "Three Forces"),
    "S14": ("loop_form", "Loop Form"),
    "S15": ("matrix_hero_stat", "Matrix + Hero Stat"),
    "S16": ("multi_card_brief", "Multi-card Brief"),
    "S17": ("system_diagram", "System Diagram"),
    "S18": ("why_now", "Why Now"),
    "S19": ("four_cards", "Four Cards"),
    "S20": ("stacked_kpi_ledger", "Stacked KPI Ledger"),
    "S21": ("tech_spec_sheet", "Tech Spec Sheet"),
    "S22": ("image_hero", "Image Hero"),
}


def slot(name: str) -> str:
    return "{{" + name + "}}"


def svg(layout_id: str, title: str, body: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" '
        f'data-style="guizang-style-b" data-layout="{layout_id}" data-layout-name="{title}">\n'
        f'  <rect id="background" width="1280" height="720" fill="{PAPER}"/>\n'
        f"{body}\n"
        "</svg>\n"
    )


def chrome(layout_id: str) -> str:
    return (
        f'  <text id="chrome-left" x="64" y="56" fill="{GREY_3}" font-family="{MONO}" font-size="12" letter-spacing="3">{{{{KICKER}}}}</text>\n'
        f'  <text id="chrome-right" x="1216" y="56" text-anchor="end" fill="{GREY_3}" font-family="{MONO}" font-size="12">{layout_id} · {{{{PAGE_NUM}}}}</text>\n'
        f'  <rect id="chrome-rule" x="64" y="84" width="1152" height="1" fill="{GREY_2}"/>\n'
        f'  <rect id="chrome-accent" x="64" y="84" width="112" height="3" fill="{ACCENT}"/>'
    )


def title_block(y: int = 140, size: int = 48) -> str:
    return (
        f'  <text id="page-title" x="64" y="{y}" fill="{INK}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="300">{{{{PAGE_TITLE}}}}</text>'
    )


def card(x: int, y: int, w: int, h: int, label: str, *, fill: str = GREY_1, text: str = INK) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{GREY_2}"/>'
        f'<text x="{x + 24}" y="{y + 52}" fill="{text}" font-family="{FONT}" font-size="24" font-weight="300">{label}</text>'
    )


def s01() -> str:
    rows = []
    for idx, y in enumerate((132, 300, 468), start=1):
        rows.append(
            f'<line x1="64" y1="{y - 34}" x2="1216" y2="{y - 34}" stroke="{GREY_2}"/>'
            f'<text x="64" y="{y + 44}" fill="{ACCENT}" font-family="{MONO}" font-size="86" font-weight="300">{idx:02d}</text>'
            f'<text x="292" y="{y + 28}" fill="{INK}" font-family="{FONT}" font-size="54" font-weight="200">{slot(f"ROW_{idx}_TITLE")}</text>'
            f'<text x="296" y="{y + 72}" fill="{GREY_3}" font-family="{FONT}" font-size="18">{slot(f"ROW_{idx}_DESC")}</text>'
        )
    return svg("S01", "Index Cover", "\n".join([chrome("S01"), '  <g id="index-rows">' + "".join(rows) + "</g>"]))


def s02() -> str:
    ticks = []
    for idx, y in enumerate((216, 292, 368, 444), start=1):
        ticks.append(
            f'<circle cx="190" cy="{y}" r="9" fill="{ACCENT}"/>'
            f'<text x="224" y="{y + 7}" fill="{INK}" font-family="{FONT}" font-size="22">{slot(f"MILESTONE_{idx}")}</text>'
        )
    kpis = []
    for idx, x in enumerate((560, 724, 888, 1052), start=1):
        kpis.append(
            f'<rect x="{x}" y="508" width="132" height="98" fill="{GREY_1}" stroke="{GREY_2}"/>'
            f'<text x="{x + 18}" y="560" fill="{ACCENT}" font-family="{FONT}" font-size="36" font-weight="200">{slot(f"KPI_{idx}")}</text>'
        )
    body = "\n".join([chrome("S02"), title_block(), f'  <g id="timeline-v"><line x1="190" y1="190" x2="190" y2="470" stroke="{GREY_2}" stroke-width="2"/>' + "".join(ticks) + "</g>", '  <g id="kpi-row">' + "".join(kpis) + "</g>"])
    return svg("S02", "Vertical Timeline + KPI", body)


def s03() -> str:
    body = "\n".join([
        f'  <rect id="left-half" x="0" y="0" width="640" height="720" fill="{ACCENT}"/>',
        f'  <rect id="right-half" x="640" y="0" width="640" height="720" fill="{GREY_1}"/>',
        f'  <text id="statement-left" x="64" y="312" fill="{WHITE}" font-family="{FONT}" font-size="82" font-weight="200"><tspan x="64" dy="0">{{{{STATEMENT}}}}</tspan><tspan x="64" dy="88">{{{{STATEMENT_LINE_2}}}}</tspan></text>',
        f'  <text id="statement-note" x="704" y="220" fill="{INK}" font-family="{FONT}" font-size="28" font-weight="300"><tspan x="704" dy="0">{{{{NOTE_LINE_1}}}}</tspan><tspan x="704" dy="44">{{{{NOTE_LINE_2}}}}</tspan><tspan x="704" dy="44">{{{{NOTE_LINE_3}}}}</tspan></text>',
    ])
    return svg("S03", "Split Statement", body)


def s04() -> str:
    cells = []
    for row, y in enumerate((214, 414)):
        for col, x in enumerate((64, 448, 832), start=1):
            idx = row * 3 + col
            cells.append(card(x, y, 336, 156, slot(f"CELL_{idx}")))
    return svg("S04", "Six Cells", "\n".join([chrome("S04"), title_block(), '  <g id="six-cells">' + "".join(cells) + "</g>"]))


def s05() -> str:
    layers = []
    for idx, y in enumerate((210, 338, 466), start=1):
        fill = ACCENT if idx == 2 else GREY_1
        text = WHITE if idx == 2 else INK
        layers.append(
            f'<rect x="168" y="{y}" width="{944 - idx * 64}" height="84" fill="{fill}" stroke="{GREY_2}"/>'
            f'<text x="208" y="{y + 52}" fill="{text}" font-family="{FONT}" font-size="28" font-weight="300">{slot(f"LAYER_{idx}")}</text>'
        )
    return svg("S05", "Three Layers", "\n".join([chrome("S05"), title_block(), '  <g id="three-layers">' + "".join(layers) + "</g>"]))


def s06() -> str:
    bars = []
    for idx, (x, h) in enumerate(zip((610, 746, 882, 1018), (120, 190, 260, 340)), start=1):
        bars.append(
            f'<rect x="{x}" y="{560 - h}" width="92" height="{h}" fill="{ACCENT if idx == 4 else GREY_1}" stroke="{GREY_2}"/>'
            f'<text x="{x + 46}" y="606" text-anchor="middle" fill="{INK}" font-family="{MONO}" font-size="12">{slot(f"KPI_{idx}")}</text>'
        )
    body = "\n".join([chrome("S06"), title_block(), f'  <text id="side-note" x="64" y="232" fill="{GREY_3}" font-family="{FONT}" font-size="22">{{{{SIDE_NOTE}}}}</text>', '  <g id="kpi-tower">' + "".join(bars) + "</g>"])
    return svg("S06", "KPI Tower", body)


def s07() -> str:
    bars = []
    for idx, (y, w) in enumerate(zip((226, 304, 382, 460, 538), (860, 720, 600, 480, 340)), start=1):
        bars.append(
            f'<text x="64" y="{y + 24}" fill="{INK}" font-family="{FONT}" font-size="20">{slot(f"BAR_{idx}_LABEL")}</text>'
            f'<rect x="320" y="{y}" width="{w}" height="42" fill="{ACCENT if idx == 1 else GREY_1}" stroke="{GREY_2}"/>'
        )
    return svg("S07", "Horizontal Bar", "\n".join([chrome("S07"), title_block(), '  <g id="horizontal-bars">' + "".join(bars) + "</g>"]))


def s08() -> str:
    body = "\n".join([
        chrome("S08"),
        title_block(),
        f'  <g id="duo-compare"><rect x="64" y="220" width="512" height="360" fill="{GREY_1}" stroke="{GREY_2}"/>'
        f'<rect x="704" y="220" width="512" height="360" fill="{GREY_1}" stroke="{GREY_2}"/>'
        f'<line x1="640" y1="206" x2="640" y2="610" stroke="{ACCENT}" stroke-width="2"/>'
        f'<text x="96" y="292" fill="{INK}" font-family="{FONT}" font-size="34" font-weight="300">{{{{LEFT_TITLE}}}}</text>'
        f'<text x="736" y="292" fill="{INK}" font-family="{FONT}" font-size="34" font-weight="300">{{{{RIGHT_TITLE}}}}</text></g>',
    ])
    return svg("S08", "Duo Compare", body)


def s09() -> str:
    dots = []
    for row in range(6):
        for col in range(9):
            dots.append(f'<rect x="{920 + col * 28}" y="{180 + row * 28}" width="9" height="9" fill="{ACCENT}"/>')
    body = "\n".join([
        chrome("S09"),
        f'  <text id="dot-statement" x="64" y="310" fill="{INK}" font-family="{FONT}" font-size="82" font-weight="200"><tspan x="64" dy="0">{{{{STATEMENT}}}}</tspan><tspan x="64" dy="88">{{{{STATEMENT_LINE_2}}}}</tspan></text>',
        '  <g id="dot-matrix">' + "".join(dots) + "</g>",
    ])
    return svg("S09", "Dot Matrix Statement", body)


def s10() -> str:
    body = "\n".join([
        f'  <rect id="closing-left" x="0" y="0" width="640" height="720" fill="{ACCENT}"/>',
        f'  <text id="closing-title" x="64" y="336" fill="{WHITE}" font-family="{FONT}" font-size="84" font-weight="200">{{{{CLOSING_TITLE}}}}</text>',
        f'  <g id="closing-list" font-family="{FONT}" font-size="24" fill="{INK}"><text x="704" y="220">{{{{POINT_1}}}}</text><line x1="704" y1="252" x2="1160" y2="252" stroke="{GREY_2}"/><text x="704" y="340">{{{{POINT_2}}}}</text><line x1="704" y1="372" x2="1160" y2="372" stroke="{GREY_2}"/><text x="704" y="460">{{{{POINT_3}}}}</text></g>',
    ])
    return svg("S10", "Split Closing", body)


def s11() -> str:
    nodes = []
    for idx, x in enumerate((140, 360, 580, 800, 1020), start=1):
        nodes.append(f'<circle cx="{x}" cy="390" r="12" fill="{ACCENT}"/><text x="{x}" y="452" text-anchor="middle" fill="{INK}" font-family="{FONT}" font-size="18">{slot(f"STEP_{idx}")}</text>')
    body = "\n".join([chrome("S11"), title_block(), f'  <g id="timeline-h"><line x1="140" y1="390" x2="1020" y2="390" stroke="{GREY_2}" stroke-width="2"/>' + "".join(nodes) + "</g>"])
    return svg("S11", "Horizontal Timeline", body)


def s12() -> str:
    body = "\n".join([
        chrome("S12"),
        f'  <text id="manifesto" x="64" y="300" fill="{INK}" font-family="{FONT}" font-size="76" font-weight="200"><tspan x="64" dy="0">{{{{MANIFESTO}}}}</tspan><tspan x="64" dy="84">{{{{MANIFESTO_LINE_2}}}}</tspan></text>',
        f'  <rect id="ink-banner" x="0" y="548" width="1280" height="112" fill="{INK}"/>',
        f'  <text id="banner-text" x="64" y="616" fill="{WHITE}" font-family="{FONT}" font-size="28" font-weight="300">{{{{BANNER_TEXT}}}}</text>',
    ])
    return svg("S12", "Manifesto + Ink Banner", body)


def s13() -> str:
    cards = "".join(card(690, y, 480, 98, slot(f"FORCE_{idx}")) for idx, y in enumerate((218, 350, 482), start=1))
    body = "\n".join([
        chrome("S13"),
        f'  <g id="three-forces"><rect x="64" y="190" width="520" height="390" fill="{INK}"/>'
        f'<text x="104" y="340" fill="{WHITE}" font-family="{FONT}" font-size="64" font-weight="200">{{{{HERO_FORCE}}}}</text>'
        f'{cards}</g>',
    ])
    return svg("S13", "Three Forces", body)


def s14() -> str:
    steps = "".join(card(64, y, 384, 74, slot(f"STEP_{idx}")) for idx, y in enumerate((214, 312, 410, 508), start=1))
    body = "\n".join([
        chrome("S14"),
        title_block(),
        f'  <g id="loop-form">{steps}<circle cx="836" cy="382" r="118" fill="none" stroke="{ACCENT}" stroke-width="18"/>'
        f'<circle cx="994" cy="382" r="118" fill="none" stroke="{GREY_2}" stroke-width="18"/>'
        f'<line x1="918" y1="264" x2="918" y2="500" stroke="{INK}" stroke-width="1"/></g>',
    ])
    return svg("S14", "Loop Form", body)


def s15() -> str:
    cells = []
    for row, y in enumerate((220, 298)):
        for col, x in enumerate((64, 256, 448, 640, 832, 1024), start=1):
            idx = row * 6 + col
            cells.append(f'<rect x="{x}" y="{y}" width="160" height="52" fill="{GREY_1}" stroke="{GREY_2}"/><text x="{x + 14}" y="{y + 34}" fill="{INK}" font-family="{MONO}" font-size="11">{slot(f"M{idx}")}</text>')
    body = "\n".join([chrome("S15"), title_block(), '  <g id="matrix-grid">' + "".join(cells) + f'</g>  <text id="hero-stat" x="64" y="590" fill="{ACCENT}" font-family="{FONT}" font-size="112" font-weight="200">{{{{HERO_STAT}}}}</text>'])
    return svg("S15", "Matrix + Hero Stat", body)


def s16() -> str:
    cells = []
    for row, y in enumerate((214, 388)):
        for col, x in enumerate((64, 448, 832), start=1):
            idx = row * 3 + col
            cells.append(card(x, y, 336, 126, slot(f"BRIEF_{idx}")))
    return svg("S16", "Multi-card Brief", "\n".join([chrome("S16"), title_block(), '  <g id="brief-cards">' + "".join(cells) + "</g>"]))


def s17() -> str:
    body = "\n".join([
        chrome("S17"),
        title_block(),
        f'  <g id="system-diagram"><rect x="484" y="244" width="312" height="128" fill="{ACCENT}"/><text x="640" y="316" text-anchor="middle" fill="{WHITE}" font-family="{FONT}" font-size="28">{{{{CORE}}}}</text>'
        f'<rect x="160" y="270" width="190" height="76" fill="{GREY_1}" stroke="{GREY_2}"/><rect x="930" y="270" width="190" height="76" fill="{GREY_1}" stroke="{GREY_2}"/>'
        f'<line x1="350" y1="308" x2="484" y2="308" stroke="{INK}"/><line x1="796" y1="308" x2="930" y2="308" stroke="{INK}"/></g>'
        f'  <g id="system-notes"><rect x="64" y="514" width="352" height="88" fill="{GREY_1}"/><rect x="464" y="514" width="352" height="88" fill="{GREY_1}"/><rect x="864" y="514" width="352" height="88" fill="{GREY_1}"/></g>',
    ])
    return svg("S17", "System Diagram", body)


def s18() -> str:
    cols = "".join(card(x, 224, 320, 260, slot(f"REASON_{idx}")) for idx, x in enumerate((64, 480, 896), start=1))
    body = "\n".join([chrome("S18"), title_block(), f'  <g id="why-now">{cols}</g>', f'  <text id="bottom-number" x="64" y="650" fill="{ACCENT}" font-family="{FONT}" font-size="84" font-weight="200">{{{{BOTTOM_NUMBER}}}}</text>'])
    return svg("S18", "Why Now", body)


def s19() -> str:
    cards = "".join(card(x, 226, 264, 292, slot(f"CARD_{idx}")) for idx, x in enumerate((64, 352, 640, 928), start=1))
    return svg("S19", "Four Cards", "\n".join([chrome("S19"), f'  <rect id="accent-line" x="64" y="130" width="264" height="10" fill="{ACCENT}"/>', title_block(178, 44), '  <g id="four-cards">' + cards + "</g>"]))


def s20() -> str:
    rows = []
    for idx, y in enumerate((166, 278, 390, 502), start=1):
        rows.append(
            f'<line x1="64" y1="{y - 34}" x2="1216" y2="{y - 34}" stroke="{GREY_2}"/>'
            f'<text x="64" y="{y + 42}" fill="{ACCENT}" font-family="{FONT}" font-size="72" font-weight="200">{slot(f"LEDGER_{idx}_VALUE")}</text>'
            f'<text x="420" y="{y + 24}" fill="{INK}" font-family="{FONT}" font-size="28">{slot(f"LEDGER_{idx}_LABEL")}</text>'
        )
    return svg("S20", "Stacked KPI Ledger", "\n".join([chrome("S20"), '  <g id="ledger-rows">' + "".join(rows) + "</g>"]))


def s21() -> str:
    matrix = []
    for row in range(5):
        for col in range(4):
            matrix.append(f'<rect x="{918 + col * 56}" y="{274 + row * 40}" width="34" height="20" fill="{ACCENT if (row + col) % 3 == 0 else GREY_2}"/>')
    body = "\n".join([
        chrome("S21"),
        title_block(176, 60),
        f'  <g id="spec-kpis"><text x="64" y="316" fill="{ACCENT}" font-family="{FONT}" font-size="64" font-weight="200">{{{{KPI_1}}}}</text><text x="64" y="408" fill="{ACCENT}" font-family="{FONT}" font-size="64" font-weight="200">{{{{KPI_2}}}}</text><text x="64" y="500" fill="{ACCENT}" font-family="{FONT}" font-size="64" font-weight="200">{{{{KPI_3}}}}</text></g>',
        '  <g id="line-matrix">' + "".join(matrix) + "</g>",
    ])
    return svg("S21", "Tech Spec Sheet", body)


def s22() -> str:
    body = "\n".join([
        f'  <rect id="image-slot" x="64" y="56" width="1152" height="330" fill="{GREY_1}" stroke="{GREY_2}"/>',
        f'  <text id="image-label" x="640" y="228" text-anchor="middle" fill="{GREY_3}" font-family="{MONO}" font-size="18">{{{{IMAGE_SLOT_21_9}}}}</text>',
        f'  <rect id="title-card" x="96" y="88" width="430" height="116" fill="{WHITE}"/>',
        f'  <text id="image-title" x="120" y="150" fill="{INK}" font-family="{FONT}" font-size="36" font-weight="300">{{{{PAGE_TITLE}}}}</text>',
        f'  <g id="image-kpis"><rect x="64" y="480" width="352" height="120" fill="{WHITE}" stroke="{GREY_2}"/><rect x="464" y="480" width="352" height="120" fill="{ACCENT}"/><rect x="864" y="480" width="352" height="120" fill="{WHITE}" stroke="{GREY_2}"/></g>',
    ])
    return svg("S22", "Image Hero", body)


GENERATORS = {
    "S01": s01,
    "S02": s02,
    "S03": s03,
    "S04": s04,
    "S05": s05,
    "S06": s06,
    "S07": s07,
    "S08": s08,
    "S09": s09,
    "S10": s10,
    "S11": s11,
    "S12": s12,
    "S13": s13,
    "S14": s14,
    "S15": s15,
    "S16": s16,
    "S17": s17,
    "S18": s18,
    "S19": s19,
    "S20": s20,
    "S21": s21,
    "S22": s22,
}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for layout_id, generator in GENERATORS.items():
        slug, _ = LAYOUTS[layout_id]
        path = OUT_DIR / f"{layout_id}_{slug}.svg"
        path.write_text(generator(), encoding="utf-8")
    print(f"Generated {len(GENERATORS)} Guizang Swiss layout SVGs in {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
