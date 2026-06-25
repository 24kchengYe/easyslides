# Surgical PPTX Editing & Data-Figure Field Notes

Hard-won lessons from editing a hand-tuned academic deck and generating its
data figures. Complements `Path B` (XML unpack/repack) and `scientific-figures.md`
(SVG-inject). This file is about the case the others don't cover: **a .pptx the
user has already hand-tuned in PowerPoint, where you must make small precise
changes without disturbing their layout.**

---

## 1. When the user has hand-tuned the deck, the .pptx IS the master

**Iron rule: never re-export the deck from SVG/source once the user has edited
it in PowerPoint.** Re-running the SVG→DrawingML pipeline regenerates every
slide and **clobbers** the user's manual moves (box positions, font sizes,
picture placement). This destroys hours of their work.

- Treat `*.pptx` the user touched as the single source of truth.
- Make changes **in place** with `python-pptx` at the run/shape level.
- The SVG sources become stale the moment the user edits the pptx. Don't sync
  back to them and don't re-export from them.

If you previously authored from SVG, that history is now reference-only.

## 2. Backup → edit-on-copy → render-verify → apply

Every edit session on a user deck:

1. **Restore point first.** Copy the current file to a timestamped name
   *before any edit*: `..._用户版备份_YYYYMMDD_HHMM.pptx`. This is the
   pre-edit snapshot to roll back to.
2. **Dry-run on a temp copy.** Apply the edit script to a `$TEMP` copy, render
   it (LibreOffice→PDF→PNG), and eyeball the changed slides.
3. **Only then apply to the working file.**
4. **Save a post-edit dated version** too (`..._XX版_YYYYMMDD_HHMM.pptx`) so the
   user has both the before and after as named restore points.
5. **Never touch the user's own backup** (e.g. `... - 副本.pptx`) — read-only, always.

Check for the lock file before writing — if `~$<name>.pptx` exists, PowerPoint
has it open; writing will corrupt/conflict. Abort and ask the user to close it.

## 3. The run-level edit that preserves formatting

A `TextBox` paragraph is split into multiple `runs`, each carrying its own font.
Setting `shape.text_frame.text = "..."` **nukes all run formatting**. To change
the words while keeping size/colour/bold, edit run[0] and blank the rest:

```python
def set_run0(sh, newtext):
    tf = sh.text_frame; para = tf.paragraphs[0]
    if para.runs:
        para.runs[0].text = newtext
        for r in para.runs[1:]:
            r.text = ""          # keep the run (and its rPr) but empty it
    else:
        tf.text = newtext
```

- A digit that's its own run (e.g. `['两级']['7']['标签']`) is usually a
  **deliberate emphasis** (different size/colour). Don't "fix" it — leave it.
- To match a shape, dump every shape's `name`, position (`Emu(sh.left).inches`),
  size, and per-run `(text, font.size.pt)` first. Match on `shape.name` +
  exact run text so you edit precisely the right element.

## 4. Editing a hand-drawn infographic (cards, progress bars)

Data "cards" / KPI tiles / progress bars are built from `AUTO_SHAPE` rectangles
+ textboxes, not a single image. To change a number you touch several elements:

- **Progress/percentage bars** are two stacked rectangles: a full-width track
  and a fill rect whose **width encodes the percent**. Recompute geometry, don't
  eyeball: `fill.width = int(track_width_emu * new_fraction)`. Verify the old
  fraction first (`fill_w / track_w`) to confirm which rect is which.
- Change **all** linked elements together: the headline count, the bar fraction,
  each sub-number, the percent labels, and any "约 1/5"-style prose. Miss one
  and the slide self-contradicts.

## 5. Swapping a picture in place (keep position/size)

```python
for sh in slide.shapes:
    if sh.name == "Picture 28" and sh.shape_type == 13:   # 13 = PICTURE
        L, T, W, H = sh.left, sh.top, sh.width, sh.height
        sh._element.getparent().remove(sh._element)        # drop old blob
        slide.shapes.add_picture(NEW_PNG, L, T, W, H)      # same geometry
        break
```

Reusing the exact `(L,T,W,H)` keeps the user's framing. Don't `add_picture`
without capturing geometry first — it lands at the origin at native size.

## 6. LibreOffice render-QA gotchas (Windows)

Rendering is for *your* verification, not a faithful preview:

- **CJK filename breaks `soffice --convert-to`** (mangled output name, "Couldn't
  open file"). **Copy the deck to an ASCII temp name first**
  (`$TEMP/_deck.pptx`), convert that, then render.
- **LibreOffice may render fewer pages than the deck has** (e.g. 18 slides → 16
  PDF pages) due to ghost-slide / blank-layout quirks. The .pptx is still valid
  (verify unique `sldId`s + parts). Don't "fix" the deck over a render artifact.
  Page numbers in the PDF will be offset from slide numbers — locate the slide
  by content, not by page index.
- **CJK text overlaps / wrong line-height in the render** even when it's fine in
  PowerPoint (font fallback differs). If you only changed numbers/pictures and
  didn't move textboxes, overlap in the render is **not your regression** — say
  so and move on. Confirm by diffing: you never touched those textboxes.
- Pipeline: `soffice --headless --convert-to pdf --outdir $TEMP _deck.pptx`
  then `pdftoppm -png -f P -l P -r 85 _deck.pdf out` for the page(s) you changed.

## 7. Data-figure pitfalls (matplotlib city/GIS maps)

When generating a whole-map data figure from model outputs:

- **Rectangular raster margins spawn phantom objects.** A segmentation TIF over
  a rectangular tile fires on nodata/seam borders, creating a regular *grid* of
  fake "buildings" at the edges. Crop to the real subject via a **density-grid
  largest-connected-component** footprint (bin centroids into cells, keep dense
  cells, take biggest 8-connected blob, fill holes) — not a convex hull (the
  hull gets inflated to the full raster by the phantoms).
- **"Lowest ratio" ≠ "cleanest figure."** Picking the example with the best
  headline metric can backfire if that instance is a large, messy city with more
  edge phantoms and more misclassification blobs. **Render the candidates and
  look** before choosing. A smaller, tighter city often shows better.
- **Drop categories that swamp the subject.** On a "demolition check" map, the
  phantom-inflated *constructed* class (blue) drowned the *demolished* signal
  (red). Removing the non-subject class — and saying so in the caption — made
  the figure read. Don't draw every class reflexively; draw what the page argues.
- **Legends/labels must survive a projector.** Bump legend/label font to ≥16–20pt
  for slides; tiny default legends are unreadable in a room.
- **Same-hue families encode hierarchy.** For a taxonomy with a parent class and
  sub-levels, use one hue in graded shades for the sub-levels (e.g. persistent =
  3 greens) and contrasting hues for the opposing classes — the structure is
  visible at a glance.

## 8. Number-caliber discipline (the expensive bug)

The slowest failure: **the same quantity computed by different pipelines gives
different numbers, and stale ones leak into figures/prose.** A demolition count
read 664 / 563 / 553 / 464 depending on which matching pipeline and whether the
map was cropped.

- **Before putting any number on a slide or in a paper, trace which script/
  pipeline produced it** and whether it's the *final production* output. Prefer
  the persisted product (e.g. the output shapefile's status field) over a figure
  script that re-runs an older code path.
- **One caliber across all deliverables.** PPT, paper body, paper table, and
  figure captions must cite the same pipeline's numbers. If a table is full-city
  and the prose is cropped-to-core, *say so explicitly* in both places.
- When a figure script *recomputes* (vs. reads the product), it can silently use
  a superseded algorithm. Rewrite it to **read the production output** instead.
- Record the canonical caliber + the provenance of each rival number in project
  memory so the confusion can't recur.

## 9. Formula & flowchart assets for this backend

(See also `scientific-figures.md`.) easyslides forbids `foreignObject`, has no
OMML math, so:

- **Formulas** → render LaTeX/mathtext to a **transparent PNG** (matplotlib
  `mathtext`, `dpi≈300`, `transparent=True`) and place as a small picture.
  These end up as thin wide picture strips (`Image NN`, e.g. 3"×0.4"); that's
  expected.
- **Flowcharts** → hand-authored SVG injected as native shapes (editable), or a
  rendered PNG if editability doesn't matter. Mermaid → PNG only; its
  markers/gradients/`foreignObject` don't survive the editable conversion.
