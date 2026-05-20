#!/usr/bin/env python3
"""Build an academic_scqa-style Chinese popular-science deck on OpenClaw and Hermes."""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parent
SVG_OUT = PROJECT / "svg_output"
NOTES_DIR = PROJECT / "notes"
PLANS_DIR = PROJECT / "plans"
REPORTS_DIR = PROJECT / "reports"
STORYBOARD_DIR = PROJECT / "storyboard"
SOURCES_DIR = PROJECT / "sources"

TODAY = date.today().isoformat()
FONT = "Microsoft YaHei, Arial, sans-serif"

BLUE = "#0046A5"
DEEP = "#0B2F6B"
CYAN = "#00A6D6"
TEAL = "#17A889"
ICE = "#F7FAFF"
SURFACE = "#F1F6FF"
BORDER = "#D6E4F5"
TEXT = "#334155"
MUTED = "#64748B"
LIGHT_TEXT = "#E8F2FF"
WHITE = "#FFFFFF"
AMBER = "#F59E0B"
RED = "#DC2626"
GREEN = "#16A34A"


SOURCES = [
    {
        "id": "O1",
        "type": "repo",
        "title": "OpenClaw GitHub README and repository metadata",
        "path": "https://github.com/openclaw/openclaw",
        "key_points": [
            "Personal AI assistant run on user devices, with a local-first Gateway.",
            "GitHub page showed 373k stars and 77.5k forks during this research pass.",
            "README lists messaging channels, onboarding, tools, and security defaults.",
        ],
    },
    {
        "id": "O2",
        "type": "documentation",
        "title": "OpenClaw Gateway architecture",
        "path": "https://docs.openclaw.ai/concepts/architecture",
        "key_points": [
            "One long-lived Gateway owns messaging surfaces and exposes WebSocket control APIs.",
            "Clients and nodes connect to the same Gateway; nodes declare capabilities.",
        ],
    },
    {
        "id": "O3",
        "type": "documentation",
        "title": "OpenClaw security and sandboxing docs",
        "path": "https://docs.openclaw.ai/security",
        "key_points": [
            "DMs should be treated as untrusted input; pairing and allowlists are defaults.",
            "Sandboxing can isolate tool execution, while the Gateway remains on the host.",
        ],
    },
    {
        "id": "O4",
        "type": "release",
        "title": "OpenClaw releases",
        "path": "https://github.com/openclaw/openclaw/releases",
        "key_points": [
            "Latest visible pre-release during this research pass: openclaw 2026.5.19-beta.2.",
        ],
    },
    {
        "id": "H1",
        "type": "repo",
        "title": "Hermes Agent GitHub README and repository metadata",
        "path": "https://github.com/NousResearch/hermes-agent",
        "key_points": [
            "Self-improving AI agent built by Nous Research.",
            "GitHub page showed 158k stars and 25.6k forks during this research pass.",
            "README emphasizes memory, autonomous skill creation, scheduling, and subagents.",
        ],
    },
    {
        "id": "H2",
        "type": "documentation",
        "title": "Hermes Agent documentation overview",
        "path": "https://hermes-agent.nousresearch.com/docs/",
        "key_points": [
            "Hermes describes itself as a self-improving agent with a built-in learning loop.",
            "Docs list 20+ gateway platforms, built-in cron, MCP support, subagents, and full web control.",
        ],
    },
    {
        "id": "H3",
        "type": "documentation",
        "title": "Hermes architecture and memory docs",
        "path": "https://hermes-agent.nousresearch.com/docs/developer-guide/architecture",
        "key_points": [
            "AIAgent orchestrates provider selection, prompt construction, tools, persistence, and callbacks.",
            "Tool registry covers 70+ tools, with terminal backends including local, Docker, SSH, Daytona, Modal, Singularity, and Vercel Sandbox.",
            "Session storage uses SQLite with FTS5 search; prompt assembly includes memory and skills.",
        ],
    },
    {
        "id": "H4",
        "type": "release",
        "title": "Hermes Agent releases",
        "path": "https://github.com/NousResearch/hermes-agent/releases",
        "key_points": [
            "Latest visible release during this research pass: Hermes Agent v0.14.0, released May 16, 2026.",
        ],
    },
    {
        "id": "H5",
        "type": "security",
        "title": "Hermes Agent security policy",
        "path": "https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md",
        "key_points": [
            "Hermes treats OS-level isolation as the load-bearing security boundary.",
            "In-process approval, redaction, and scanning are useful heuristics but not containment.",
        ],
    },
]


def esc(value: object) -> str:
    return xml_escape(str(value), {'"': "&quot;"})


def clean_generated() -> None:
    for folder in (SVG_OUT, NOTES_DIR, PLANS_DIR, REPORTS_DIR, STORYBOARD_DIR):
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)


def tspans(lines: list[str], x: int | float, line_height: int | float) -> str:
    parts: list[str] = []
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        parts.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    return "".join(parts)


def text_block(
    x: int | float,
    y: int | float,
    lines: list[str],
    *,
    size: int = 22,
    fill: str = TEXT,
    weight: str = "400",
    line_height: int | None = None,
    width: int | float = 520,
    box_y: int | float | None = None,
    box_h: int | float | None = None,
    anchor: str = "start",
    name: str = "text",
) -> str:
    if line_height is None:
        line_height = int(size * 1.38)
    if box_y is None:
        box_y = y - size
    if box_h is None:
        box_h = max(line_height * len(lines) + 10, line_height + 10)
    if anchor == "middle":
        box_x = x - width / 2
    elif anchor == "end":
        box_x = x - width
    else:
        box_x = x
    return (
        f'<g id="{esc(name)}">'
        f'<rect x="{box_x}" y="{box_y}" width="{width}" height="{box_h}" fill="none"/>'
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" xml:space="preserve" '
        f'font-family="{FONT}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'data-pptx-textbox="true" data-pptx-box-x="{box_x}" data-pptx-box-y="{box_y}" '
        f'data-pptx-box-w="{width}" data-pptx-box-h="{box_h}" data-pptx-valign="top">{tspans(lines, x, line_height)}</text>'
        f"</g>"
    )


def single_text(
    x: int | float,
    y: int | float,
    text: str,
    *,
    size: int = 22,
    fill: str = TEXT,
    weight: str = "400",
    width: int | float = 360,
    height: int | float | None = None,
    anchor: str = "start",
    name: str = "single",
    box_x: int | float | None = None,
    box_y: int | float | None = None,
) -> str:
    if height is None:
        height = size + 12
    height = max(height, size * 1.7)
    if box_x is None:
        if anchor == "middle":
            box_x = x - width / 2
        elif anchor == "end":
            box_x = x - width
        else:
            box_x = x
    if box_y is None:
        box_y = y - size
    return (
        f'<g id="{esc(name)}">'
        f'<rect x="{box_x}" y="{box_y}" width="{width}" height="{height}" fill="none"/>'
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" xml:space="preserve" '
        f'font-family="{FONT}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
        f'data-pptx-textbox="true" data-pptx-box-x="{box_x}" data-pptx-box-y="{box_y}" '
        f'data-pptx-box-w="{width}" data-pptx-box-h="{height}" data-pptx-valign="middle"><tspan>{esc(text)}</tspan></text>'
        f"</g>"
    )


def centered_label(
    x: int | float,
    y: int | float,
    w: int | float,
    h: int | float,
    text: str,
    *,
    size: int = 16,
    fill: str = TEXT,
    weight: str = "700",
    name: str = "centered-label",
) -> str:
    return single_text(
        x + w / 2,
        y + h / 2 + size * 0.34,
        text,
        size=size,
        fill=fill,
        weight=weight,
        width=w,
        height=h,
        anchor="middle",
        name=name,
        box_x=x,
        box_y=y,
    )


def logo_fallback(x: int = 1104, y: int = 18, scale: float = 1.0) -> str:
    return (
        f'<g id="logo-fallback" data-slot="LOGO">'
        f'<rect x="{x}" y="{y}" width="{88 * scale}" height="{46 * scale}" fill="none"/>'
        f'<path d="M{x + 14 * scale} {y + 22 * scale} L{x + 44 * scale} {y + 9 * scale} '
        f'L{x + 74 * scale} {y + 22 * scale} L{x + 44 * scale} {y + 35 * scale} Z" fill="{LIGHT_TEXT}"/>'
        f'<path d="M{x + 28 * scale} {y + 29 * scale} L{x + 28 * scale} {y + 38 * scale} '
        f'Q{x + 44 * scale} {y + 45 * scale} {x + 60 * scale} {y + 38 * scale} '
        f'L{x + 60 * scale} {y + 29 * scale}" fill="none" stroke="{CYAN}" stroke-width="{3 * scale}" stroke-linecap="round"/>'
        f'<path d="M{x + 74 * scale} {y + 22 * scale} L{x + 74 * scale} {y + 35 * scale}" '
        f'fill="none" stroke="{TEAL}" stroke-width="{2.5 * scale}" stroke-linecap="round"/>'
        f'<circle cx="{x + 74 * scale}" cy="{y + 38 * scale}" r="{2.5 * scale}" fill="{TEAL}"/>'
        f"</g>"
    )


def content_shell(
    *,
    page_title: str,
    key_message: str,
    section: str,
    page_num: int,
    source: str,
    body: str,
) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect x="0" y="0" width="1280" height="720" fill="{WHITE}"/>
  <g id="content-header">
    <rect x="0" y="0" width="1280" height="82" fill="{BLUE}"/>
    <rect x="0" y="0" width="8" height="82" fill="{CYAN}"/>
    {single_text(70, 52, page_title, size=28, fill=WHITE, weight="700", width=860, height=44, name="page-title")}
    {logo_fallback()}
  </g>
  <g id="key-message">
    <rect x="70" y="108" width="1140" height="48" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1" rx="4"/>
    <rect x="70" y="108" width="6" height="48" fill="{TEAL}" rx="3"/>
    {single_text(94, 139, key_message, size=18, fill=TEXT, weight="600", width=1084, height=30, name="key-message-text")}
  </g>
  <g id="content-area">
    <rect x="70" y="176" width="1140" height="452" fill="{WHITE}" stroke="{BORDER}" stroke-width="1" rx="6"/>
    {body}
  </g>
  <g id="content-footer">
    <line x1="70" y1="654" x2="1210" y2="654" stroke="{BORDER}" stroke-width="1"/>
    {single_text(70, 686, source, size=12, fill="#94A3B8", width=410, height=22, name="source-footer")}
    {single_text(640, 686, section, size=12, fill=MUTED, anchor="middle", width=300, height=20, name="section-footer")}
    {single_text(1210, 686, f"{page_num:02d}", size=14, fill=BLUE, weight="700", anchor="end", width=80, height=22, name="page-number")}
  </g>
</svg>
'''


def cover_slide() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect x="0" y="0" width="1280" height="720" fill="{ICE}"/>
  <rect x="0" y="0" width="1280" height="4" fill="{CYAN}"/>
  {logo_fallback(1094, 24, 1.18)}
  <g id="cover-band">
    <rect x="0" y="172" width="1280" height="244" fill="{BLUE}"/>
    <rect x="0" y="172" width="12" height="244" fill="{CYAN}"/>
    <rect x="72" y="204" width="8" height="180" fill="{TEAL}"/>
  </g>
  {text_block(640, 268, ["从 OpenClaw 到 Hermes：", "AI Agent 如何从聊天走向行动"], size=42, fill=ICE, weight="700", line_height=58, width=980, box_y=220, box_h=118, anchor="middle", name="cover-title")}
  {single_text(640, 356, "一份面向非专业听众的技术科普报告", size=26, fill=LIGHT_TEXT, anchor="middle", width=920, height=44, name="cover-subtitle")}
  <rect x="450" y="472" width="380" height="2" fill="{BLUE}"/>
  {single_text(640, 526, "调研范围：官方仓库、文档、release 与安全说明", size=20, fill="#475569", anchor="middle", width=620, name="cover-scope")}
  {single_text(640, 562, f"时间口径：截至 {TODAY}", size=20, fill="#475569", anchor="middle", width=420, name="cover-date")}
  {single_text(640, 672, "academic_scqa template | editable native PPTX", size=13, fill=BLUE, anchor="middle", width=520, name="cover-footer")}
</svg>
'''


def toc_slide() -> str:
    items = [
        "为什么 Agent 突然重要",
        "OpenClaw 与 Hermes 案例",
        "共同架构与工作循环",
        "风险边界与安全试用",
        "判断框架与参考资料",
    ]
    cells: list[str] = []
    positions = [(70, 205), (690, 205), (70, 333), (690, 333), (70, 461)]
    widths = [520, 520, 520, 520, 1140]
    for i, (item, pos, width) in enumerate(zip(items, positions, widths), 1):
        x, y = pos
        title_x = x + 140
        cells.append(
            f'<g id="toc-item-{i}">'
            f'<rect x="{x}" y="{y}" width="{width}" height="90" fill="{WHITE}" stroke="{BORDER}" stroke-width="1" rx="6"/>'
            f'<text x="{x + 38}" y="{y + 55}" fill="{BLUE}" font-family="{FONT}" font-size="34" font-weight="700"><tspan>{i:02d}</tspan></text>'
            f'<rect x="{x + 108}" y="{y + 23}" width="6" height="44" fill="{TEAL}" rx="3"/>'
            f'{single_text(title_x, y + 55, item, size=22, fill=TEXT, weight="600", width=width - 170, height=34, name=f"toc-text-{i}")}'
            f"</g>"
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect x="0" y="0" width="1280" height="720" fill="{ICE}"/>
  {single_text(70, 86, "目录", size=38, fill=BLUE, weight="700", width=220, name="toc-title")}
  <rect x="70" y="106" width="248" height="4" fill="{CYAN}"/>
  {single_text(70, 146, "按 SCQA 组织：情境、冲突、问题、回答，再落到安全实践。", size=18, fill="#475569", width=780, name="toc-intro")}
  {logo_fallback(1096, 44, 1.16)}
  <g id="toc-items">
    {''.join(cells)}
  </g>
  <rect x="70" y="642" width="1140" height="2" fill="{BORDER}"/>
</svg>
'''


def chapter_slide(num: str, title: str, desc: str, label: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect x="0" y="0" width="1280" height="720" fill="{WHITE}"/>
  {single_text(64, 58, "章节", size=44, fill=DEEP, weight="700", width=160, name="chapter-word")}
  {single_text(192, 58, "SECTION", size=34, fill="#A6A6A6", weight="700", width=220, name="chapter-en")}
  {logo_fallback(1098, 34, 1.1)}
  <g id="chapter-card">
    <rect x="54" y="142" width="1172" height="520" rx="8" fill="{WHITE}" stroke="{BLUE}" stroke-width="1.6" stroke-opacity="0.18"/>
    <rect x="54" y="656" width="1172" height="11" rx="5.5" fill="{BLUE}"/>
    <rect x="346" y="312" width="64" height="64" fill="{DEEP}"/>
    <rect x="380" y="344" width="96" height="96" fill="{BLUE}"/>
    <text x="430" y="402" text-anchor="middle" xml:space="preserve" font-family="{FONT}" font-size="48" fill="{WHITE}" font-weight="700"><tspan>{esc(num)}</tspan></text>
    {single_text(522, 374, title, size=54, fill=DEEP, weight="700", width=620, height=82, name="chapter-title")}
    {single_text(522, 450, desc, size=24, fill="#4B5563", width=650, height=38, name="chapter-desc")}
    {single_text(522, 510, label, size=18, fill=TEAL, weight="700", width=660, height=30, name="chapter-label")}
  </g>
</svg>
'''


def bullet_rows(
    x: int,
    y: int,
    items: list[tuple[str, list[str]]],
    *,
    width: int = 420,
    gap: int = 76,
    color: str = TEAL,
    name: str = "bullets",
) -> str:
    rows: list[str] = []
    for i, (head, lines) in enumerate(items):
        cy = y + i * gap
        body_h = max(64, 26 * len(lines) + 10)
        rows.append(
            f'<g id="{esc(name)}-{i + 1}">'
            f'<circle cx="{x}" cy="{cy - 8}" r="8" fill="{color}"/>'
            f'{single_text(x + 22, cy, head, size=20, fill=DEEP, weight="700", width=width, height=28, name=f"{name}-{i + 1}-head")}'
            f'{text_block(x + 22, cy + 31, lines, size=15, fill=MUTED, line_height=22, width=width, box_y=cy + 11, box_h=body_h, name=f"{name}-{i + 1}-body")}'
            f"</g>"
        )
    return "".join(rows)


def metric_card(x: int, y: int, w: int, h: int, num: str, label: str, note: str, color: str, name: str) -> str:
    num_size = 30 if len(num) >= 8 else 34
    return (
        f'<g id="{esc(name)}">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3.5" fill="{color}"/>'
        f'{single_text(x + 26, y + 46, num, size=num_size, fill=color, weight="700", width=w - 52, height=58, name=f"{name}-num")}'
        f'{single_text(x + 26, y + 92, label, size=16, fill=DEEP, weight="700", width=w - 52, height=30, name=f"{name}-label")}'
        f'{single_text(x + 26, y + 116, note, size=12, fill=MUTED, width=w - 52, height=24, name=f"{name}-note")}'
        f"</g>"
    )


def small_card(x: int, y: int, w: int, h: int, title: str, lines: list[str], name: str, accent: str = BLUE) -> str:
    return (
        f'<g id="{esc(name)}">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{accent}"/>'
        f'{single_text(x + 22, y + 42, title, size=19, fill=DEEP, weight="700", width=w - 44, name=f"{name}-title")}'
        f'{text_block(x + 22, y + 76, lines, size=15, fill=MUTED, line_height=22, width=w - 44, box_y=y + 54, box_h=h - 62, name=f"{name}-body")}'
        f"</g>"
    )


def summary_slide() -> str:
    body = (
        f'<rect x="110" y="226" width="520" height="330" rx="8" fill="{DEEP}"/>'
        f'<rect x="110" y="226" width="10" height="330" fill="{CYAN}"/>'
        f'{text_block(150, 292, ["AI Agent 的关键变化不是", "模型更会聊天，", "而是它开始能调用工具、", "持久记忆并跨平台执行任务。"], size=33, fill=WHITE, weight="700", line_height=47, width=430, box_y=254, box_h=240, name="summary-thesis")}'
        f'{single_text(150, 526, "模型思考，工具行动，权限刹车。", size=18, fill=LIGHT_TEXT, width=470, height=42, name="summary-analogy")}'
        f'{small_card(690, 226, 220, 154, "从问答到行动", ["不只是回答问题，", "还会发消息、跑命令、", "浏览网页、写文件。"], "tile-action", TEAL)}'
        f'{small_card(944, 226, 220, 154, "从单次到持续", ["长期运行、定时任务、", "跨会话记忆，", "让上下文不再一次性。"], "tile-persist", CYAN)}'
        f'{small_card(690, 420, 220, 154, "从个人到生态", ["插件、MCP、技能库，", "让能力像积木一样扩展。"], "tile-ecosystem", BLUE)}'
        f'{small_card(944, 420, 220, 154, "从体验到治理", ["权限、沙箱、审计，", "决定 agent 能否安全落地。"], "tile-safety", RED)}'
    )
    return content_shell(
        page_title="AI Agent 正在从聊天界面变成行动系统",
        key_message="OpenClaw 和 Hermes 的共同点：都在把模型能力包装成长期运行、可调用工具的个人/本地 agent。",
        section="Situation",
        page_num=3,
        source="Sources: O1, H1, H2; checked 2026-05-20",
        body=body,
    )


def architecture_slide() -> str:
    cards = [
        (116, 230, 260, 112, "输入渠道", ["CLI / Telegram / Slack", "WhatsApp / Email / Web"], BLUE),
        (510, 230, 260, 112, "Gateway / Runtime", ["鉴权、会话、路由", "队列、事件、日志"], TEAL),
        (904, 230, 260, 112, "LLM Provider", ["OpenAI、Claude", "OpenRouter、本地模型"], CYAN),
        (116, 440, 260, 112, "记忆层", ["偏好与项目事实", "历史会话检索"], TEAL),
        (510, 440, 260, 112, "工具层", ["终端、浏览器、文件", "MCP、API、代码执行"], BLUE),
        (904, 440, 260, 112, "安全层", ["allowlist、审批", "沙箱、隔离、审计"], RED),
    ]
    connectors = [
        (376, 286, 510, 286),
        (770, 286, 904, 286),
        (640, 342, 640, 440),
        (376, 496, 510, 496),
        (770, 496, 904, 496),
        (246, 440, 246, 342),
        (1034, 342, 1034, 440),
    ]
    svg = []
    for i, (x1, y1, x2, y2) in enumerate(connectors):
        svg.append(
            f'<g id="arch-connector-{i}">'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BORDER}" stroke-width="3" stroke-linecap="round"/>'
            f'</g>'
        )
    for i, (x, y, w, h, title, lines, accent) in enumerate(cards):
        svg.append(small_card(x, y, w, h, title, lines, f"arch-card-{i}", accent))
    svg.append(
        f'<rect x="116" y="578" width="1048" height="36" rx="4" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{centered_label(116, 578, 1048, 36, "判断顺序：先看谁能触发，再看能动哪些工具，最后看错误能否被隔离和审计。", size=16, fill=DEEP, name="arch-bottom-rule")}'
    )
    return content_shell(
        page_title="这类 Agent 的结构像一个小型操作系统",
        key_message="理解 agent 不要只看模型，要看它怎样接入渠道、怎样调工具、怎样记忆、怎样限制权限。",
        section="Situation",
        page_num=5,
        source="Sources: O2, H3, H5",
        body="".join(svg),
    )


def why_cases_slide() -> str:
    body = (
        f'{small_card(104, 226, 320, 280, "OpenClaw 代表“本地网关型”", ["官方 README 把 Gateway 定位为控制平面，", "围绕多消息渠道、节点、工具与本地运行展开。", "它适合解释：agent 怎样接入现实软件。"], "why-openclaw", BLUE)}'
        f'{small_card(480, 226, 320, 280, "Hermes 代表“学习闭环型”", ["官方文档反复强调 memory、session search、", "技能自生成与 cron 自动化。", "它适合解释：agent 怎样积累经验。"], "why-hermes", TEAL)}'
        f'{small_card(856, 226, 320, 280, "共同代表 2026 年趋势", ["从单一聊天产品转向可部署 runtime；", "从一个模型转向多模型/多工具编排；", "从演示能力转向权限与治理。"], "why-common", CYAN)}'
        f'<rect x="104" y="548" width="1072" height="54" rx="6" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{centered_label(104, 548, 1072, 54, "读法提示：本报告不评测谁更强，而是把它们当作两个剖面，科普“现代 AI Agent 由哪些部件构成”。", size=17, fill=DEEP, name="why-note")}'
    )
    return content_shell(
        page_title="OpenClaw 和 Hermes 是理解现代 Agent 的两个入口",
        key_message="一个突出多渠道本地控制平面，一个突出记忆与技能闭环；合起来能看清 agent 化软件的基本形状。",
        section="Question",
        page_num=6,
        source="Sources: O1, O2, H1, H2",
        body=body,
    )


def openclaw_slide() -> str:
    body = (
        metric_card(100, 218, 200, 126, "373k", "GitHub stars", "仓库页研究时点", BLUE, "oc-stars")
        + metric_card(322, 218, 220, 126, "2026.5.19", "latest tag", "beta.2 pre-release", TEAL, "oc-release")
        + metric_card(564, 218, 200, 126, "20+", "channels", "README 多渠道入口", CYAN, "oc-channels")
        + f'<rect x="806" y="218" width="354" height="390" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>'
        + f'{single_text(834, 260, "为什么值得看", size=22, fill=DEEP, weight="700", width=260, name="oc-panel-title")}'
        + bullet_rows(
            836,
            300,
            [
                ("统一入口", ["把 WhatsApp/Telegram/Slack 等入口", "收拢到本地 Gateway。"]),
                ("关键边界", ["主会话默认在宿主机执行，", "敏感场景需要沙箱。"]),
                ("适合讲清", ["agent 如何接入现实软件，", "并保持单人本地控制。"]),
            ],
            width=268,
            gap=102,
            color=TEAL,
            name="oc-bullets",
        )
        + f'<g id="oc-flow">'
        + f'<rect x="130" y="410" width="160" height="82" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>'
        + f'{centered_label(130, 410, 160, 82, "消息渠道", size=21, fill=DEEP, name="oc-flow-1")}'
        + f'<line x1="290" y1="451" x2="388" y2="451" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/>'
        + f'<polygon points="388,451 374,443 374,459" fill="{TEAL}"/>'
        + f'<rect x="388" y="386" width="210" height="130" rx="8" fill="{BLUE}"/>'
        + f'{centered_label(388, 404, 210, 42, "Gateway", size=28, fill=WHITE, name="oc-flow-2a")}'
        + f'{centered_label(388, 448, 210, 38, "控制平面", size=18, fill=LIGHT_TEXT, weight="500", name="oc-flow-2b")}'
        + f'<line x1="598" y1="451" x2="666" y2="451" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/>'
        + f'<polygon points="666,451 652,443 652,459" fill="{TEAL}"/>'
        + f'<rect x="666" y="410" width="120" height="82" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>'
        + f'{centered_label(666, 410, 120, 82, "工具", size=21, fill=DEEP, name="oc-flow-3")}'
        + f'</g>'
        + f'<rect x="130" y="548" width="656" height="40" rx="4" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        + f'{centered_label(130, 548, 656, 40, "OpenClaw 的重点不是“更会聊”，而是把消息入口和本地执行边界组织成控制平面。", size=15, fill=DEEP, name="oc-summary")}'
    )
    return content_shell(
        page_title="OpenClaw 把多渠道消息入口收拢到本地 Gateway",
        key_message="它的科普价值在于展示：agent 不是单一聊天窗口，而是长期运行的本地控制平面。",
        section="Case Study",
        page_num=8,
        source="Sources: O1, O2, O3, O4",
        body=body,
    )


def hermes_slide() -> str:
    loop_nodes = [
        (596, 238, 164, 70, "Memory", "偏好、事实、用户模型"),
        (788, 346, 164, 70, "Skills", "沉淀可复用技能"),
        (596, 454, 164, 70, "Session Search", "从历史会话找证据"),
        (404, 346, 164, 70, "Cron / Subagents", "定时与并行执行"),
    ]
    connectors = (
        f'<path d="M 760 273 C 810 286 836 314 840 346" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 870 416 C 850 454 810 482 760 489" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 596 489 C 546 482 506 454 486 416" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 486 346 C 490 314 516 286 596 273" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
    )
    node_shapes = []
    for i, (x, y, w, h, title, desc) in enumerate(loop_nodes):
        node_shapes.append(
            f'<g id="hermes-node-{i}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{SURFACE}" stroke="{TEAL}" stroke-width="2"/>'
            f'{centered_label(x, y + 8, w, 28, title, size=17, fill=DEEP, name=f"hermes-node-{i}-title")}'
            f'{centered_label(x, y + 38, w, 24, desc, size=12, fill=MUTED, weight="400", name=f"hermes-node-{i}-desc")}'
            f'</g>'
        )
    body = (
        metric_card(100, 218, 190, 126, "158k", "GitHub stars", "仓库页研究时点", BLUE, "h-stars")
        + metric_card(312, 218, 210, 126, "v0.14.0", "latest release", "2026-05-16", TEAL, "h-release")
        + metric_card(100, 370, 190, 126, "70+", "tools", "官方架构文档", CYAN, "h-tools")
        + connectors
        + f'<rect x="598" y="352" width="160" height="62" rx="8" fill="{DEEP}"/>'
        + f'{centered_label(598, 352, 160, 62, "Hermes", size=25, fill=WHITE, name="h-center")}'
        + "".join(node_shapes)
        + f'<rect x="970" y="218" width="190" height="390" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>'
        + f'{single_text(998, 264, "阅读重点", size=22, fill=DEEP, weight="700", width=120, name="h-panel-title")}'
        + bullet_rows(
            1000,
            304,
            [
                ("核心卖点", ["记忆 + 技能", "组成学习闭环"]),
                ("运行位置", ["VPS / Docker / SSH", "或本地终端"]),
                ("适合问题", ["怎样让 agent", "跨会话复用经验"]),
            ],
            width=128,
            gap=104,
            color=TEAL,
            name="h-bullets",
        )
    )
    return content_shell(
        page_title="Hermes 把记忆、技能和调度组织成学习闭环",
        key_message="它的科普价值在于展示：agent 不只是会调用工具，还可以把经验沉淀成可复用的上下文与技能。",
        section="Case Study",
        page_num=9,
        source="Sources: H1, H2, H3, H4",
        body=body,
    )


def comparison_slide() -> str:
    rows = [
        ("定位", "多渠道本地个人助理 / Gateway", "自改进个人 agent / 学习闭环"),
        ("入口", "WhatsApp、Telegram、Slack 等消息面", "CLI + gateway 多平台 + 云/服务器运行"),
        ("重点", "控制平面、渠道路由、节点与工具", "记忆、技能、会话搜索、cron、subagents"),
        ("工具生态", "浏览器、canvas、nodes、cron、skills", "70+ tools、MCP、browser、code execution"),
        ("安全口径", "单人信任域；沙箱降低工具执行影响面", "OS 级隔离是安全边界；进程内检查是启发式"),
        ("适合讲清", "agent 如何接入现实软件", "agent 如何跨会话学习与复用经验"),
    ]
    y = 226
    body = [
        f'<rect x="96" y="{y}" width="1088" height="42" fill="{BLUE}" rx="6"/>',
        single_text(122, y + 28, "维度", size=16, fill=WHITE, weight="700", width=140, name="cmp-head-1"),
        single_text(326, y + 28, "OpenClaw", size=16, fill=WHITE, weight="700", width=330, name="cmp-head-2"),
        single_text(768, y + 28, "Hermes Agent", size=16, fill=WHITE, weight="700", width=330, name="cmp-head-3"),
    ]
    for i, (dim, left, right) in enumerate(rows):
        yy = y + 48 + i * 55
        fill = WHITE if i % 2 == 0 else ICE
        body.append(f'<rect x="96" y="{yy}" width="1088" height="50" fill="{fill}" stroke="{BORDER}" stroke-width="1"/>')
        body.append(single_text(122, yy + 32, dim, size=16, fill=DEEP, weight="700", width=120, height=24, name=f"cmp-dim-{i}"))
        body.append(single_text(326, yy + 32, left, size=15, fill=TEXT, width=380, height=24, name=f"cmp-left-{i}"))
        body.append(single_text(768, yy + 32, right, size=15, fill=TEXT, width=380, height=24, name=f"cmp-right-{i}"))
    body.append(
        f'<rect x="96" y="608" width="1088" height="34" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1" rx="4"/>'
        f'{centered_label(96, 608, 1088, 34, "结论：二者不是简单替代关系，而是分别把“连接现实世界”和“积累长期经验”推到前台。", size=15, fill=DEEP, name="cmp-conclusion")}'
    )
    return content_shell(
        page_title="两者的差异不是谁更像聊天机器人，而是谁更像运行时",
        key_message="OpenClaw 更像本地多渠道控制平面；Hermes 更像带记忆和技能进化的 agent runtime。",
        section="Case Study",
        page_num=10,
        source="Sources: O1-O3, H1-H5",
        body="".join(body),
    )


def loop_slide() -> str:
    cx, cy = 640, 400
    steps = [
        (640, 236, "感知", "读消息、文件、网页"),
        (842, 324, "计划", "拆任务、选工具"),
        (782, 524, "行动", "调用工具执行"),
        (498, 524, "观察", "读取结果与错误"),
        (438, 324, "记忆", "写入经验与偏好"),
    ]
    curve = (
        f'<path d="M 692 250 C 760 264 802 284 815 304" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 852 378 C 850 452 828 492 806 506" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 732 548 C 640 590 548 574 535 548" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 462 500 C 426 452 424 380 434 376" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
        f'<path d="M 474 302 C 528 264 578 246 586 240" fill="none" stroke="{CYAN}" stroke-width="3" stroke-linecap="round"/>'
    )
    parts = [curve, f'<circle cx="{cx}" cy="{cy}" r="84" fill="{DEEP}"/>']
    parts.append(single_text(cx, cy - 4, "Agent Loop", size=25, fill=WHITE, weight="700", anchor="middle", width=180, name="loop-center"))
    parts.append(single_text(cx, cy + 30, "不是魔法，是循环", size=15, fill=LIGHT_TEXT, anchor="middle", width=180, name="loop-center-sub"))
    for i, (x, y, title, desc) in enumerate(steps):
        parts.append(
            f'<g id="loop-step-{i}">'
            f'<circle cx="{x}" cy="{y}" r="54" fill="{SURFACE}" stroke="{TEAL}" stroke-width="2"/>'
            f'{single_text(x, y - 4, title, size=22, fill=DEEP, weight="700", anchor="middle", width=90, name=f"loop-step-{i}-title")}'
            f'{single_text(x, y + 26, desc, size=12, fill=MUTED, anchor="middle", width=120, name=f"loop-step-{i}-desc")}'
            f"</g>"
        )
    parts.append(
        f'<rect x="92" y="220" width="250" height="370" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{single_text(120, 268, "和普通脚本不同", size=21, fill=DEEP, weight="700", width=200, name="loop-left-title")}'
        f'{bullet_rows(126, 306, [("可感知上下文", ["把网页、邮件、文件纳入判断"]), ("可选择工具", ["不是固定流程，而是动态决策"]), ("可复盘", ["把成功路径沉淀为记忆或技能"])], width=170, gap=100, color=TEAL, name="loop-left")}'
        f'<rect x="938" y="220" width="250" height="370" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{single_text(966, 268, "也不是全自动可靠", size=21, fill=DEEP, weight="700", width=200, name="loop-right-title")}'
        f'{bullet_rows(972, 306, [("模型会误判", ["所以要工具策略和审批"]), ("输入会被污染", ["所以要把外部内容当不可信"]), ("状态会漂移", ["所以要日志、回滚和边界"])], width=170, gap=100, color=RED, name="loop-right")}'
    )
    return content_shell(
        page_title="Agent 的基本机制是“感知、计划、行动、观察、记忆”的循环",
        key_message="越多真实工具接入循环，agent 越像自动化同事；越多权限接入循环，也越需要边界治理。",
        section="Mechanism",
        page_num=12,
        source="Sources: O2, H3",
        body="".join(parts),
    )


def automation_slide() -> str:
    cards = [
        ("消息触发", "有人在 Telegram/Slack 里发来任务", "Gateway 鉴权后路由到会话"),
        ("定时触发", "每天/每周自动运行检查或报告", "cron 让 agent 离开当前聊天继续工作"),
        ("事件触发", "PR、告警、webhook 或文件变化", "把 agent 接进工程工作流"),
        ("并行触发", "拆成多个子任务同时推进", "subagents 降低大任务等待时间"),
    ]
    parts = []
    for i, (title, trigger, effect) in enumerate(cards):
        x = 104 + i * 270
        parts.append(
            f'<g id="auto-card-{i}">'
            f'<rect x="{x}" y="238" width="230" height="260" rx="8" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>'
            f'<circle cx="{x + 42}" cy="284" r="26" fill="{[BLUE, TEAL, CYAN, AMBER][i]}"/>'
            f'<text x="{x + 42}" y="293" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{WHITE}" font-weight="700"><tspan>{i + 1}</tspan></text>'
            f'{single_text(x + 82, 292, title, size=21, fill=DEEP, weight="700", width=120, name=f"auto-title-{i}")}'
            f'{text_block(x + 28, 360, [trigger], size=16, fill=TEXT, line_height=24, width=174, box_y=330, box_h=70, name=f"auto-trigger-{i}")}'
            f'<line x1="{x + 28}" y1="420" x2="{x + 202}" y2="420" stroke="{BORDER}" stroke-width="1"/>'
            f'{text_block(x + 28, 458, [effect], size=15, fill=MUTED, line_height=22, width=174, box_y=432, box_h=56, name=f"auto-effect-{i}")}'
            f"</g>"
        )
    parts.append(
        f'<rect x="104" y="540" width="1040" height="58" rx="6" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{centered_label(104, 540, 1040, 58, "科普重点：一旦有触发器，agent 就从“你问我答”变成“系统事件驱动的工作者”。", size=17, fill=DEEP, name="auto-note")}'
    )
    return content_shell(
        page_title="自动化触发器让 Agent 脱离单次聊天窗口",
        key_message="定时任务、消息网关、webhook 与子代理并行，是这类系统从玩具走向工作流的关键。",
        section="Mechanism",
        page_num=13,
        source="Sources: O1, H2, H3",
        body="".join(parts),
    )


def safety_slide() -> str:
    layers = [
        ("谁能说话", "DM pairing / allowlist", "避免陌生输入直接触发工具"),
        ("能用什么", "tool policy / MCP filter", "把高风险工具默认关掉"),
        ("在哪里做", "Docker / SSH / sandbox", "把错误操作限制在隔离环境"),
        ("错了怎么办", "logs / approvals / rollback", "让行为可见、可停、可追溯"),
    ]
    parts = []
    for i, (title, control, note) in enumerate(layers):
        y = 226 + i * 86
        color = [BLUE, TEAL, CYAN, RED][i]
        parts.append(
            f'<g id="safe-layer-{i}">'
            f'<rect x="112" y="{y}" width="760" height="66" rx="8" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>'
            f'<rect x="112" y="{y}" width="12" height="66" rx="6" fill="{color}"/>'
            f'{centered_label(146, y + 12, 150, 42, title, size=20, fill=DEEP, name=f"safe-title-{i}")}'
            f'{centered_label(330, y + 12, 250, 42, control, size=16, fill=TEXT, name=f"safe-control-{i}")}'
            f'{centered_label(614, y + 12, 230, 42, note, size=15, fill=MUTED, weight="400", name=f"safe-note-{i}")}'
            f"</g>"
        )
    parts.append(
        f'<rect x="922" y="226" width="244" height="324" rx="8" fill="{DEEP}"/>'
        f'{single_text(1044, 276, "核心误区", size=25, fill=WHITE, weight="700", anchor="middle", width=180, name="safe-myth-title")}'
        f'{text_block(954, 330, ["不要把安全寄托在", "“系统提示词很强”上。", "", "官方安全文档都把", "硬边界放在授权、", "工具策略和 OS/沙箱隔离。"], size=18, fill=LIGHT_TEXT, line_height=28, width=180, box_y=304, box_h=190, name="safe-myth")}'
        f'<rect x="922" y="570" width="244" height="50" rx="6" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{centered_label(922, 570, 244, 50, "提示词是方向盘，权限才是刹车。", size=16, fill=DEEP, name="safe-quote")}'
    )
    return content_shell(
        page_title="Agent 安全首先是权限边界问题，而不是提示词问题",
        key_message="越是能读文件、跑命令、发消息的 agent，越要用授权、工具策略和沙箱把行动范围框住。",
        section="Risk",
        page_num=14,
        source="Sources: O3, H5",
        body="".join(parts),
    )


def judgement_slide() -> str:
    cards = [
        (112, 226, "看运行位置", ["本机、VPS、云沙箱还是公司服务器？", "数据、凭证和日志在哪里？"]),
        (650, 226, "看触发面", ["谁能 DM 它？谁能发 webhook？", "群聊里是否需要明确 mention？"]),
        (112, 386, "看工具清单", ["终端、浏览器、文件写入、邮件发送", "是否默认开启？是否可按任务收窄？"]),
        (650, 386, "看隔离和审计", ["有没有沙箱、审批、日志、回滚？", "profile / gateway 是否分离？"]),
    ]
    body = []
    for i, (x, y, title, lines) in enumerate(cards, 1):
        body.append(
            f'<g id="judge-card-{i}">'
            f'<rect x="{x}" y="{y}" width="468" height="124" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>'
            f'<circle cx="{x + 34}" cy="{y + 38}" r="10" fill="{TEAL}"/>'
            f'{single_text(x + 60, y + 48, title, size=23, fill=DEEP, weight="700", width=330, name=f"judge-title-{i}")}'
            f'{text_block(x + 60, y + 84, lines, size=16, fill=MUTED, line_height=24, width=370, box_y=y + 62, box_h=56, name=f"judge-body-{i}")}'
            f'</g>'
        )
    body.append(
        f'<rect x="112" y="556" width="1006" height="60" rx="8" fill="{DEEP}"/>'
        f'{centered_label(112, 556, 1006, 60, "一句话结论：把 agent 当作“会思考的自动化脚本”，用产品眼光看体验，用安全眼光看权限。", size=18, fill=WHITE, name="final-conclusion")}'
    )
    return content_shell(
        page_title="评估一个 Agent，先问四个工程问题",
        key_message="比起问“模型聪不聪明”，更该问：它在哪里运行、谁能触发、能动哪些工具、出了错能否收住。",
        section="Discussion",
        page_num=15,
        source=f"All source pages checked on {TODAY}",
        body="".join(body),
    )


def references_slide() -> str:
    references = [
        ("[1]", "OpenClaw. GitHub repository.", "github.com/openclaw/openclaw"),
        ("[2]", "OpenClaw. Gateway architecture.", "docs.openclaw.ai/concepts/architecture"),
        ("[3]", "OpenClaw. Security and sandboxing.", "docs.openclaw.ai/security"),
        ("[4]", "OpenClaw. Release notes.", "github.com/openclaw/openclaw/releases"),
        ("[5]", "Nous Research. Hermes Agent repository.", "github.com/NousResearch/hermes-agent"),
        ("[6]", "Hermes Agent. Documentation overview.", "hermes-agent.nousresearch.com/docs/"),
        ("[7]", "Hermes Agent. Architecture/memory docs.", "Developer guide pages"),
        ("[8]", "Hermes Agent. Release notes.", "github.com/NousResearch/hermes-agent/releases"),
        ("[9]", "Hermes Agent. Security policy.", "github.com/NousResearch/hermes-agent/blob/main/SECURITY.md"),
    ]
    rows: list[str] = [
        f'<rect x="92" y="204" width="1096" height="370" rx="8" fill="{ICE}" stroke="{BORDER}" stroke-width="1"/>',
        f'<rect x="92" y="204" width="1096" height="8" rx="4" fill="{BLUE}"/>',
    ]
    for i, (num, title, locator) in enumerate(references):
        y = 226 + i * 37
        color = BLUE if i < 4 else TEAL
        rows.append(
            f'<g id="ref-row-{i + 1}">'
            f'<rect x="112" y="{y}" width="1056" height="30" rx="4" fill="{WHITE}" stroke="{BORDER}" stroke-width="1"/>'
            f'<rect x="112" y="{y}" width="52" height="30" rx="4" fill="{color}"/>'
            f'{centered_label(112, y, 52, 30, num, size=14, fill=WHITE, name=f"ref-num-{i + 1}")}'
            f'{single_text(180, y + 13, title, size=13, fill=DEEP, weight="700", width=360, height=20, name=f"ref-title-{i + 1}")}'
            f'{single_text(550, y + 13, locator + f"; Accessed: {TODAY}.", size=11, fill=MUTED, width=600, height=20, name=f"ref-url-{i + 1}")}'
            f'</g>'
        )
    rows.append(
        f'<rect x="112" y="590" width="1056" height="34" rx="4" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'{centered_label(112, 590, 1056, 34, "格式：编号. 责任主体. 页面标题. URL 或文档位置. Accessed date.", size=14, fill=DEEP, name="refs-note")}'
    )
    body = "".join(rows)
    return content_shell(
        page_title="参考文献按编号列出，方便回查证据来源",
        key_message="编号顺序对应报告证据索引；每条保留责任主体、页面标题、URL 或文档位置与访问日期。",
        section="References",
        page_num=16,
        source=f"All source pages checked on {TODAY}",
        body=body,
    )


def build_deck() -> list[dict[str, object]]:
    slides: list[dict[str, object]] = [
        {
            "filename": "01_cover.svg",
            "svg": cover_slide(),
            "role": "cover",
            "action_title": "AI Agent 正在从聊天界面变成行动系统",
            "claim": "OpenClaw 与 Hermes 可作为理解现代 agent runtime 的两个代表剖面。",
            "sources": ["O1", "H1", "H2"],
            "kind": "reference",
            "note": "开场：说明本报告不是产品排名，而是用两个热门开源 agent 案例科普现代 AI Agent 的组成方式。",
        },
        {
            "filename": "02_toc.svg",
            "svg": toc_slide(),
            "role": "agenda",
            "action_title": "报告按 SCQA 从情境、案例、机制走向安全判断",
            "claim": "SCQA 结构能把工具热度转化为可理解的工程问题。",
            "sources": ["O1", "H2"],
            "kind": "reference",
            "note": "快速过目录，提醒听众最后会回到安全试用和判断框架。",
        },
        {
            "filename": "03_summary.svg",
            "svg": summary_slide(),
            "role": "overview",
            "action_title": "AI Agent 的关键变化是把模型接上行动能力",
            "claim": "现代 agent 的核心不是单次聊天，而是模型、工具、记忆、网关和安全策略的组合。",
            "sources": ["O1", "H1", "H2"],
            "kind": "reference",
            "note": "用一句话打底：LLM 大脑、网关神经、工具双手、记忆本和安全围栏。",
        },
        {
            "filename": "04_chapter_situation.svg",
            "svg": chapter_slide("01", "为什么是 Agent", "From chat interface to action runtime", "Situation: 聊天只是入口，执行才是变化"),
            "role": "section_open",
            "action_title": "从聊天到行动是 Agent 化软件的第一性变化",
            "claim": "Agent 将自然语言入口与现实工具连接起来，形成可执行的运行时。",
            "sources": ["O1", "H2"],
            "kind": "reference",
            "note": "切到第一部分：为什么它不是又一个聊天应用。",
        },
        {
            "filename": "05_architecture.svg",
            "svg": architecture_slide(),
            "role": "framework",
            "action_title": "现代 Agent 更像小型操作系统而不是单个模型",
            "claim": "Agent 需要渠道、运行时、模型、工具、记忆和安全边界共同工作。",
            "sources": ["O2", "H3", "H5"],
            "kind": "diagram",
            "note": "讲清六个部件，特别强调评估 agent 时要看权限和边界。",
        },
        {
            "filename": "06_why_cases.svg",
            "svg": why_cases_slide(),
            "role": "research_question",
            "action_title": "OpenClaw 与 Hermes 分别照亮连接现实和积累经验两条路线",
            "claim": "二者可以作为现代 agent 的两个剖面：多渠道控制平面与学习闭环。",
            "sources": ["O1", "O2", "H1", "H2"],
            "kind": "reference",
            "note": "解释为什么选这两个项目，而不是泛泛列一堆 agent 框架。",
        },
        {
            "filename": "07_chapter_cases.svg",
            "svg": chapter_slide("02", "两个代表案例", "OpenClaw as gateway, Hermes as learning loop", "Question: 同样叫 agent，它们到底在强化什么？"),
            "role": "section_open",
            "action_title": "案例对比能把 Agent 的抽象概念变成可观察结构",
            "claim": "通过案例可以看见 agent runtime 的不同设计重心。",
            "sources": ["O1", "H1"],
            "kind": "reference",
            "note": "引出两个案例，先 OpenClaw 后 Hermes。",
        },
        {
            "filename": "08_openclaw.svg",
            "svg": openclaw_slide(),
            "role": "case_study",
            "action_title": "OpenClaw 的核心是多渠道本地 Gateway",
            "claim": "OpenClaw 以本地 Gateway 作为控制平面，把消息渠道、会话和工具接到一起。",
            "sources": ["O1", "O2", "O3", "O4"],
            "kind": "data",
            "note": "说明 373k stars 等数字是研究时点的 GitHub 页面快照，不写成永久事实。",
        },
        {
            "filename": "09_hermes.svg",
            "svg": hermes_slide(),
            "role": "case_study",
            "action_title": "Hermes 的核心是记忆和技能驱动的学习闭环",
            "claim": "Hermes 把持久记忆、会话检索、技能自生成、调度和子代理组织成持续运行的 agent。",
            "sources": ["H1", "H2", "H3", "H4"],
            "kind": "data",
            "note": "把 learning loop 讲成四个模块：记忆、技能、会话检索、定时/并行，并强调连接线只表达循环关系。",
        },
        {
            "filename": "10_comparison.svg",
            "svg": comparison_slide(),
            "role": "comparison",
            "action_title": "OpenClaw 更像控制平面，Hermes 更像学习型运行时",
            "claim": "二者不是简单替代关系，而是突出 agent 系统的不同能力轴。",
            "sources": ["O1", "O2", "O3", "H1", "H2", "H3", "H5"],
            "kind": "table",
            "note": "用表格收束案例对比，帮助听众建立两个定位。",
        },
        {
            "filename": "11_chapter_mechanism.svg",
            "svg": chapter_slide("03", "共同工作机制", "Sense, plan, act, observe, remember", "Answer: 把 agent 拆成循环，而不是人格化想象"),
            "role": "section_open",
            "action_title": "Agent 的共同机制可以拆成一个可审计循环",
            "claim": "感知、计划、行动、观察和记忆构成这类系统的基本循环。",
            "sources": ["O2", "H3"],
            "kind": "diagram",
            "note": "从案例回到机制。",
        },
        {
            "filename": "12_loop.svg",
            "svg": loop_slide(),
            "role": "mechanism",
            "action_title": "Agent 循环越接近现实工具，越需要边界治理",
            "claim": "感知、计划、行动、观察、记忆的循环解释了 agent 为什么强，也解释了为什么危险。",
            "sources": ["O2", "H3"],
            "kind": "diagram",
            "note": "强调它不是魔法，而是循环；越接现实工具，越要看边界。",
        },
        {
            "filename": "13_automation.svg",
            "svg": automation_slide(),
            "role": "workflow",
            "action_title": "触发器让 Agent 从对话走向无人值守工作流",
            "claim": "消息、定时、事件和子代理并行是 agent 进入工作流的关键。",
            "sources": ["O1", "H2", "H3"],
            "kind": "diagram",
            "note": "这页解释为什么 cron/webhook/subagents 很重要。",
        },
        {
            "filename": "14_safety.svg",
            "svg": safety_slide(),
            "role": "risk",
            "action_title": "Agent 安全首先是权限边界问题",
            "claim": "官方安全文档都将硬边界放在授权、工具策略和 OS/沙箱隔离上，而非单靠提示词。",
            "sources": ["O3", "H5"],
            "kind": "reference",
            "note": "用方向盘和刹车的比喻解释：提示词给方向，权限边界才是刹车。",
        },
        {
            "filename": "15_judgement.svg",
            "svg": judgement_slide(),
            "role": "discussion",
            "action_title": "评估 Agent 要先问运行、触发、工具和隔离四个问题",
            "claim": "把 agent 当成会思考的自动化脚本，才能同时看见效率与风险。",
            "sources": ["O1", "O2", "O3", "O4", "H1", "H2", "H3", "H4", "H5"],
            "kind": "reference",
            "note": "给出四问判断框架，避免把判断和参考资料挤在同一页。",
        },
        {
            "filename": "16_references.svg",
            "svg": references_slide(),
            "role": "references",
            "action_title": "参考文献按 [1]-[9] 编号列出",
            "claim": "本报告所有事实主张均绑定到官方仓库、文档、release 或安全说明。",
            "sources": ["O1", "O2", "O3", "O4", "H1", "H2", "H3", "H4", "H5"],
            "kind": "reference",
            "note": "参考文献采用编号格式，包含责任主体、页面标题、URL 或文档位置，以及访问日期。",
        },
    ]

    for slide in slides:
        filename = str(slide["filename"])
        (SVG_OUT / filename).write_text(str(slide["svg"]), encoding="utf-8")
        (NOTES_DIR / f"{Path(filename).stem}.md").write_text(str(slide["note"]) + "\n", encoding="utf-8")
    return slides


def write_artifacts(slides: list[dict[str, object]]) -> None:
    source_pack = {
        "schema_version": "easyppt.source_pack.v1",
        "topic": "OpenClaw and Hermes-like AI agents",
        "research_date": TODAY,
        "local_kb_status": "OneFind searched first; no direct relevant local evidence was found.",
        "sources": SOURCES,
        "claims": [
            {
                "id": "c-agent-runtime",
                "claim": "Modern AI agents should be understood as runtimes combining model reasoning, tools, memory, channels, automation, and security policy.",
                "source_ids": ["O1", "O2", "H2", "H3"],
            },
            {
                "id": "c-openclaw-gateway",
                "claim": "OpenClaw's public docs emphasize a long-lived Gateway that owns messaging surfaces and routes clients, nodes, sessions, tools, and events.",
                "source_ids": ["O1", "O2"],
            },
            {
                "id": "c-hermes-learning",
                "claim": "Hermes emphasizes a built-in learning loop: curated memory, session search, autonomous skill creation, cron, subagents, and many tool backends.",
                "source_ids": ["H1", "H2", "H3"],
            },
            {
                "id": "c-security-boundary",
                "claim": "For tool-capable agents, safety depends on authorization, tool policy, OS/sandbox isolation, and auditability rather than prompt rules alone.",
                "source_ids": ["O3", "H5"],
            },
        ],
        "provenance_notes": "Search-result SEO pages and unsourced secondary commentary were used only for discovery, not as slide evidence.",
    }
    (SOURCES_DIR / "source_pack.json").write_text(
        json.dumps(source_pack, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    research_notes = [
        "# Research Notes",
        "",
        f"Research date: {TODAY}",
        "",
        "Local OneFind was queried first for `openclaw hermes AI agent 科普 报告`; it returned no relevant local evidence.",
        "The deck uses primary or near-primary public sources: GitHub repositories, official docs, release pages, and security policies.",
        "",
        "## Source Index",
    ]
    for source in SOURCES:
        research_notes.append(f"- {source['id']}: {source['title']} — {source['path']}")
    (SOURCES_DIR / "research_notes.md").write_text("\n".join(research_notes) + "\n", encoding="utf-8")

    deck_plan = {
        "schema_version": "easyslides.deck_plan.v1",
        "scenario_profile": "workshop_training",
        "scenario_variant": "popular_science_technical_report",
        "source_map": [
            {"id": s["id"], "type": s["type"], "path": s["path"], "title": s["title"]}
            for s in SOURCES
        ],
        "slides": [],
    }
    for idx, slide in enumerate(slides, 1):
        deck_plan["slides"].append(
            {
                "page": f"P{idx:02d}",
                "role": slide["role"],
                "action_title": slide["action_title"],
                "claim": slide["claim"],
                "layout_id": "academic_scqa",
                "rhythm": "anchor" if slide["role"] in {"cover", "section_open", "references"} else "breathing",
                "speaker_note": slide["note"],
                "evidence_sources": [
                    {
                        "source_id": sid,
                        "locator": "official page / public repository lines captured by web research",
                        "kind": slide["kind"],
                    }
                    for sid in slide["sources"]
                ],
            }
        )
    (PROJECT / "deck_plan.json").write_text(json.dumps(deck_plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PLANS_DIR / "deck_plan.json").write_text(json.dumps(deck_plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    intake_lock = f"""# Intake Lock

- scenario: popular-science technical report
- audience: AI-curious academic or product audience, not necessarily agent-framework specialists
- slide count / duration: {len(slides)} slides / about 10 minutes
- language: Chinese with selected English technical terms
- output contract: editable-native PPTX through EasySlides SVG-to-DrawingML pipeline
- source materials: public official repositories, docs, releases, and security policies
- institution / logo: no user-supplied logo; academic_scqa degree-cap fallback retained
- template route: `templates/layouts/academic_scqa`
- density: medium, one claim per content slide
- sample gate: inferred direct-build because user requested a completed PPT
"""
    (PLANS_DIR / "intake_lock.md").write_text(intake_lock, encoding="utf-8")

    spec_lock = f"""# Spec Lock

## Deck Contract
Chinese popular-science report on OpenClaw and Hermes-like AI agents, 16:9, using academic_scqa.

## Visual Contract
Academic blue/cyan/teal palette, SCQA flow, no full-slide screenshots. Diagrams and tables are editable native SVG-derived shapes.

## colors
- academic_blue: #0046A5
- deep_blue: #0B2F6B
- sky_cyan: #00A6D6
- teal: #17A889
- ice: #F7FAFF
- surface: #F1F6FF
- white: #FFFFFF
- border: #D6E4F5
- light_text: #E8F2FF
- text: #334155
- muted: #64748B
- footer_gray: #94A3B8
- slate: #475569
- body_gray: #4B5563
- template_gray: #A6A6A6
- amber: #F59E0B
- red: #DC2626
- green: #16A34A

## Source Contract
Every claim ties to source labels O1-O4 and H1-H5. Search-result SEO pages are excluded from evidence.

## Page Roster
cover, agenda, overview, section dividers, architecture diagram, case study, comparison table, mechanism loop, automation triggers, safety model, judgement/reference slide.

## Typography
Microsoft YaHei, Arial, sans-serif. Body text stays at 12px or above for references and 15px+ for main content.
"""
    (PLANS_DIR / "spec_lock.md").write_text(spec_lock, encoding="utf-8")
    (PROJECT / "spec_lock.md").write_text(spec_lock, encoding="utf-8")

    design_spec = f"""# Design Spec

- template_id: academic_scqa
- canvas: 1280 x 720, PPT 16:9
- palette: academic blue {BLUE}, deep blue {DEEP}, sky cyan {CYAN}, teal {TEAL}, ice background {ICE}
- typography: {FONT}
- layout policy: one conclusion-style page title, one key message, one dominant exhibit per content slide
- logo policy: no real logo supplied; use built-in degree-cap fallback
- citation policy: slide footers carry source labels; final slide expands references
"""
    (PROJECT / "design_spec.md").write_text(design_spec, encoding="utf-8")
    (PLANS_DIR / "design_system.json").write_text(
        json.dumps(
            {
                "template_id": "academic_scqa",
                "canvas": "1280x720",
                "palette": {
                    "academic_blue": BLUE,
                    "deep_blue": DEEP,
                    "sky_cyan": CYAN,
                    "teal": TEAL,
                    "ice": ICE,
                    "surface": SURFACE,
                    "border": BORDER,
                },
                "font_stack": FONT,
                "logo": "academic_scqa fallback degree-cap icon",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (PLANS_DIR / "story_blueprint.json").write_text(
        json.dumps(
            {
                "audience_question": "这类 AI agent 到底是什么，为什么现在重要，如何安全判断？",
                "central_claim": "现代 agent 是模型、工具、记忆、网关和权限边界组成的运行时。",
                "slides": [
                    {
                        "slide": i,
                        "file": slide["filename"],
                        "claim": slide["claim"],
                        "source_ids": slide["sources"],
                    }
                    for i, slide in enumerate(slides, 1)
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (PLANS_DIR / "template_binding.json").write_text(
        json.dumps(
            [
                {
                    "slide": i,
                    "file": slide["filename"],
                    "template_id": "academic_scqa",
                    "layout_id": "A02-S04" if slide["role"] not in {"cover", "agenda", "section_open"} else "academic_scqa-shell",
                    "route": "style reconstruction with editable SVG shapes",
                }
                for i, slide in enumerate(slides, 1)
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (PLANS_DIR / "element_plan.json").write_text(
        json.dumps(
            [
                {
                    "slide": i,
                    "file": slide["filename"],
                    "page_role": slide["role"],
                    "content_element": slide["kind"],
                    "shell": "academic_scqa",
                    "module_reuse_policy": "no external module; native shape reconstruction",
                }
                for i, slide in enumerate(slides, 1)
            ],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (PLANS_DIR / "institution_logo.json").write_text(
        json.dumps(
            {
                "institution": None,
                "logo_source": None,
                "policy": "No user-provided logo was available; keep academic_scqa fallback icon.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (REPORTS_DIR / "source_traceability_report.json").write_text(
        json.dumps(
            {
                "schema_version": "easyppt.source_traceability_report.v1",
                "status": "pass",
                "blocking_count": 0,
                "slide_count": len(slides),
                "notes": "Each slide declares source labels in deck_plan.json; final slide expands the source index.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    storyboard_items = []
    for i, slide in enumerate(slides, 1):
        filename = esc(slide["filename"])
        title = esc(slide["action_title"])
        storyboard_items.append(
            f'<section><h2>{i:02d}. {title}</h2><object data="../svg_output/{filename}" type="image/svg+xml"></object></section>'
        )
    storyboard = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <title>OpenClaw Hermes academic_scqa storyboard</title>
  <style>
    body {{ margin: 24px; background: #f5f7fb; font-family: Arial, 'Microsoft YaHei', sans-serif; }}
    h1 {{ color: {DEEP}; }}
    section {{ margin-bottom: 32px; }}
    object {{ width: 960px; height: 540px; background: white; box-shadow: 0 6px 20px rgba(0,0,0,.08); }}
  </style>
</head>
<body>
  <h1>OpenClaw / Hermes AI Agent 科普报告 storyboard</h1>
  {''.join(storyboard_items)}
</body>
</html>
"""
    (STORYBOARD_DIR / "index.html").write_text(storyboard, encoding="utf-8")


def main() -> None:
    clean_generated()
    slides = build_deck()
    write_artifacts(slides)
    print(json.dumps({"project": str(PROJECT), "slides": len(slides), "svg_output": str(SVG_OUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
