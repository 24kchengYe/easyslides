#!/usr/bin/env python3
"""Validate and resolve style-pack contracts declared in spec_lock.md.

The current implementation supports the Guizang editable style pack. It turns
machine-readable `## style_pack` + `## page_layouts` rows into concrete SVG
paths so Strategist and Executor can share the same contract instead of relying
on prose style descriptions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


STYLE_PACK_SECTION = "style_pack"
PAGE_LAYOUTS_SECTION = "page_layouts"
SUPPORTED_PACKAGES = {"guizang_ppt"}
STYLE_PACKS_DIR = Path("templates") / "style_packs"
LOCK_ROW_RE = re.compile(r"^-\s+([A-Za-z0-9_]+)\s*:\s*(.+?)\s*$")


def issue(code: str, message: str, path: Path | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if path is not None:
        item["path"] = str(path)
    return item


def parse_lock(lock_path: Path) -> dict[str, dict[str, str]]:
    """Parse the simple `## section` / `- key: value` spec_lock format."""
    sections: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw in lock_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, {})
            continue
        if current is None:
            continue
        match = LOCK_ROW_RE.match(line)
        if match:
            sections[current][match.group(1)] = match.group(2).strip()
    return sections


def read_json(path: Path, issues: list[dict[str, str]]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(issue("GUZ-STYLE-PACK-MISSING", f"{path.name} is required", path))
        return {}
    except json.JSONDecodeError as exc:
        issues.append(issue("GUZ-STYLE-PACK-JSON", f"{path.name} is invalid JSON: {exc}", path))
        return {}
    if not isinstance(data, dict):
        issues.append(issue("GUZ-STYLE-PACK-JSON", f"{path.name} must contain a JSON object", path))
        return {}
    return data


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _package_root(contract: dict[str, str], repo_root: Path, issues: list[dict[str, str]]) -> Path:
    package = contract.get("package", "")
    layout_source = contract.get("layout_source")
    if layout_source:
        root = (repo_root / layout_source).resolve()
        legacy_root = (repo_root / "templates" / package).resolve()
        canonical_root = (repo_root / STYLE_PACKS_DIR / package).resolve()
        if root == legacy_root and not root.exists() and canonical_root.exists():
            root = canonical_root
    else:
        root = (repo_root / STYLE_PACKS_DIR / package).resolve()

    if not root.exists():
        issues.append(
            issue(
                "GUZ-STYLE-PACK-ROOT",
                f"style_pack root does not exist: {_repo_relative(root, repo_root)}",
                root,
            )
        )
    return root


def _layout_aliases(template: str, package: str, package_root: Path, repo_root: Path) -> set[str]:
    path = Path(template)
    no_ext = path.with_suffix("").as_posix()
    full = (package_root / template).resolve()
    rel_full = _repo_relative(full, repo_root)
    rel_no_ext = str(Path(rel_full).with_suffix("")).replace("\\", "/")

    aliases = {
        template,
        template.removesuffix(".svg"),
        no_ext,
        path.name,
        path.stem,
        rel_full,
        rel_no_ext,
        f"templates/style_packs/{package}/{template}",
        f"templates/style_packs/{package}/{template}".removesuffix(".svg"),
        f"templates/{package}/{template}",
        f"templates/{package}/{template}".removesuffix(".svg"),
    }
    return {alias.replace("\\", "/") for alias in aliases if alias}


def build_layout_index(
    layouts: dict[str, Any],
    *,
    package: str,
    variant: str,
    package_root: Path,
    repo_root: Path,
    issues: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    """Return accepted layout aliases mapped to concrete package SVG paths."""
    variants = layouts.get("variants", {})
    variant_data = variants.get(variant)
    if not isinstance(variant_data, dict):
        return {}

    index: dict[str, dict[str, str]] = {}
    layout_rows: list[dict[str, Any]] = []
    layout_rows.extend(item for item in variant_data.get("native_shells", []) if isinstance(item, dict))
    layout_rows.extend(item for item in variant_data.get("native_layouts", []) if isinstance(item, dict))

    for row in layout_rows:
        template = row.get("template")
        if not isinstance(template, str) or not template:
            continue
        svg_path = (package_root / template).resolve()
        record = {
            "id": str(row.get("id", "")),
            "name": str(row.get("name", "")),
            "template": template,
            "path": _repo_relative(svg_path, repo_root),
        }
        aliases = _layout_aliases(template, package, package_root, repo_root)
        if row.get("id"):
            aliases.add(str(row["id"]))
        for alias in aliases:
            previous = index.get(alias)
            if previous and previous["path"] != record["path"]:
                issues.append(
                    issue(
                        "GUZ-STYLE-PACK-ALIAS",
                        f"layout alias {alias!r} is ambiguous: {previous['path']} vs {record['path']}",
                        package_root / "layouts.json",
                    )
                )
                continue
            index[alias] = record
    return index


def _normalize_layout_value(value: str) -> str:
    value = value.strip()
    if "|" in value:
        value = value.split("|", 1)[0].strip()
    return value.replace("\\", "/")


def validate_spec_lock(spec_lock_path: Path, *, repo_root: Path | None = None) -> dict[str, Any]:
    """Validate a style_pack contract and resolve page_layouts entries."""
    repo = (repo_root or Path.cwd()).resolve()
    lock = spec_lock_path.resolve()
    issues: list[dict[str, str]] = []

    if not lock.exists():
        issues.append(issue("GUZ-STYLE-PACK-LOCK", "spec_lock.md not found", lock))
        return {
            "schema_version": "easyslides.style_pack_contract_report.v1",
            "status": "fail",
            "spec_lock": str(lock),
            "issue_count": len(issues),
            "issues": issues,
            "style_pack": {},
            "resolved_layouts": {},
        }

    sections = parse_lock(lock)

    contract = sections.get(STYLE_PACK_SECTION, {})
    page_layouts = sections.get(PAGE_LAYOUTS_SECTION, {})
    resolved_layouts: dict[str, dict[str, str]] = {}

    if not contract:
        return {
            "schema_version": "easyslides.style_pack_contract_report.v1",
            "status": "skipped",
            "spec_lock": str(lock),
            "issue_count": 0,
            "issues": [],
            "style_pack": {},
            "resolved_layouts": {},
        }

    package = contract.get("package", "")
    variant = contract.get("variant", "")
    theme = contract.get("theme", "")

    if package not in SUPPORTED_PACKAGES:
        issues.append(
            issue(
                "GUZ-STYLE-PACK-PACKAGE",
                f"unsupported style_pack package {package!r}; expected one of {sorted(SUPPORTED_PACKAGES)}",
                lock,
            )
        )

    for key in ("package", "variant", "theme"):
        if not contract.get(key):
            issues.append(issue("GUZ-STYLE-PACK-KEY", f"style_pack.{key} is required", lock))

    package_root = _package_root(contract, repo, issues)
    tokens = read_json(package_root / "design_tokens.json", issues)
    layouts = read_json(package_root / "layouts.json", issues)

    token_variant = tokens.get("variants", {}).get(variant)
    layout_variant = layouts.get("variants", {}).get(variant)
    if variant and not isinstance(token_variant, dict):
        issues.append(issue("GUZ-STYLE-PACK-VARIANT", f"unknown Guizang variant {variant!r}", lock))
    if variant and not isinstance(layout_variant, dict):
        issues.append(issue("GUZ-STYLE-PACK-VARIANT", f"variant {variant!r} is missing in layouts.json", lock))
    if isinstance(token_variant, dict) and theme not in token_variant.get("themes", {}):
        issues.append(issue("GUZ-STYLE-PACK-THEME", f"unknown theme {theme!r} for {variant}", lock))

    layout_index = build_layout_index(
        layouts,
        package=package or "guizang_ppt",
        variant=variant,
        package_root=package_root,
        repo_root=repo,
        issues=issues,
    )

    for page, raw_value in sorted(page_layouts.items()):
        layout_key = _normalize_layout_value(raw_value)
        record = layout_index.get(layout_key)
        if record is None and layout_key.endswith(".svg"):
            record = layout_index.get(layout_key.removesuffix(".svg"))
        if record is None:
            issues.append(
                issue(
                    "GUZ-STYLE-PACK-LAYOUT",
                    f"page_layouts {page} references unknown Guizang layout {raw_value!r}",
                    lock,
                )
            )
            continue
        svg_path = repo / record["path"]
        if not svg_path.exists():
            issues.append(
                issue(
                    "GUZ-STYLE-PACK-LAYOUT-MISSING",
                    f"page_layouts {page} resolves to missing file {record['path']}",
                    svg_path,
                )
            )
        resolved_layouts[page] = record

    return {
        "schema_version": "easyslides.style_pack_contract_report.v1",
        "status": "pass" if not issues else "fail",
        "spec_lock": str(lock),
        "issue_count": len(issues),
        "issues": issues,
        "style_pack": {
            "package": package,
            "variant": variant,
            "theme": theme,
            "layout_source": contract.get("layout_source", f"templates/style_packs/{package}"),
            "root": _repo_relative(package_root, repo),
        },
        "resolved_layouts": resolved_layouts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_lock", type=Path, help="Path to a project spec_lock.md")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root used to resolve templates/<package> paths",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)

    report = validate_spec_lock(args.spec_lock, repo_root=args.repo_root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Style-pack contract: {report['status']} ({report['issue_count']} issue(s))")
        for page, record in report["resolved_layouts"].items():
            print(f"- {page}: {record['path']}")
        for item in report["issues"]:
            loc = f" [{item['path']}]" if "path" in item else ""
            print(f"- {item['code']}: {item['message']}{loc}")
    return 0 if report["status"] in {"pass", "skipped"} else 1


if __name__ == "__main__":
    sys.exit(main())
