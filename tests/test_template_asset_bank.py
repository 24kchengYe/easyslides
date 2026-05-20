import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class TemplateAssetBankTests(unittest.TestCase):
    def _write_import_workspace(self, root: Path, *, include_flat_svg: bool = True) -> Path:
        workspace = root / "premium_template_import"
        (workspace / "svg").mkdir(parents=True)
        (workspace / "svg-flat").mkdir(parents=True)
        (workspace / "assets").mkdir(parents=True)

        (workspace / "svg" / "slide_01.svg").write_text(
            '<svg viewBox="0 0 1280 720"><text>Quarterly Review</text></svg>',
            encoding="utf-8",
        )
        if include_flat_svg:
            (workspace / "svg-flat" / "slide_01.svg").write_text(
                '<svg viewBox="0 0 1280 720"><text>Quarterly Review</text></svg>',
                encoding="utf-8",
            )
        (workspace / "assets" / "hero.png").write_bytes(b"fake")

        manifest = {
            "source": {
                "pptx": "C:/templates/premium.pptx",
                "name": "premium.pptx",
            },
            "slideSize": {"widthPx": 1280, "heightPx": 720},
            "theme": {
                "colors": {"accent1": "#0055AA"},
                "fonts": {"latin": "Aptos"},
            },
            "assets": {
                "exportDir": "assets",
                "allAssets": ["hero.png"],
                "commonAssets": ["hero.png"],
            },
            "pageTypeCandidates": {"cover": [1]},
            "layouts": [
                {
                    "path": "ppt/slideLayouts/slideLayout1.xml",
                    "name": "slideLayout1.xml",
                    "svgFile": "layout_01_slideLayout1.svg",
                    "usedBySlides": [1],
                    "placeholders": [
                        {
                            "type": "title",
                            "idx": "1",
                            "geometry": {"x": 100, "y": 60, "width": 760, "height": 80},
                            "textStyle": {"fontSizePx": 36, "bold": True},
                        },
                        {
                            "type": "pic",
                            "idx": "2",
                            "geometry": {"x": 760, "y": 120, "width": 380, "height": 280},
                        },
                    ],
                }
            ],
            "masters": [
                {
                    "path": "ppt/slideMasters/slideMaster1.xml",
                    "name": "slideMaster1.xml",
                    "svgFile": "master_01_slideMaster1.svg",
                    "usedBySlides": [1],
                    "placeholders": [
                        {
                            "type": "sldNum",
                            "idx": "12",
                            "geometry": {"x": 1160, "y": 680, "width": 60, "height": 24},
                        }
                    ],
                }
            ],
            "slides": [
                {
                    "index": 1,
                    "name": "slide1.xml",
                    "svgFile": "slide_01.svg",
                    "flatSvgFile": "slide_01.svg",
                    "slidePath": "ppt/slides/slide1.xml",
                    "layoutPath": "ppt/slideLayouts/slideLayout1.xml",
                    "masterPath": "ppt/slideMasters/slideMaster1.xml",
                    "backgroundAsset": None,
                    "backgroundSource": None,
                    "imageAssets": ["hero.png"],
                    "textSamples": ["Quarterly Review", "FY2026"],
                    "textCount": 2,
                    "shapeCount": 14,
                    "pageType": "cover",
                }
            ],
        }
        (workspace / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return workspace

    def test_builds_exact_reuse_modules_from_import_workspace(self):
        from scripts.template_asset_bank import build_asset_bank_from_workspaces

        with tempfile.TemporaryDirectory() as tmp:
            workspace = self._write_import_workspace(Path(tmp))

            bank = build_asset_bank_from_workspaces([workspace])

        self.assertEqual(bank["schema_version"], "easyslides.template_asset_bank.v1")
        self.assertEqual(bank["harness"]["primary_mode"], "exact_template_reuse")
        template = bank["templates"][0]
        self.assertEqual(template["template_id"], "premium")
        self.assertEqual(template["source_pptx"], "C:/templates/premium.pptx")
        page = template["pages"][0]
        self.assertEqual(page["module_id"], "premium/001_cover")
        self.assertEqual(page["page_type"], "cover")
        self.assertEqual(page["source"]["flat_svg"], "svg-flat/slide_01.svg")
        self.assertEqual(page["source"]["layered_svg"], "svg/slide_01.svg")
        self.assertEqual(page["reuse_contract"]["mode"], "exact_template_reuse")
        self.assertIn("replace text in existing text elements", page["reuse_contract"]["allowed_edits"])
        self.assertIn("move, resize, recolor, or delete fixed geometry", page["reuse_contract"]["forbidden_edits"])
        self.assertEqual(
            [slot["slot_id"] for slot in page["slots"]],
            ["title_1", "pic_2", "sldNum_12"],
        )
        self.assertEqual(page["slots"][0]["kind"], "text")
        self.assertEqual(page["slots"][1]["kind"], "image")

    def test_rejects_import_workspace_missing_flat_svg(self):
        from scripts.template_asset_bank import TemplateAssetBankError, build_asset_bank_from_workspaces

        with tempfile.TemporaryDirectory() as tmp:
            workspace = self._write_import_workspace(Path(tmp), include_flat_svg=False)

            with self.assertRaisesRegex(TemplateAssetBankError, "missing flat SVG"):
                build_asset_bank_from_workspaces([workspace])

    def test_non_ascii_pptx_name_falls_back_to_workspace_slug(self):
        from scripts.template_asset_bank import build_asset_bank_from_workspaces

        with tempfile.TemporaryDirectory() as tmp:
            workspace = self._write_import_workspace(Path(tmp) / "imports")
            manifest_path = workspace / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["source"]["name"] = "毕业答辩-酒红左侧导航栏.pptx"
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            stable_workspace = workspace.parent / "l001_left_nav"
            workspace.rename(stable_workspace)

            bank = build_asset_bank_from_workspaces([stable_workspace])

        self.assertEqual(bank["templates"][0]["template_id"], "l001_left_nav")
        self.assertEqual(
            bank["templates"][0]["pages"][0]["module_id"],
            "l001_left_nav/001_cover",
        )


if __name__ == "__main__":
    unittest.main()
