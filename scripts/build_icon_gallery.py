from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ICONS_DIR = ROOT / "templates" / "icons"
DEFAULT_MANIFEST = DEFAULT_ICONS_DIR / "icons_manifest.js"
PREFERRED_FAMILY_ORDER = [
    "chunk-filled",
    "lucide",
    "phosphor-duotone",
    "simple-icons",
    "tabler-filled",
    "tabler-outline",
]


def family_sort_key(path: Path) -> tuple[int, str]:
    try:
        return (PREFERRED_FAMILY_ORDER.index(path.name), path.name)
    except ValueError:
        return (len(PREFERRED_FAMILY_ORDER), path.name)


def build_manifest(icons_dir: Path) -> dict:
    icons_dir = icons_dir.resolve()
    if not icons_dir.exists():
        raise FileNotFoundError(f"Icon directory not found: {icons_dir}")

    families = []
    for family_dir in sorted(
        [path for path in icons_dir.iterdir() if path.is_dir()],
        key=family_sort_key,
    ):
        svg_paths = sorted(family_dir.glob("*.svg"), key=lambda path: path.stem.lower())
        if not svg_paths:
            continue

        icons = []
        for svg_path in svg_paths:
            rel_path = svg_path.relative_to(icons_dir).as_posix()
            icons.append(
                {
                    "name": svg_path.stem,
                    "token": f"{family_dir.name}/{svg_path.stem}",
                    "path": rel_path,
                }
            )

        families.append(
            {
                "id": family_dir.name,
                "count": len(icons),
                "icons": icons,
            }
        )

    return {
        "schema_version": "easyslides.icons_manifest.v1",
        "total": sum(family["count"] for family in families),
        "families": families,
    }


def write_manifest_js(manifest: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
    output_path.write_text(f"window.ICON_MANIFEST = {payload};\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the browser-ready icon manifest for templates/icons/index.html."
    )
    parser.add_argument("--icons-dir", type=Path, default=DEFAULT_ICONS_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    manifest = build_manifest(args.icons_dir)
    write_manifest_js(manifest, args.manifest)
    print(
        f"wrote {args.manifest} with {manifest['total']} icons "
        f"across {len(manifest['families'])} families"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
