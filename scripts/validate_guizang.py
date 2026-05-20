#!/usr/bin/env python3
"""Validate the Guizang editable PPT style migration pack."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


STYLE_SYSTEM = "guizang_ppt"
VIEWBOX = "0 0 1280 720"
REQUIRED_SVGS = (
    "style_a/01_cover.svg",
    "style_a/02_section.svg",
    "style_a/03_content.svg",
    "style_a/04_closing.svg",
    "style_b/01_cover.svg",
    "style_b/02_statement.svg",
    "style_b/03_content.svg",
    "style_b/04_image_hero.svg",
    "style_b/05_closing.svg",
)
STYLE_A_SVGS = REQUIRED_SVGS[:4]
STYLE_B_SVGS = REQUIRED_SVGS[4:]
STYLE_A_THEME_COUNT = 5
STYLE_B_THEME_COUNT = 4
SWISS_LAYOUT_IDS = {f"S{idx:02d}" for idx in range(1, 23)}
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6,8}\b")
DISALLOWED_SVG_TAGS = {"foreignObject", "script", "style", "canvas", "video", "iframe"}


def issue(code: str, message: str, path: Path | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if path is not None:
        item["path"] = str(path)
    return item


def read_json(path: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(issue("GUZ-MISSING-FILE", f"{path.name} is required", path))
        return {}
    except json.JSONDecodeError as exc:
        issues.append(issue("GUZ-JSON", f"{path.name} is not valid JSON: {exc}", path))
        return {}
    if not isinstance(data, dict):
        issues.append(issue("GUZ-JSON", f"{path.name} must contain a JSON object", path))
        return {}
    return data


def normalize_viewbox(value: str | None) -> str:
    return " ".join((value or "").replace(",", " ").split())


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def iter_hex_values(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.extend(match.group(0).upper() for match in HEX_RE.finditer(value))
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(iter_hex_values(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(iter_hex_values(item))
    return found


def check_tokens(template_dir: Path, issues: list[dict[str, str]]) -> tuple[dict[str, Any], set[str]]:
    token_path = template_dir / "design_tokens.json"
    tokens = read_json(token_path, issues)
    allowed = {str(value).upper() for value in tokens.get("allowed_hex", [])}

    if tokens.get("style_system") != STYLE_SYSTEM:
        issues.append(issue("GUZ-STYLE-SYSTEM", "style_system must be guizang_ppt", token_path))

    source = tokens.get("source", {})
    if source.get("upstream_repo") != "https://github.com/op7418/guizang-ppt-skill":
        issues.append(issue("GUZ-SOURCE", "source.upstream_repo must point to op7418/guizang-ppt-skill", token_path))
    if not source.get("upstream_commit"):
        issues.append(issue("GUZ-SOURCE", "source.upstream_commit is required", token_path))

    variants = tokens.get("variants", {})
    style_a = variants.get("style_a_editorial_ink", {})
    style_b = variants.get("style_b_swiss", {})
    if len(style_a.get("themes", {})) != STYLE_A_THEME_COUNT:
        issues.append(issue("GUZ-STYLE-A-THEMES", "Style A must keep the 5 upstream theme presets", token_path))
    if len(style_b.get("themes", {})) != STYLE_B_THEME_COUNT:
        issues.append(issue("GUZ-STYLE-B-THEMES", "Style B must keep the 4 upstream Swiss theme presets", token_path))

    for found in sorted(set(iter_hex_values(tokens))):
        if found not in allowed:
            issues.append(issue("GUZ-COLOR-DRIFT", f"unregistered token color {found}", token_path))

    return tokens, allowed


def check_layouts(template_dir: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    layouts_path = template_dir / "layouts.json"
    layouts = read_json(layouts_path, issues)
    if layouts.get("style_system") != STYLE_SYSTEM:
        issues.append(issue("GUZ-LAYOUT-SYSTEM", "layouts.json style_system must be guizang_ppt", layouts_path))

    variants = layouts.get("variants", {})
    style_a = variants.get("style_a_editorial_ink", {})
    style_b = variants.get("style_b_swiss", {})

    style_a_pages = {item.get("page_type") for item in style_a.get("native_shells", []) if isinstance(item, dict)}
    if style_a_pages != {"cover", "section", "content", "closing"}:
        issues.append(issue("GUZ-STYLE-A-PAGE-TYPES", "Style A shells must cover cover/section/content/closing", layouts_path))

    style_b_pages = {item.get("page_type") for item in style_b.get("native_shells", []) if isinstance(item, dict)}
    if style_b_pages != {"cover", "statement", "content", "image_hero", "closing"}:
        issues.append(issue("GUZ-STYLE-B-PAGE-TYPES", "Style B shells must cover cover/statement/content/image_hero/closing", layouts_path))

    registered = set(style_b.get("registered_layouts", []))
    if registered != SWISS_LAYOUT_IDS:
        issues.append(issue("GUZ-SWISS-LAYOUTS", "Style B must register upstream S01-S22 layout IDs", layouts_path))

    native_layouts = style_b.get("native_layouts", [])
    native_layout_ids = {
        item.get("id")
        for item in native_layouts
        if isinstance(item, dict)
    }
    if native_layout_ids != SWISS_LAYOUT_IDS:
        issues.append(issue("GUZ-SWISS-NATIVE-LAYOUTS", "Style B native layouts must cover S01-S22", layouts_path))

    for item in native_layouts:
        if not isinstance(item, dict):
            issues.append(issue("GUZ-SWISS-NATIVE-LAYOUT", "native_layouts entries must be objects", layouts_path))
            continue
        template = item.get("template")
        if template and not (template_dir / template).exists():
            issues.append(issue("GUZ-LAYOUT-MISSING-SVG", f"Style B native layout references missing {template}", layouts_path))

    for variant_name, variant in variants.items():
        for shell in variant.get("native_shells", []):
            template = shell.get("template") if isinstance(shell, dict) else None
            if template and not (template_dir / template).exists():
                issues.append(issue("GUZ-LAYOUT-MISSING-SVG", f"{variant_name} shell references missing {template}", layouts_path))

    return layouts


def check_svg(path: Path, allowed_hex: set[str], issues: list[dict[str, str]]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(issue("GUZ-MISSING-FILE", f"{path.name} is required", path))
        return

    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        issues.append(issue("GUZ-SVG-XML", f"{path.name} is not well-formed XML: {exc}", path))
        return

    if normalize_viewbox(root.attrib.get("viewBox")) != VIEWBOX:
        issues.append(issue("GUZ-SVG-VIEWBOX", f"{path.name} must use viewBox {VIEWBOX}", path))

    if local_name(root.tag) != "svg":
        issues.append(issue("GUZ-SVG-ROOT", f"{path.name} root must be svg", path))

    for node in root.iter():
        name = local_name(node.tag)
        if name in DISALLOWED_SVG_TAGS:
            issues.append(issue("GUZ-SVG-DISALLOWED-TAG", f"{path.name} uses disallowed <{name}>", path))

    for found in sorted({match.group(0).upper() for match in HEX_RE.finditer(text)}):
        if found not in allowed_hex:
            issues.append(issue("GUZ-COLOR-DRIFT", f"{path.name} uses unregistered color {found}", path))

    is_swiss_native_layout = path.parent.name == "swiss"
    is_style_b_svg = path.name in STYLE_B_SVGS or is_swiss_native_layout

    if path.name in STYLE_A_SVGS and 'data-style="guizang-style-a"' not in text:
        issues.append(issue("GUZ-SVG-STYLE", f"{path.name} must declare data-style guizang-style-a", path))
    if is_style_b_svg and 'data-style="guizang-style-b"' not in text:
        issues.append(issue("GUZ-SVG-STYLE", f"{path.name} must declare data-style guizang-style-b", path))

    if is_swiss_native_layout:
        layout_id = root.attrib.get("data-layout")
        if layout_id not in SWISS_LAYOUT_IDS:
            issues.append(issue("GUZ-SWISS-DATA-LAYOUT", f"{path.name} must declare data-layout S01-S22", path))

    if is_style_b_svg:
        if "#002FA7" not in text:
            issues.append(issue("GUZ-SWISS-ACCENT", f"{path.name} must use default IKB accent #002FA7", path))
        if "filter=" in text or "linearGradient" in text or "radialGradient" in text:
            issues.append(issue("GUZ-SWISS-PURITY", f"{path.name} must avoid gradients and filters", path))


def validate(
    template_dir: Path,
    *,
    spec_lock_path: Path | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    tokens, allowed_hex = check_tokens(template_dir, issues)
    layouts = check_layouts(template_dir, issues)

    for svg_name in REQUIRED_SVGS:
        check_svg(template_dir / svg_name, allowed_hex or set(), issues)

    native_layouts = (
        layouts
        .get("variants", {})
        .get("style_b_swiss", {})
        .get("native_layouts", [])
    )
    swiss_svg_count = 0
    for item in native_layouts:
        if not isinstance(item, dict) or not item.get("template"):
            continue
        swiss_svg_count += 1
        check_svg(template_dir / item["template"], allowed_hex or set(), issues)

    checked_files = 2 + len(REQUIRED_SVGS) + swiss_svg_count
    style_pack_contract = None
    if spec_lock_path is not None:
        from style_pack_contract import validate_spec_lock

        style_pack_contract = validate_spec_lock(
            spec_lock_path,
            repo_root=repo_root or Path.cwd(),
        )
        if style_pack_contract["status"] == "fail":
            issues.extend(style_pack_contract["issues"])

    return {
        "schema_version": "easyslides.guizang_validation_report.v1",
        "style_system": STYLE_SYSTEM,
        "template_dir": str(template_dir),
        "status": "pass" if not issues else "fail",
        "checked_files": checked_files,
        "source": tokens.get("source", {}),
        "issue_count": len(issues),
        "issues": issues,
        "style_pack_contract": style_pack_contract,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template_dir", nargs="?", default="templates/style_packs/guizang_ppt")
    parser.add_argument(
        "--spec-lock",
        type=Path,
        help="Also validate a project spec_lock.md style_pack contract",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root for resolving style_pack paths",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    report = validate(
        Path(args.template_dir),
        spec_lock_path=args.spec_lock,
        repo_root=args.repo_root,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Guizang validation: {report['status']} ({report['issue_count']} issue(s))")
        for item in report["issues"]:
            loc = f" [{item['path']}]" if "path" in item else ""
            print(f"- {item['code']}: {item['message']}{loc}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
