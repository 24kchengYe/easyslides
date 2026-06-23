# figures/examples

Runnable examples for the three figure workflows.

| File | Workflow | Run |
|------|----------|-----|
| `example_bar.py` | DATA figure (numbers → matplotlib via `figstyle`) | `python examples/example_bar.py` → `example_bar.png` |

For the **concept-diagram** workflow (hand-authored SVG → native editable shapes),
see the ready-made templates in `../../templates/figures/svg_examples/` (probe_flow.svg,
memory_vs_causal_concept.svg, *_4theories.svg, sampling_paradigm.svg, blueprint.svg, …)
and inject them with:

```python
from pptx import Presentation
from figures.svg_inject import inject_svg_shapes
prs = Presentation(); prs.slide_width = ...; prs.slide_height = ...
slide = prs.slides.add_slide(prs.slide_layouts[6])
inject_svg_shapes(slide, "../../templates/figures/svg_examples/probe_flow.svg")  # native shapes
```

See `../../references/scientific-figures.md` for the decision tree and house rules.
