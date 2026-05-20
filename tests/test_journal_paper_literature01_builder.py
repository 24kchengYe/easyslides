from __future__ import annotations

import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "projects" / "journal_paper" / "build_literature01_deck.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("journal_paper_builder", BUILDER_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_svg(svg: str) -> ET.Element:
    return ET.fromstring(svg)


def local_name(node: ET.Element) -> str:
    return node.tag.split("}")[-1]


def test_defaults_omit_logo_and_use_chuanbai_presenter():
    builder = load_builder()

    svgs = [
        builder.build_cover(),
        builder.build_toc(),
        builder.build_chapter("01", "论文主张", "Core thesis"),
        builder.build_ending(),
    ]

    for svg in svgs:
        assert "{{LOGO_IMAGE}}" not in svg
        assert "logo_mark.png" not in svg
        assert 'data-slot="LOGO_IMAGE"' not in svg

    assert 'id="cover-chrome"' in svgs[0]
    assert "汇报人：</tspan><tspan data-slot=\"AUTHOR\">川柏同学</tspan>" in svgs[0]
    assert "日期：</tspan><tspan data-slot=\"DATE\">2026-05-19</tspan>" in svgs[0]
    assert "单位：" not in svgs[0]
    assert "Trends in Ecology" not in svgs[0]
    assert "{{TITLE}}" not in svgs[0]
    assert "{{SUBTITLE}}" not in svgs[0]
    assert "{{AUTHOR}}" not in svgs[0]
    assert "{{INSTITUTION}}" not in svgs[0]
    assert "{{DATE}}" not in svgs[0]
    cover_root = parse_svg(svgs[0])
    cover_meta = next(node for node in cover_root.iter() if node.attrib.get("id") == "cover-meta")
    assert not any(local_name(node) == "rect" for node in list(cover_meta))
    meta_texts = [node for node in list(cover_meta) if local_name(node) == "text"]
    assert len(meta_texts) == 2
    for meta_text in meta_texts:
        assert meta_text.attrib["x"] == "640"
        assert meta_text.attrib["text-anchor"] == "middle"
        assert meta_text.attrib["font-size"] == "18"
        assert meta_text.attrib["fill"] == "#000000"
    assert "汇报人：</tspan><tspan data-slot=\"AUTHOR\">川柏同学</tspan>" in svgs[-1]
    assert "敬请批评指正！" in svgs[-1]
    assert "谢谢聆听" not in svgs[-1]
    assert "Thank you for listening!" in svgs[-1]


def test_slide_05_figure_frame_caption_describes_content_not_source_name():
    builder = load_builder()
    root = parse_svg(builder.slide_05())
    vibroscape = next(node for node in root.iter() if node.attrib.get("id") == "vibroscape")
    texts = ["".join(node.itertext()) for node in vibroscape.iter() if local_name(node) == "text"]

    assert not any("Figure 1" in text for text in texts)
    assert any("取食者" in text and "背景振动" in text for text in texts)


def test_rounded_frame_text_boxes_are_bounded_by_their_frame():
    builder = load_builder()

    for slide in [builder.slide_05(), builder.slide_07(), builder.slide_09(), builder.slide_11()]:
        root = parse_svg(slide)
        for group in root.iter():
            if local_name(group) != "g":
                continue
            rects = [
                node
                for node in list(group)
                if local_name(node) == "rect" and (node.attrib.get("rx") or node.attrib.get("ry"))
            ]
            if not rects:
                continue
            frame = rects[0]
            x = float(frame.attrib["x"])
            y = float(frame.attrib["y"])
            w = float(frame.attrib["width"])
            h = float(frame.attrib["height"])
            for text in group.iter():
                if local_name(text) != "text" or text.attrib.get("data-pptx-textbox") != "true":
                    continue
                attrs = text.attrib
                for key in ["data-pptx-box-x", "data-pptx-box-y", "data-pptx-box-w", "data-pptx-box-h"]:
                    assert key in attrs, f"{group.attrib.get('id')} missing {key}"
                tx = float(attrs["data-pptx-box-x"])
                ty = float(attrs["data-pptx-box-y"])
                tw = float(attrs["data-pptx-box-w"])
                th = float(attrs["data-pptx-box-h"])
                assert x <= tx <= x + w, group.attrib.get("id")
                assert y <= ty <= y + h, group.attrib.get("id")
                assert tx + tw <= x + w, group.attrib.get("id")
                assert ty + th <= y + h, group.attrib.get("id")
