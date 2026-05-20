import json
import tempfile
import unittest
from pathlib import Path


def write_layouts(path: Path, *, include_caption_default: bool = True) -> None:
    role_defaults = {
        "title": {
            "default_font_size_px": 28,
            "min_font_size_px": 22,
            "line_height": 1.2,
            "max_chars_per_line_zh": 18,
            "overflow_action": "split",
            "max_lines": 2,
        },
        "body": {
            "default_font_size_px": 22,
            "min_font_size_px": 18,
            "line_height": 1.25,
            "max_chars_per_line_zh": 24,
            "overflow_action": "split",
            "max_lines": 5,
        },
    }
    if include_caption_default:
        role_defaults["caption"] = {
            "default_font_size_px": 16,
            "min_font_size_px": 12,
            "line_height": 1.15,
            "max_chars_per_line_zh": 30,
            "overflow_action": "truncate",
            "max_lines": 2,
        }

    payload = {
        "template_id": "fixture_slot",
        "text_fit_policy": {
            "schema_version": "easyslides.template_text_fit_policy.v1",
            "overflow_strategy_order": [
                "compress_text_to_capacity",
                "choose_lower_density_layout",
                "split_across_slides",
                "shrink_font_with_floor",
            ],
            "allowed_overflow_actions": ["split", "truncate"],
            "role_defaults": role_defaults,
        },
        "slot_models": {
            "content": [
                {"slot_id": "PAGE_TITLE", "role": "title", "max_lines": 2},
                {"slot_id": "BODY", "role": "body", "max_lines": 5},
                {"slot_id": "CAPTION", "role": "caption", "max_lines": 2},
                {"slot_id": "MAIN_EXHIBIT", "role": "main_figure", "image_fit": "contain"},
                {"slot_id": "PAGE_NUM", "role": "page_number"},
            ]
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class TemplateTextFitCheckTests(unittest.TestCase):
    def test_slot_guided_fixture_has_complete_text_fit_policy(self):
        from scripts.template_text_fit_check import validate_template_text_fit

        with tempfile.TemporaryDirectory() as tmp:
            template_dir = Path(tmp) / "fixture_slot"
            template_dir.mkdir()
            write_layouts(template_dir / "layouts.json")
            report = validate_template_text_fit(template_dir)

        self.assertEqual(report["status"], "pass", report["issues"])
        self.assertEqual(
            report["text_fit_policy"]["schema_version"],
            "easyslides.template_text_fit_policy.v1",
        )
        self.assertEqual(report["checked_text_slot_count"], 3)

    def test_text_fit_check_rejects_missing_role_capacity_default(self):
        from scripts.template_text_fit_check import validate_template_text_fit

        with tempfile.TemporaryDirectory() as tmp:
            template_dir = Path(tmp) / "fixture_slot"
            template_dir.mkdir()
            write_layouts(template_dir / "layouts.json", include_caption_default=False)
            report = validate_template_text_fit(template_dir)

        self.assertEqual(report["status"], "fail")
        self.assertTrue(
            any(issue["code"] == "TEXT-FIT-ROLE-DEFAULT" for issue in report["issues"]),
            report["issues"],
        )


if __name__ == "__main__":
    unittest.main()
