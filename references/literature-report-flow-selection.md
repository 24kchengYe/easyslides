# Literature Report Flow Selection

Use this reference for single-paper literature reports before drafting
`deck_plan.json`, `design_spec.md`, or `spec_lock.md`.

## Core Rule

用户提供大纲或讲稿时，用户结构是主线；不得启用自动长文献汇报流程来替换它。

Treat these as user-provided structure:

- page-by-page outline, slide roster, or chapter order;
- speaking script, learning notes, or rehearsal notes;
- files such as `outline.docx`, `outline.md`, `script.txt`, `speaker_notes.md`;
- direct instructions like "按我的讲稿", "按这个大纲", or "每页照这个顺序讲".

When such structure exists, parse it first, preserve its order, and use the
paper/SI to verify claims, locate figures, calibrate wording, and fill evidence
gaps. Do not replace it with an agent-derived 20+ page literature report unless
the user explicitly asks for a rebuild.

## Flow Options

| Flow id | Inspired by | Use when | Default length | Main artifacts |
|---|---|---|---:|---|
| `paper_ppt_concise` | `xiao634zhang/paper-ppt-skill` | The user provides an outline/script, asks for a short group-meeting/course report, or wants a concise figure-first deck. | 6-10 slides | `deck_plan.json`, `source_map`, figure crops, template style notes |
| `literature_report_deep_dive` | `fangyuanopus/literature-report-ppt-builder` | No outline/script is provided and the user asks for a complete literature report, main paper + SI synthesis, maximum quality, or 20+ pages. | 20+ slides | `paper_logic_tree`, `terminology_table`, `main_si_crosswalk`, `figure_source_manifest`, `adaptive_navigation_plan`, `deck_order_map`, `page_briefs`, `speaker_notes` |

## Selection Procedure

1. Detect whether the user supplied an outline or script.
2. If yes, choose `paper_ppt_concise` unless the user explicitly requests a
   long-form rebuild. Preserve user page order and speaking logic.
3. If no, present or internally select between the two flow options:
   - concise / quick / group meeting / course presentation -> `paper_ppt_concise`;
   - complete / maximum quality / main paper plus SI / 20+ pages ->
     `literature_report_deep_dive`.
4. For ambiguous requests without outline/script, recommend the concise option
   for ordinary group meetings and the deep-dive option for formal literature
   reports; record the chosen `flow_id` in `deck_plan.json` metadata when
   available.
5. Both options must keep EasySlides' editable SVG/shape-IR -> DrawingML backend
   as the production path. Do not switch to image-only PPT assembly just because
   an inspiration skill used image2 or python-pptx.

## Non-Override Guardrails

- A user outline/script outranks any default story spine.
- A user reference template controls visual style where compatible with source
  traceability and text fit.
- Scientific figures, tables, charts, mechanisms, spectra, microscopy, and data
  must come from the paper, SI, or user-provided sources.
- `literature_report_deep_dive` is a planning flow, not permission to invent
  extra claims or figures.
- `deck_order_map` is required for long-form deck assembly; never assemble long
  decks in generation order.
- `page_briefs` are required before generating a deep-dive long-form deck.
- `figure_source_manifest` is required whenever scientific visuals are used.
