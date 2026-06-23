# -*- coding: utf-8 -*-
"""
Minimal DATA-figure example: real numbers -> matplotlib -> publication PNG/PDF,
using the talk/projector theme (figstyle). Run from the figures/ dir:

    python examples/example_bar.py

Demonstrates the house rules:
- shared style (figstyle.apply_rc) -> one place controls font/colour/linewidth
- colourblind-safe palette (figstyle.C_BLUE / C_ORANGE / C_GREEN / C_RED)
- title ABOVE the axes (never on data), 300 dpi tight export
- every number here is illustrative; in real use, load from a results file so the
  figure is source-traceable (do NOT hand-type numbers you cannot point back to).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import figstyle as FS

FS.apply_rc()

# illustrative data (replace with values loaded from your results file)
theories = ["Scaling", "Decay", "Vitality", "Perception"]
probe_r2 = [0.71, 0.46, 0.88, 0.29]          # memory-layer probe R^2
colors = [FS.C_BLUE, FS.C_ORANGE, FS.C_GREEN, FS.C_RED]

fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(theories, probe_r2, color=colors, width=0.62)
ax.set_ylabel("Probe $R^2$ (memory layer)", fontsize=FS.FS_AXIS)
ax.set_ylim(0, 1)
for i, v in enumerate(probe_r2):
    ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom",
            fontsize=FS.FS_DATALAB)
# title ABOVE the axes (Nature style), not on the data
ax.set_title("Each theory is encoded inside the model",
             loc="left", weight="bold", fontsize=FS.FS_PANEL, pad=12)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "example_bar.png")
FS.savefig(fig, out)   # 300 dpi, tight bbox
print("wrote", out)
