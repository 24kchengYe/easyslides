#!/usr/bin/env python3
"""Build a searchable Template Asset Bank from PPTX import workspaces.

The input is one or more directories produced by ``pptx_template_import.py``.
The output is a compact manifest for the "exact template reuse" path: each
source slide becomes a fixed module that an agent may select, copy, and edit in
place while preserving geometry and decoration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "easyslides.template_asset_bank.v1"

TEXT_PLACEHOLDERS = {
    "title",
    "ctrTitle",
    "subTitle",
    "body",
    "obj",
    "dt",
    "ftr",
    "hdr",
    "sldNum",
}
IMAGE_PLACEHOLDERS = {"pic", "media"}


class TemplateAssetBankError(RuntimeError):
    """Raised when an import workspace cannot become a template asset bank."""


def build_asset_bank_from_workspaces(
    workspaces: Iterable[str | Path],
    *,
    bank_id: str = "local_template_asset_bank",
) -> dict[str, Any]:
    """Build a Template Asset Bank manifest from PPTX import workspaces."""
    workspace_paths = [Path(path).expanduser().resolve() for path in workspaces]
    if not workspace_paths:
        raise TemplateAssetBankError("at least one import workspace is required")

    templates: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    for workspace in workspace_paths:
        manifest = _load_manifest(workspace)
        template_id = _unique_id(_infer_template_id(manifest, workspace), used_ids)
        used_ids.add(template_id)
        templates.append(_build_template_record(workspace, manifest, template_id))

    return {
        "schema_version": SCHEMA_VERSION,
        "bank_id": bank_id,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generated_by": "scripts/template_asset_bank.py",
        "harness": {
            "primary_mode": "exact_template_reuse",
            "selection_unit": "source_slide_module",
            "template_source": "pptx_template_import workspace",
            "agent_rule": (
                "Select a module by content fit, copy its flat SVG, then replace "
                "text/images inside existing slots while preserving fixed geometry."
            ),
            "fallback": "Use a Style Pack only when no exact template module fits.",
        },
        "templates": templates,
    }


def _load_manifest(workspace: Path) -> dict[str, Any]:
    manifest_path = workspace / "manifest.json"
    if not manifest_path.exists():
        raise TemplateAssetBankError(f"missing manifest.json: {workspace}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TemplateAssetBankError(f"invalid manifest.json in {workspace}: {exc}") from exc
    if not isinstance(manifest, dict):
        raise TemplateAssetBankError(f"manifest.json must be an object: {workspace}")
    return manifest


def _infer_template_id(manifest: dict[str, Any], workspace: Path) -> str:
    source_name = manifest.get("source", {}).get("name")
    if isinstance(source_name, str) and source_name.strip():
        source_slug = _slugify(Path(source_name).stem)
        if _has_ascii_alnum(source_slug):
            return source_slug
    stem = workspace.name
    stem = re.sub(r"(_template_import|[-_]?imported)$", "", stem, flags=re.IGNORECASE)
    return _slugify(stem)


def _unique_id(base: str, used: set[str]) -> str:
    if base not in used:
        return base
    counter = 2
    while f"{base}_{counter}" in used:
        counter += 1
    return f"{base}_{counter}"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip()).strip("_").lower()
    return slug or "template"


def _has_ascii_alnum(value: str) -> bool:
    return any(char.isascii() and char.isalnum() for char in value)


def _build_template_record(
    workspace: Path,
    manifest: dict[str, Any],
    template_id: str,
) -> dict[str, Any]:
    layout_by_path = {
        item.get("path"): item
        for item in manifest.get("layouts", [])
        if isinstance(item, dict) and item.get("path")
    }
    master_by_path = {
        item.get("path"): item
        for item in manifest.get("masters", [])
        if isinstance(item, dict) and item.get("path")
    }

    pages = [
        _build_page_record(workspace, manifest, template_id, slide, layout_by_path, master_by_path)
        for slide in manifest.get("slides", [])
        if isinstance(slide, dict)
    ]
    if not pages:
        raise TemplateAssetBankError(f"manifest has no slides: {workspace}")

    return {
        "template_id": template_id,
        "source_name": manifest.get("source", {}).get("name", workspace.name),
        "source_pptx": manifest.get("source", {}).get("pptx"),
        "import_workspace": str(workspace),
        "slide_size": manifest.get("slideSize", {}),
        "theme": manifest.get("theme", {}),
        "assets": {
            "dir": manifest.get("assets", {}).get("exportDir", "assets"),
            "all": manifest.get("assets", {}).get("allAssets", []),
            "common": manifest.get("assets", {}).get("commonAssets", []),
        },
        "module_count": len(pages),
        "page_type_candidates": manifest.get("pageTypeCandidates", {}),
        "pages": pages,
    }


def _build_page_record(
    workspace: Path,
    manifest: dict[str, Any],
    template_id: str,
    slide: dict[str, Any],
    layout_by_path: dict[str, dict[str, Any]],
    master_by_path: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    index = int(slide.get("index", 0) or 0)
    if index <= 0:
        raise TemplateAssetBankError(f"slide has invalid index in {workspace}: {slide!r}")
    page_type = str(slide.get("pageType") or "content")

    flat_svg_file = str(slide.get("flatSvgFile") or "")
    layered_svg_file = str(slide.get("svgFile") or "")
    flat_path = workspace / "svg-flat" / flat_svg_file
    layered_path = workspace / "svg" / layered_svg_file
    if not flat_svg_file or not flat_path.exists():
        raise TemplateAssetBankError(
            f"missing flat SVG for slide {index}: {flat_path}"
        )
    if not layered_svg_file or not layered_path.exists():
        raise TemplateAssetBankError(
            f"missing layered SVG for slide {index}: {layered_path}"
        )

    layout = layout_by_path.get(slide.get("layoutPath") or "")
    master = master_by_path.get(slide.get("masterPath") or "")
    slots = _slots_for_slide(layout, master)

    module_basename = f"{index:03d}_{_slugify(page_type)}"
    return {
        "module_id": f"{template_id}/{module_basename}",
        "module_basename": module_basename,
        "source_slide_index": index,
        "page_type": page_type,
        "layout_path": slide.get("layoutPath"),
        "master_path": slide.get("masterPath"),
        "source": {
            "flat_svg": _relative_posix(flat_path, workspace),
            "layered_svg": _relative_posix(layered_path, workspace),
        },
        "text_samples": slide.get("textSamples", []),
        "assets": {
            "background": slide.get("backgroundAsset"),
            "images": slide.get("imageAssets", []),
        },
        "metrics": {
            "text_count": slide.get("textCount", 0),
            "shape_count": slide.get("shapeCount", 0),
            "slot_count": len(slots),
        },
        "slots": slots,
        "reuse_contract": _exact_reuse_contract(),
        "search_hints": _search_hints(manifest, slide, page_type),
    }


def _slots_for_slide(
    layout: dict[str, Any] | None,
    master: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    slots: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for source, part in (("layout", layout), ("master", master)):
        if not part:
            continue
        for placeholder in part.get("placeholders", []):
            if not isinstance(placeholder, dict):
                continue
            slot = _normalize_slot(placeholder, source)
            key = (slot["slot_id"], source)
            if key in seen:
                continue
            seen.add(key)
            slots.append(slot)
    return slots


def _normalize_slot(placeholder: dict[str, Any], source: str) -> dict[str, Any]:
    ph_type = str(placeholder.get("type") or "placeholder")
    idx = str(placeholder.get("idx") or "0")
    slot_id = f"{ph_type}_{idx}"
    kind = _slot_kind(ph_type)
    slot = {
        "slot_id": slot_id,
        "kind": kind,
        "placeholder_type": ph_type,
        "idx": idx,
        "source": source,
        "geometry": placeholder.get("geometry"),
    }
    if placeholder.get("textStyle"):
        slot["text_style"] = placeholder["textStyle"]
    if placeholder.get("textSamples"):
        slot["text_samples"] = placeholder["textSamples"]
    return slot


def _slot_kind(ph_type: str) -> str:
    if ph_type in IMAGE_PLACEHOLDERS:
        return "image"
    if ph_type in TEXT_PLACEHOLDERS:
        return "text"
    return "content"


def _exact_reuse_contract() -> dict[str, Any]:
    return {
        "mode": "exact_template_reuse",
        "allowed_edits": [
            "replace text in existing text elements",
            "replace images inside existing picture/media slots",
            "update chart/table labels only when the source slide already contains that structure",
        ],
        "forbidden_edits": [
            "move, resize, recolor, or delete fixed geometry",
            "invent new layout grids or decorative shapes",
            "convert the module into a free-form Style Pack page",
        ],
        "content_fit_rule": (
            "If content does not fit the existing slots, choose another module, "
            "split the content across pages, or warn before simplifying."
        ),
    }


def _search_hints(manifest: dict[str, Any], slide: dict[str, Any], page_type: str) -> list[str]:
    hints = [page_type]
    hints.extend(str(text) for text in slide.get("textSamples", [])[:4])
    for asset in slide.get("imageAssets", [])[:3]:
        hints.append(str(asset))
    source_name = manifest.get("source", {}).get("name")
    if source_name:
        hints.append(str(source_name))
    return [hint for hint in hints if hint]


def _relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Template Asset Bank from one or more pptx_template_import workspaces."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser(
        "build",
        help="Build template_asset_bank.json from import workspaces.",
    )
    build.add_argument("workspaces", nargs="+", help="Directories containing manifest.json")
    build.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    build.add_argument(
        "--bank-id",
        default="local_template_asset_bank",
        help="Stable identifier for the generated bank",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "build":
            bank = build_asset_bank_from_workspaces(args.workspaces, bank_id=args.bank_id)
        else:  # pragma: no cover - argparse prevents this branch.
            raise TemplateAssetBankError(f"unknown command: {args.command}")
    except TemplateAssetBankError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    payload = json.dumps(bank, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
