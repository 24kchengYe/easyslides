# -*- coding: utf-8 -*-
"""Rebuild deck to ~11-page storytelling version per approved outline.
Select best existing pages, drop chapter dividers + technical/detail pages +
the (now removed) data-availability page. Move originals to _removed_v20/.
"""
import os, glob, re, shutil

SVG = 'svg_output'
GRAVE = '_removed_v20'
os.makedirs(GRAVE, exist_ok=True)

# new order -> source page number in current 20-page deck
# 1 cover, 2 problem, 3 hook, 4 data, 5 method-one-line,
# 6 core hard numbers, 7 positive-fill(fig4d), 8 honest(spectrum),
# 9 dataset, 10 workbench(for tool demo), 11 conclusion+ending
ORDER = [1, 4, 5, 6, 8, 13, 10, 14, 16, 11, 18]
# (P20 ending is dropped; conclusion P18 becomes the closer. Ending re-added later if wanted.)

# stage all current pages out to GRAVE first
cur = sorted(glob.glob(os.path.join(SVG, 'page_*.svg')),
             key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group(1)))
for p in cur:
    shutil.copy(p, os.path.join(GRAVE, os.path.basename(p)))

# build new sequence from GRAVE copies
for p in cur:
    os.remove(p)
total = len(ORDER)
for newn, src in enumerate(ORDER, start=1):
    srcpath = os.path.join(GRAVE, 'page_%02d.svg' % src)
    dst = os.path.join(SVG, 'page_%02d.svg' % newn)
    s = open(srcpath, encoding='utf-8').read()
    # fix footer page number 'X / NN' -> 'newn / total'
    s = re.sub(r'>\s*\d+\s*/\s*\d+\s*<', '>%d / %d<' % (newn, total), s)
    open(dst, 'w', encoding='utf-8').write(s)
    print(f'new P{newn:02d} <- old P{src:02d}')
print('total new pages:', total)
