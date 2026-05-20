import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SourceMaterialPolicyDocsTests(unittest.TestCase):
    def test_main_skill_declares_material_mode_policy(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Source Material Policy", text)
        self.assertIn("No supplied source materials", text)
        self.assertIn("Provided mature source materials", text)
        self.assertIn("Do not replace extracted figures", text)

    def test_topic_research_allows_web_images_only_without_user_materials(self):
        text = (ROOT / "workflows" / "topic-research.md").read_text(encoding="utf-8")

        self.assertIn("only when the user supplies no source materials", text)
        self.assertIn("download relevant openly licensed images", text)
        self.assertIn("If source materials are provided", text)

    def test_create_workflow_points_to_the_policy_before_research(self):
        text = (ROOT / "references" / "workflow-create.md").read_text(encoding="utf-8")

        self.assertIn("Source Material Policy", text)
        self.assertIn("topic-research workflow to gather web text and images", text)


if __name__ == "__main__":
    unittest.main()
