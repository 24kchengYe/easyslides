import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def load_builder():
    script = ROOT / "projects" / "degree_thesis" / "defense01_deck" / "build_deck.py"
    spec = importlib.util.spec_from_file_location("degree_thesis_defense_topnav_builder", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load builder: {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DegreeThesisDefenseTopnavBuilderTests(unittest.TestCase):
    def test_content_shell_applies_defense_topnav_top_navigation_state_from_template(self):
        builder = load_builder()
        nav = json.loads((ROOT / "templates" / "layouts" / "defense_topnav" / "navigation_states.json").read_text(encoding="utf-8"))
        section = builder.SECTIONS[3]
        expected = nav["sections"][3]

        root, _ = builder.content_shell(
            {
                "slide": 18,
                "title": "结果与分析",
                "section": section,
                "summary": "用于测试导航状态。",
            }
        )

        def by_id(element_id):
            return next(node for node in root.iter() if node.attrib.get("id") == element_id)

        active_tab = by_id("nav-active-tab")
        self.assertEqual(active_tab.attrib["data-active-index"], "4")
        self.assertEqual(active_tab.attrib["data-active-section"], section)
        self.assertEqual(active_tab.attrib["x"], str(expected["active_tab"]["x"]))
        self.assertEqual(active_tab.attrib["width"], str(expected["active_tab"]["width"]))
        self.assertEqual(active_tab.attrib["fill"], "#FFFFFF")

        active_label = by_id("nav-active-label")
        self.assertEqual(active_label.attrib["x"], str(expected["label"]["x"]))
        self.assertEqual(active_label.attrib["y"], str(expected["label"]["title_y"]))
        self.assertEqual(active_label.attrib["text-anchor"], "middle")
        self.assertEqual(active_label.attrib["fill"], "#183A6A")
        self.assertEqual("".join(active_label.itertext()).strip(), section)

        inactive_labels = [
            node
            for node in root.iter()
            if node.tag.split("}")[-1] == "text" and node.attrib.get("id", "").startswith("nav-label-")
        ]
        self.assertEqual(len(inactive_labels), 5)
        self.assertEqual(
            ["".join(node.itertext()).strip() for node in inactive_labels],
            [item for item in builder.NAV_SECTIONS if item != section],
        )
        self.assertTrue(all(node.attrib["fill"] == "#FFFFFF" for node in inactive_labels))

        page_title = next(node for node in root.iter() if node.attrib.get("data-slot") == "PAGE_TITLE")
        self.assertEqual(page_title.attrib["data-pptx-box-x"], "48.51")
        self.assertEqual(page_title.attrib["data-pptx-box-y"], "128.42")
        self.assertEqual(page_title.attrib["data-pptx-box-w"], "197.11")
        self.assertEqual(page_title.attrib["data-pptx-box-h"], "48.47")
        self.assertEqual(page_title.attrib["data-pptx-valign"], "middle")
        self.assertEqual(page_title.attrib["dominant-baseline"], "middle")
        page_title_text = "".join(page_title.itertext()).strip()

        key_message = next(node for node in root.iter() if node.attrib.get("data-slot") == "KEY_MESSAGE")
        self.assertEqual(key_message.attrib["data-pptx-box-x"], "288")
        self.assertEqual(key_message.attrib["data-pptx-box-y"], "132.37")
        self.assertEqual(key_message.attrib["data-pptx-box-w"], "898")
        self.assertEqual(key_message.attrib["data-pptx-box-h"], "40.57")
        self.assertEqual(key_message.attrib["data-pptx-valign"], "middle")
        self.assertEqual(key_message.attrib["dominant-baseline"], "middle")
        self.assertAlmostEqual(float(page_title.attrib["y"]), float(key_message.attrib["y"]), places=1)
        key_message_text = "".join(key_message.itertext()).strip()
        self.assertNotEqual(key_message_text, page_title_text.replace("◆", "").strip())
        self.assertGreater(len(key_message_text), len(page_title_text.replace("◆", "").strip()))

        content_area = next(node for node in root.iter() if node.attrib.get("id") == "content-area")
        self.assertEqual(content_area.attrib["fill"], "none")
        self.assertEqual(content_area.attrib["stroke"], "none")
        self.assertNotIn("stroke-dasharray", content_area.attrib)
        self.assertLessEqual(float(content_area.attrib["x"]), 56)
        self.assertLessEqual(float(content_area.attrib["y"]), 190)
        self.assertGreaterEqual(float(content_area.attrib["width"]), 1170)
        self.assertGreaterEqual(float(content_area.attrib["height"]), 480)

        self.assertFalse(any(node.attrib.get("data-slot") == "FOOTER_KEYWORD" for node in root.iter()))
        self.assertFalse(any(node.attrib.get("data-slot") == "FOOTER_SUMMARY" for node in root.iter()))

    def test_write_svg_does_not_insert_preserved_whitespace_into_nav_text(self):
        builder = load_builder()
        root, _ = builder.content_shell(
            {
                "slide": 4,
                "title": "研究背景",
                "section": builder.SECTIONS[0],
                "summary": "用于测试导航文字空白。",
            }
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slide.svg"
            builder.write_svg(path, root)
            written = ET.parse(path).getroot()

        nav_texts = [
            node
            for node in written.iter()
            if node.tag.split("}")[-1] == "text"
            and (node.attrib.get("id") == "nav-active-label" or node.attrib.get("id", "").startswith("nav-label-"))
        ]
        for node in nav_texts:
            self.assertEqual((node.text or "").strip(), "".join(node.itertext()).strip())
            for child in list(node):
                self.assertIn(child.tail, (None, ""))

    def test_table_image_slide_places_table_name_above_image(self):
        builder = load_builder()
        cfg = next(slide for slide in builder.SLIDES if slide["slide"] == 26)
        root = builder.build_content_slide(cfg)

        table_name = next(
            node
            for node in root.iter()
            if node.tag.split("}")[-1] == "text" and "表一 导生关系内涵及本质" in "".join(node.itertext())
        )
        image = next(node for node in root.iter() if node.tag.split("}")[-1] == "image")

        self.assertLess(float(table_name.attrib["y"]), float(image.attrib["y"]))
        self.assertEqual(table_name.attrib["text-anchor"], "middle")
        self.assertEqual(table_name.attrib["fill"], builder.PRIMARY)

    def test_references_page_title_says_primary_references(self):
        builder = load_builder()
        root = builder.build_references(28)
        page_title = next(node for node in root.iter() if node.attrib.get("data-slot") == "PAGE_TITLE")
        refs_cfg = next(slide for slide in builder.SLIDES if slide["archetype"] == "references")

        self.assertEqual("".join(page_title.itertext()).strip(), "◆ 主要参考文献")
        self.assertEqual(builder.title_for_slide(refs_cfg), "主要参考文献")

    def test_timeline_sequence_connects_actual_nodes_for_variable_counts(self):
        builder = load_builder()

        for count in (3, 6):
            with self.subTest(count=count):
                cfg = {
                    "slide": 55 + count,
                    "title": f"测试时间线 {count}",
                    "section": builder.SECTIONS[0],
                    "kind": "timeline",
                    "summary": "用于测试时间线节点连线。",
                    "items": [
                        {"year": f"T{idx}", "title": f"节点{idx}", "body": "测试正文"}
                        for idx in range(1, count + 1)
                    ],
                }
                root = builder.build_content_slide(cfg)
                body = next(node for node in root.iter() if node.attrib.get("id") == f"content-body-{55 + count:02d}")
                circles = [
                    node
                    for node in list(body)
                    if node.tag.split("}")[-1] == "circle" and node.attrib.get("r") == "13"
                ]
                self.assertEqual(len(circles), count)

                connector = next(
                    node
                    for node in list(body)
                    if node.tag.split("}")[-1] == "line" and node.attrib.get("stroke") == builder.PRIMARY
                )
                circle_xs = [float(node.attrib["cx"]) for node in circles]
                circle_y = float(circles[0].attrib["cy"])

                self.assertEqual(float(connector.attrib["x1"]), circle_xs[0])
                self.assertEqual(float(connector.attrib["x2"]), circle_xs[-1])
                self.assertEqual(float(connector.attrib["y1"]), circle_y)
                self.assertEqual(float(connector.attrib["y2"]), circle_y)
                self.assertEqual(circle_xs, sorted(circle_xs))

                gaps = [round(b - a, 2) for a, b in zip(circle_xs, circle_xs[1:])]
                self.assertEqual(len(set(gaps)), 1)


if __name__ == "__main__":
    unittest.main()
