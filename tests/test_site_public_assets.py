import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SitePublicAssetsTests(unittest.TestCase):
    def test_public_asset_urls_are_ascii_and_exist(self):
        site = ROOT / "site"
        checked = []

        index_text = (site / "index.html").read_text(encoding="utf-8")
        for match in re.findall(r"assets/[^\s\"'`)<>]+", index_text):
            checked.append(match)
            with self.subTest(path="index.html", asset=match):
                self.assertTrue(match.isascii())
                self.assertTrue((site / match).exists())

        readme_text = (site / "assets" / "slides" / "README.md").read_text(
            encoding="utf-8"
        )
        for match in re.findall(r"assets/[^\s\"'`)<>]+", readme_text):
            checked.append(match)
            with self.subTest(path="README.md", asset=match):
                self.assertTrue(match.isascii())

        self.assertTrue(checked)

    def test_scene_assets_have_webp_variants(self):
        site = ROOT / "site"

        for png in [
            site / "assets" / "seminar-hall.png",
            site / "assets" / "classroom.png",
            site / "assets" / "meeting-room.png",
            site / "assets" / "scenes-16x9" / "seminar-hall.png",
            site / "assets" / "scenes-16x9" / "classroom.png",
            site / "assets" / "scenes-16x9" / "meeting-room.png",
        ]:
            with self.subTest(asset=png.relative_to(site)):
                self.assertTrue(png.with_suffix(".webp").exists())

    def test_home_hero_preloads_webp_background(self):
        text = (ROOT / "site" / "index.html").read_text(encoding="utf-8")

        self.assertIn('rel="preload"', text)
        self.assertIn('href="assets/seminar-hall.webp"', text)
        self.assertIn('type="image/webp"', text)
        self.assertIn("image-set(", text)


if __name__ == "__main__":
    unittest.main()
