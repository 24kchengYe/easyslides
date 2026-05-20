import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HtmlJsxArchitectureDocsTests(unittest.TestCase):
    def test_skill_declares_single_backend_with_html_jsx_upstream(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("## Backend-Centered Architecture", skill)
        self.assertIn("one production backend", skill)
        self.assertIn("### Path C: HTML/JSX Authoring", skill)
        self.assertIn("normalized SVG or shape IR", skill)
        self.assertIn("not main-path dependencies", skill)

    def test_html_jsx_workflow_locks_experimental_boundary(self):
        workflow_path = ROOT / "workflows" / "html-jsx-authoring.md"
        self.assertTrue(workflow_path.exists(), "Path C workflow is required")

        workflow = workflow_path.read_text(encoding="utf-8")
        self.assertIn("html_jsx_upstream_to_easyslides_backend", workflow)
        self.assertIn("one production backend", workflow)
        self.assertIn("experiments/pptxgenjs-jsx-spike", workflow)
        self.assertIn("@artifact-kit/pptxgenjs-jsx", workflow)
        self.assertIn("svg_quality_checker.py", workflow)
        self.assertIn("svg_to_pptx.py", workflow)
        self.assertIn("must not", workflow)
        self.assertIn("add `@artifact-kit/pptxgenjs-jsx`", workflow)

    def test_html_jsx_workflow_absorbs_measure_first_lessons(self):
        workflow = (ROOT / "workflows" / "html-jsx-authoring.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## Lessons To Absorb From artifact-kit/html-to-pptx-skill", workflow)
        self.assertIn("copy-first exporter hygiene", workflow)
        self.assertIn("measurement manifest", workflow)
        self.assertIn("coordinate provenance", workflow)
        self.assertIn("native reconstruction inventory", workflow)
        self.assertIn("audit gate", workflow)
        self.assertIn("source HTML must stay clean", workflow)


if __name__ == "__main__":
    unittest.main()
