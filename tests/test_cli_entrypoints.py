import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("PYTHONIOENCODING", None)
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


class CliEntrypointTests(unittest.TestCase):
    def test_project_manager_help_imports_shared_project_utils(self):
        result = run_cli("scripts/project_manager.py", "help")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("project_manager.py init", result.stdout)

    def test_thumbnail_help_imports_office_soffice_helper(self):
        result = run_cli("scripts/thumbnail.py", "--help")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Create thumbnail grids", result.stdout)

    def test_svg_quality_checker_help_is_printable_on_windows(self):
        result = run_cli("scripts/svg_quality_checker.py", "--help")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SVG Quality Check Tool", result.stdout)
        self.assertNotIn("Unable to import dependency modules", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
