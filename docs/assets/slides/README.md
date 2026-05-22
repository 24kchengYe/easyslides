Put exported PPT page images here when the real decks are ready.

Recommended structure:

```text
assets/slides/work-01/slide-01.png
assets/slides/work-01/slide-02.png
assets/slides/work-02/slide-01.png
```

Current real deck:

```text
assets/slides/work-01/slide-01.jpg
assets/slides/work-01/slide-02.jpg
...
assets/slides/work-01/slide-14.jpg
```

Then register those paths in `slideAssets` inside `index.html`. The detail page will place the selected image exactly inside the photo screen area and use the current mock slide only as a fallback.

Scene photo screen regions are defined as CSS percentages in `index.html`:

```text
seminar   assets/scenes-16x9/报告厅.png   x 24.04%, y 17.95%, w 52.16%, h 47.86%
classroom assets/scenes-16x9/教室.png     x 22.24%, y 18.59%, w 54.57%, h 49.57%
meeting   assets/scenes-16x9/会议室.png   x 24.04%, y 17.73%, w 52.04%, h 47.86%
display   assets/scenes-16x9/会议室2.png  x 23.43%, y 22.44%, w 53.00%, h 52.99%
```

The `assets/scenes-16x9` images are center-cropped from the originals to `1664x936`, a strict 16:9 ratio.
