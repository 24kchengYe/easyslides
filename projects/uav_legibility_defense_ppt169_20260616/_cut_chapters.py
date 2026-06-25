# -*- coding: utf-8 -*-
"""Cut 3 redundant chapter-divider pages (P06 data, P09 framework, P20 conclusion)
per user decision. Keep P03 (background), P14 (core finding, soul chapter),
P17 (dataset). Move cut pages to _removed_chapters/ (reversible), renumber
remaining 23 -> 20 contiguously, fix per-page 'N / NN' footers."""
import os, glob, re, shutil

SVG = 'svg_output'
GRAVE = '_removed_chapters'
os.makedirs(GRAVE, exist_ok=True)

DROP = [6, 9, 20]  # chapter dividers: 二/数据, 三/框架, 六/结论

for n in DROP:
    p = os.path.join(SVG, 'page_%02d.svg' % n)
    if os.path.exists(p):
        shutil.move(p, os.path.join(GRAVE, 'page_%02d.svg' % n))
        print('moved out:', p)

remaining = sorted(glob.glob(os.path.join(SVG, 'page_*.svg')),
                   key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group(1)))
total = len(remaining)
# rename via temp to avoid collisions
tmp = []
for i, p in enumerate(remaining, start=1):
    t = os.path.join(SVG, 'tmp_%02d.svg' % i)
    os.rename(p, t)
    tmp.append((i, t))
for i, t in tmp:
    final = os.path.join(SVG, 'page_%02d.svg' % i)
    os.rename(t, final)
    s = open(final, encoding='utf-8').read()
    s = re.sub(r'>\s*\d+\s*/\s*\d+\s*<', '>%d / %d<' % (i, total), s)
    open(final, 'w', encoding='utf-8').write(s)

print('final pages:', total)
