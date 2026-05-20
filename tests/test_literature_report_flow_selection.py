import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LiteratureReportFlowSelectionTests(unittest.TestCase):
    def test_single_paper_profile_declares_outline_first_flow_options(self):
        from scripts.scenario_profiles import get_profile, load_profiles, validate_profiles

        catalog = load_profiles()
        validate_profiles(catalog)
        profile = get_profile("single_paper_report", catalog)

        self.assertEqual(
            profile["input_priority"]["outline_or_script"],
            "user_structure_first",
        )
        self.assertEqual(
            profile["input_priority"]["no_outline_or_script"],
            "offer_concise_or_deep_literature_report",
        )

        options = {item["id"]: item for item in profile["flow_options"]}
        self.assertEqual(
            set(options),
            {"paper_ppt_concise", "literature_report_deep_dive"},
        )
        self.assertEqual(options["paper_ppt_concise"]["slide_count"], {"min": 6, "max": 10})
        self.assertEqual(options["literature_report_deep_dive"]["slide_count"]["min"], 20)
        self.assertIn("outline_or_script_provided", options["paper_ppt_concise"]["use_when"])
        self.assertIn("no_outline_or_script", options["literature_report_deep_dive"]["use_when"])

    def test_flow_selection_reference_records_non_override_rule(self):
        text = (ROOT / "references" / "literature-report-flow-selection.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("用户提供大纲或讲稿", text)
        self.assertIn("不得启用自动长文献汇报流程", text)
        self.assertIn("paper_ppt_concise", text)
        self.assertIn("literature_report_deep_dive", text)
        self.assertIn("deck_order_map", text)
        self.assertIn("page_briefs", text)
        self.assertIn("figure_source_manifest", text)

    def test_entry_docs_point_to_flow_selection_reference(self):
        docs = [
            ROOT / "SKILL.md",
            ROOT / "references" / "workflow-create.md",
            ROOT / "references" / "strategist.md",
        ]

        for path in docs:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("literature-report-flow-selection.md", text)
                self.assertIn("paper_ppt_concise", text)
                self.assertIn("literature_report_deep_dive", text)


if __name__ == "__main__":
    unittest.main()
