import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeAcknowledgementsTests(unittest.TestCase):
    def test_acknowledgements_are_layered_project_lists(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")

        for heading in [
            "工程底座",
            "学术表达",
            "叙事编排",
            "风格与模板治理",
            "论文与文献报告流程",
            "Engineering foundation",
            "Academic communication",
            "Narrative orchestration",
            "Style and template governance",
            "Paper and literature report workflows",
        ]:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

        self.assertIn("LearnPrompt/humanize-ppt", text)
        self.assertIn("Audience-State-Transfer", text)
        self.assertIn("观众状态转移", text)


if __name__ == "__main__":
    unittest.main()
