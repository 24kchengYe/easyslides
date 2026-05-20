#!/usr/bin/env python3
"""Validate slot-guided template text-fit capacity contracts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.template_contract_pack import LAYOUTS_ROOT, ROOT, slot_is_image
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from template_contract_pack import LAYOUTS_ROOT, ROOT, slot_is_image


POLICY_SCHEMA = "easyslides.template_text_fit_policy.v1"
REQUIRED_OVERFLOW_STEPS = (
    "compress_text_to_capacity",
    "choose_lower_density_layout",
    "split_across_slides",
    "shrink_font_with_floor",
)
ROLE_DEFAULT_KEYS = (
    "default_font_size_px",
    "min_font_size_px",
    "line_height",
    "max_chars_per_line_zh",
    "overflow_action",
)
FIXED_TEXT_ROLES = {"page_number"}


def read_json(path: Path, issues: list[dict[str, str]]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        issues.append(issue("TEXT-FIT-MISSING", f"{path.name} is required", path))
        return None
    except json.JSONDecodeError as exc:
        issues.append(issue("TEXT-FIT-JSON", f"{path.name} is invalid JSON: {exc}", path))
        return None
    if not isinstance(payload, dict):
        issues.append(issue("TEXT-FIT-JSON", f"{path.name} must contain a JSON object", path))
        return None
    return payload


def issue(code: str, message: str, path: Path) -> dict[str, str]:
    return {"code": code, "message": message, "path": str(path)}


def resolve_template_dir(value: str | Path) -> Path:
    path = Path(value)
    if path.is_dir():
        return path
    return LAYOUTS_ROOT / str(value)


def numeric(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def validate_policy(policy: dict[str, Any], path: Path, issues: list[dict[str, str]]) -> None:
    if policy.get("schema_version") != POLICY_SCHEMA:
        issues.append(
            issue(
                "TEXT-FIT-POLICY-SCHEMA",
                f"text_fit_policy.schema_version must be {POLICY_SCHEMA}",
                path,
            )
        )

    strategy = policy.get("overflow_strategy_order")
    if not isinstance(strategy, list):
        issues.append(issue("TEXT-FIT-OVERFLOW-STRATEGY", "overflow_strategy_order must be a list", path))
    else:
        missing = [step for step in REQUIRED_OVERFLOW_STEPS if step not in strategy]
        if missing:
            issues.append(
                issue(
                    "TEXT-FIT-OVERFLOW-STRATEGY",
                    f"overflow_strategy_order is missing: {', '.join(missing)}",
                    path,
                )
            )

    role_defaults = policy.get("role_defaults")
    if not isinstance(role_defaults, dict) or not role_defaults:
        issues.append(issue("TEXT-FIT-ROLE-DEFAULTS", "role_defaults must be a non-empty object", path))
        return

    allowed_actions = policy.get("allowed_overflow_actions")
    if not isinstance(allowed_actions, list) or not allowed_actions:
        issues.append(issue("TEXT-FIT-ACTIONS", "allowed_overflow_actions must be a non-empty list", path))


def validate_role_default(
    role: str,
    role_default: dict[str, Any] | None,
    allowed_actions: set[str],
    path: Path,
    issues: list[dict[str, str]],
) -> None:
    if not isinstance(role_default, dict):
        issues.append(issue("TEXT-FIT-ROLE-DEFAULT", f"role {role!r} is missing a capacity default", path))
        return

    for key in ROLE_DEFAULT_KEYS:
        if key not in role_default:
            issues.append(issue("TEXT-FIT-ROLE-DEFAULT", f"role {role!r} is missing {key}", path))

    default_font = numeric(role_default.get("default_font_size_px"))
    min_font = numeric(role_default.get("min_font_size_px"))
    line_height = numeric(role_default.get("line_height"))
    chars = numeric(role_default.get("max_chars_per_line_zh"))
    if default_font is None or default_font <= 0:
        issues.append(issue("TEXT-FIT-FONT", f"role {role!r} default_font_size_px must be positive", path))
    if min_font is None or min_font <= 0:
        issues.append(issue("TEXT-FIT-FONT", f"role {role!r} min_font_size_px must be positive", path))
    if default_font is not None and min_font is not None and min_font > default_font:
        issues.append(issue("TEXT-FIT-FONT", f"role {role!r} min font exceeds default font", path))
    if line_height is None or line_height < 1.0:
        issues.append(issue("TEXT-FIT-LINE-HEIGHT", f"role {role!r} line_height must be >= 1.0", path))
    if chars is None or chars <= 0:
        issues.append(issue("TEXT-FIT-CHARS", f"role {role!r} max_chars_per_line_zh must be positive", path))

    overflow_action = str(role_default.get("overflow_action") or "")
    if allowed_actions and overflow_action not in allowed_actions:
        issues.append(
            issue(
                "TEXT-FIT-ACTION",
                f"role {role!r} overflow_action {overflow_action!r} is not allowed",
                path,
            )
        )


def validate_text_slot(
    model_id: str,
    slot: dict[str, Any],
    role_defaults: dict[str, Any],
    allowed_actions: set[str],
    path: Path,
    issues: list[dict[str, str]],
) -> bool:
    if slot_is_image(slot):
        return False

    slot_id = str(slot.get("slot_id") or "")
    role = str(slot.get("role") or slot_id.lower())
    if role in FIXED_TEXT_ROLES or slot.get("fixed_geometry") is True:
        return False

    role_default = role_defaults.get(role)
    validate_role_default(role, role_default, allowed_actions, path, issues)

    has_capacity = (
        slot.get("max_lines") is not None
        or slot.get("max_items") is not None
        or (isinstance(role_default, dict) and role_default.get("max_lines") is not None)
        or (isinstance(role_default, dict) and role_default.get("max_items") is not None)
    )
    if not has_capacity:
        issues.append(
            issue(
                "TEXT-FIT-SLOT-CAPACITY",
                f"{model_id}.{slot_id} must declare max_lines/max_items or inherit one from role {role!r}",
                path,
            )
        )

    text_fit = slot.get("text_fit")
    if text_fit is not None and str(text_fit) not in {"preserve", "shrink"}:
        issues.append(
            issue(
                "TEXT-FIT-SLOT-POLICY",
                f"{model_id}.{slot_id} text_fit must be preserve or shrink, got {text_fit!r}",
                path,
            )
        )

    return True


def validate_template_text_fit(template: str | Path) -> dict[str, Any]:
    template_dir = resolve_template_dir(template)
    layouts_path = template_dir / "layouts.json"
    issues: list[dict[str, str]] = []
    layouts = read_json(layouts_path, issues)
    checked_text_slot_count = 0
    policy: dict[str, Any] = {}

    if layouts is not None:
        raw_policy = layouts.get("text_fit_policy")
        if not isinstance(raw_policy, dict):
            issues.append(issue("TEXT-FIT-POLICY", "layouts.json must define text_fit_policy", layouts_path))
        else:
            policy = raw_policy
            validate_policy(policy, layouts_path, issues)
            role_defaults = policy.get("role_defaults") if isinstance(policy.get("role_defaults"), dict) else {}
            allowed_actions = set(
                str(action)
                for action in policy.get("allowed_overflow_actions", [])
                if str(action)
            )
            slot_models = layouts.get("slot_models")
            if not isinstance(slot_models, dict):
                issues.append(issue("TEXT-FIT-SLOT-MODELS", "layouts.json slot_models must be an object", layouts_path))
            else:
                for model_id, slots in slot_models.items():
                    if not isinstance(slots, list):
                        issues.append(
                            issue("TEXT-FIT-SLOT-MODEL", f"slot model {model_id!r} must be a list", layouts_path)
                        )
                        continue
                    for slot in slots:
                        if not isinstance(slot, dict):
                            issues.append(
                                issue("TEXT-FIT-SLOT", f"slot model {model_id!r} contains a non-object slot", layouts_path)
                            )
                            continue
                        if validate_text_slot(str(model_id), slot, role_defaults, allowed_actions, layouts_path, issues):
                            checked_text_slot_count += 1

    return {
        "schema_version": "easyslides.template_text_fit_check_report.v1",
        "template_dir": str(template_dir),
        "status": "pass" if not issues else "fail",
        "issue_count": len(issues),
        "checked_text_slot_count": checked_text_slot_count,
        "text_fit_policy": {
            "schema_version": policy.get("schema_version"),
            "overflow_strategy_order": policy.get("overflow_strategy_order", []),
        },
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", help="Template id under templates/layouts or a template directory path.")
    args = parser.parse_args(argv)

    report = validate_template_text_fit(args.template)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
