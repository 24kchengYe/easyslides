#!/usr/bin/env python3
"""Materialize a layout template with one of its declared theme palettes."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
LAYOUTS_DIR = ROOT / "templates" / "layouts"

TEXT_EXTENSIONS = {".md", ".svg", ".txt"}
JSON_EXTENSIONS = {".json"}
PALETTE_FILENAME = "theme_palettes.json"


class PaletteError(RuntimeError):
    """Raised when a template palette catalog is missing or invalid."""


def _normalize_hex(value: str) -> str:
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise PaletteError(f"Expected 6-digit hex color, got {value!r}")
    return value.upper()


def read_palette_catalog(template_dir: Path) -> dict[str, Any]:
    """Read ``theme_palettes.json`` from a template directory."""
    catalog_path = template_dir / PALETTE_FILENAME
    if not catalog_path.exists():
        raise PaletteError(f"Palette catalog not found: {catalog_path}")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(catalog, dict):
        raise PaletteError(f"Palette catalog must be a JSON object: {catalog_path}")
    if "palettes" not in catalog or not isinstance(catalog["palettes"], dict):
        raise PaletteError(f"Palette catalog has no palettes object: {catalog_path}")
    return catalog


def palette_color_replacements(catalog: dict[str, Any], palette_id: str) -> dict[str, str]:
    """Return old-color to new-color replacements for ``palette_id``."""
    palettes = catalog.get("palettes")
    if not isinstance(palettes, dict):
        raise PaletteError("Palette catalog has no palettes object")

    default_palette_id = str(catalog.get("default_palette", ""))
    if not default_palette_id or default_palette_id not in palettes:
        raise PaletteError("Palette catalog default_palette is missing or unknown")
    if palette_id not in palettes:
        available = ", ".join(sorted(palettes))
        raise PaletteError(f"Unknown palette {palette_id!r}; available: {available}")

    replace_roles = catalog.get("replace_roles")
    if not isinstance(replace_roles, list) or not replace_roles:
        raise PaletteError("Palette catalog replace_roles must be a non-empty list")

    default_colors = palettes[default_palette_id].get("colors", {})
    target_colors = palettes[palette_id].get("colors", {})
    replacements: dict[str, str] = {}
    for role in replace_roles:
        if role not in default_colors:
            raise PaletteError(f"Default palette is missing replace role {role!r}")
        if role not in target_colors:
            raise PaletteError(f"Palette {palette_id!r} is missing replace role {role!r}")
        replacements[_normalize_hex(str(default_colors[role]))] = _normalize_hex(str(target_colors[role]))
    return replacements


def apply_color_replacements(text: str, replacements: dict[str, str]) -> str:
    """Replace exact hex colors in text, case-insensitively."""
    if not replacements:
        return text
    normalized = {_normalize_hex(old): _normalize_hex(new) for old, new in replacements.items()}
    pattern = re.compile("|".join(re.escape(color) for color in sorted(normalized, key=len, reverse=True)), re.IGNORECASE)
    return pattern.sub(lambda match: normalized[match.group(0).upper()], text)


def _replace_in_json(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: _replace_in_json(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [_replace_in_json(item, replacements) for item in value]
    if isinstance(value, str):
        return apply_color_replacements(value, replacements)
    return value


def _assert_output_is_not_template_child(template_dir: Path, output_dir: Path) -> None:
    template_root = template_dir.resolve()
    output_root = output_dir.resolve()
    if output_root == template_root:
        raise PaletteError("Output directory must not be the source template directory")
    try:
        is_child = output_root.is_relative_to(template_root)
    except AttributeError:  # pragma: no cover - Python 3.8 fallback
        is_child = str(output_root).startswith(str(template_root) + str(Path.sep))
    if is_child:
        raise PaletteError("Output directory must not be inside the source template directory")


def materialize_template_palette(template_dir: Path, palette_id: str, output_dir: Path) -> list[Path]:
    """Copy a template folder to ``output_dir`` with semantic theme colors replaced."""
    if not template_dir.is_dir():
        raise PaletteError(f"Template directory not found: {template_dir}")
    _assert_output_is_not_template_child(template_dir, output_dir)

    catalog = read_palette_catalog(template_dir)
    replacements = palette_color_replacements(catalog, palette_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for source in sorted(template_dir.rglob("*")):
        relative = source.relative_to(template_dir)
        target = output_dir / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        if source.name == PALETTE_FILENAME:
            shutil.copy2(source, target)
        elif source.suffix.lower() in JSON_EXTENSIONS:
            data = json.loads(source.read_text(encoding="utf-8"))
            target.write_text(
                json.dumps(_replace_in_json(data, replacements), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        elif source.suffix.lower() in TEXT_EXTENSIONS:
            target.write_text(
                apply_color_replacements(source.read_text(encoding="utf-8"), replacements),
                encoding="utf-8",
            )
        else:
            shutil.copy2(source, target)
        written.append(target)
    return written


def _resolve_template_dir(template: str) -> Path:
    direct = Path(template)
    if direct.is_dir():
        return direct
    return LAYOUTS_DIR / template


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Materialize a layout template with one declared theme palette."
    )
    parser.add_argument("template", help="Template id under templates/layouts/ or an explicit template directory")
    parser.add_argument("palette", help="Palette id from theme_palettes.json")
    parser.add_argument(
        "--output-dir",
        help="Output directory. Defaults to tmp/template_palettes/<template>_<palette>.",
    )
    args = parser.parse_args(argv)

    template_dir = _resolve_template_dir(args.template)
    output_dir = Path(args.output_dir) if args.output_dir else ROOT / "tmp" / "template_palettes" / f"{template_dir.name}_{args.palette}"

    try:
        written = materialize_template_palette(template_dir, args.palette, output_dir)
    except PaletteError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "template": str(template_dir),
                "palette": args.palette,
                "output_dir": str(output_dir),
                "files_written": len(written),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
