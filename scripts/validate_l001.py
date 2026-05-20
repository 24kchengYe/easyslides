#!/usr/bin/env python3
"""Validate the lightweight L001 notebook-defense style pack."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


STYLE_SYSTEM = "l001_notebook_defense"
PRIMARY = "#8B0012"
VIEWBOX = "0 0 1280 720"
REQUIRED_SVGS = (
    "01_cover.svg",
    "02_toc.svg",
    "03_section.svg",
    "04_content.svg",
    "05_closing.svg",
)
REQUIRED_PAGE_TYPES = {"cover", "toc", "section", "content", "closing"}
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6,8}\b")


def issue(code: str, message: str, path: Path | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if path is not None:
        item["path"] = str(path)
    return item


def read_json(path: Path, issues: list[dict[str, str]]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(issue("L001-MISSING-FILE", f"{path.name} is required", path))
    except json.JSONDecodeError as exc:
        issues.append(issue("L001-JSON", f"{path.name} is not valid JSON: {exc}", path))
    return {}


def check_tokens(template_dir: Path, issues: list[dict[str, str]]) -> tuple[dict, set[str]]:
    token_path = template_dir / "design_tokens.json"
    tokens = read_json(token_path, issues)
    allowed = {value.upper() for value in tokens.get("allowed_hex", [])}

    if tokens.get("style_system") != STYLE_SYSTEM:
        issues.append(issue("L001-STYLE-SYSTEM", "style_system must be l001_notebook_defense", token_path))

    primary = tokens.get("colors", {}).get("primary")
    if primary != PRIMARY:
        issues.append(issue("L001-COLOR-PRIMARY", f"primary color must be {PRIMARY}, got {primary!r}", token_path))

    if PRIMARY not in allowed:
        issues.append(issue("L001-ALLOWED-HEX", f"{PRIMARY} must appear in allowed_hex", token_path))

    if tokens.get("closing", {}).get("default_title") != "恳请老师批评指正！":
        issues.append(issue("L001-CLOSING-TITLE", "closing.default_title must stay locked", token_path))

    for name, value in tokens.get("colors", {}).items():
        if isinstance(value, str) and value.startswith("#") and value.upper() not in allowed:
            issues.append(issue("L001-COLOR-DRIFT", f"colors.{name}={value} is not in allowed_hex", token_path))

    return tokens, allowed


def check_layouts(template_dir: Path, issues: list[dict[str, str]]) -> dict:
    layouts_path = template_dir / "layouts.json"
    layouts = read_json(layouts_path, issues)
    if layouts.get("style_system") != STYLE_SYSTEM:
        issues.append(issue("L001-LAYOUT-SYSTEM", "layouts.json style_system must be l001_notebook_defense", layouts_path))

    page_types = {
        item.get("page_type")
        for item in layouts.get("layouts", [])
        if isinstance(item, dict)
    }
    if page_types != REQUIRED_PAGE_TYPES:
        issues.append(
            issue(
                "L001-LAYOUT-PAGE-TYPES",
                f"layouts page_type set must be {sorted(REQUIRED_PAGE_TYPES)}, got {sorted(page_types)}",
                layouts_path,
            )
        )
    return layouts


def normalize_viewbox(value: str | None) -> str:
    return " ".join((value or "").replace(",", " ").split())


def check_svg(path: Path, allowed_hex: set[str], issues: list[dict[str, str]]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(issue("L001-MISSING-FILE", f"{path.name} is required", path))
        return

    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        issues.append(issue("L001-SVG-XML", f"{path.name} is not well-formed XML: {exc}", path))
        return

    if normalize_viewbox(root.attrib.get("viewBox")) != VIEWBOX:
        issues.append(issue("L001-SVG-VIEWBOX", f"{path.name} must use viewBox {VIEWBOX}", path))

    if PRIMARY not in text:
        issues.append(issue("L001-SVG-PRIMARY", f"{path.name} must use primary {PRIMARY}", path))

    for found in sorted({match.group(0).upper() for match in HEX_RE.finditer(text)}):
        if found not in allowed_hex:
            issues.append(issue("L001-COLOR-DRIFT", f"{path.name} uses unregistered color {found}", path))

    if "#003366" in text.upper():
        issues.append(issue("L001-COLOR-DRIFT", f"{path.name} uses academic blue #003366", path))


def validate(template_dir: Path) -> dict:
    issues: list[dict[str, str]] = []
    tokens, allowed_hex = check_tokens(template_dir, issues)
    check_layouts(template_dir, issues)

    for svg_name in REQUIRED_SVGS:
        check_svg(template_dir / svg_name, allowed_hex or {PRIMARY}, issues)

    checked_files = 2 + len(REQUIRED_SVGS)
    return {
        "schema_version": "easyslides.l001_validation_report.v1",
        "style_system": STYLE_SYSTEM,
        "template_dir": str(template_dir),
        "status": "pass" if not issues else "fail",
        "checked_files": checked_files,
        "primary": tokens.get("colors", {}).get("primary"),
        "issue_count": len(issues),
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template_dir", nargs="?", default="templates/style_packs/l001_notebook_defense")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    report = validate(Path(args.template_dir))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"L001 validation: {report['status']} ({report['issue_count']} issue(s))")
        for item in report["issues"]:
            loc = f" [{item['path']}]" if "path" in item else ""
            print(f"- {item['code']}: {item['message']}{loc}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
