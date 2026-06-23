# -*- coding: utf-8 -*-
"""
Shared figure style for the AI4US rebuttal figures.

Golden standard = the author's own manuscript-figure code
(_original_code/01LLM_Zero-shot_code_naturecities/03AIUS-...图1.py):
  * big canvas (per-panel ~7x6.5 in),  Arial, axes.linewidth 1.5
  * large fonts: panel title 22-24, axis label 20, tick 18, stats box 16, legend 18
  * generous wspace/hspace so nothing overlaps; titles ABOVE the axes (never on data)

This module centralises those constants so every make_fig_*.py produces
projector-readable, collision-free figures at the same visual scale.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- colour palette (colourblind-safe, matches manuscript) ----
C_BLUE   = "#0072B2"   # text model / primary
C_ORANGE = "#D55E00"   # VL model (vermillion)
C_RED    = "#D62728"   # mean / trend line
C_GREEN  = "#009E73"   # causal effect
C_GREY   = "#999999"   # null / control
C_LBLUE  = "#56B4E9"   # secondary blue (fictional)
C_BAND   = "#1f77b4"   # CI band
DIVERGE  = "RdBu_r"

# ---- font sizes (projector-readable; ~2x the old 8-12pt) ----
FS_SUPTITLE = 23   # figure caption / take-home
FS_PANEL    = 21   # a/b/c panel title (above axes)
FS_AXIS     = 19   # axis labels
FS_TICK     = 17   # tick labels
FS_STATS    = 15   # in-plot stats / annotations
FS_LEGEND   = 16   # legend
FS_DATALAB  = 15   # value labels on bars/points
FS_SMALL    = 13   # secondary side-notes

LW_AX   = 1.5
LW_LINE = 2.6
LW_REF  = 2.4


def apply_rc():
    """Global rcParams matching the author's manuscript figures."""
    plt.rcParams.update({
        "font.family": "Arial",
        "font.size": FS_TICK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": LW_AX,
        "axes.titlesize": FS_PANEL,
        "axes.labelsize": FS_AXIS,
        "xtick.labelsize": FS_TICK,
        "ytick.labelsize": FS_TICK,
        "xtick.major.width": LW_AX,
        "ytick.major.width": LW_AX,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.fontsize": FS_LEGEND,
        "figure.dpi": 150,
    })


def panel_title(ax, letter, text, pad=14):
    """
    Nature-style panel title placed ABOVE the axes (never on the data or the
    y-axis label). Bold letter + descriptive sentence, left-aligned.
    """
    ax.set_title(f"{letter}  {text}", loc="left", weight="bold",
                 fontsize=FS_PANEL, pad=pad)


def savefig(fig, path):
    fig.savefig(path, dpi=300, bbox_inches="tight")
    print("SAVED", path)
