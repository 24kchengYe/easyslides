# -*- coding: utf-8 -*-
"""
Trim the legibility section to a single honest-footnote page (keep P17), per user
decision "几乎删光，只留1页点到".

Current order (29 pages):
  ... P15 frontier(keep), P16 method(drop), P17 spectrum(KEEP->becomes P16),
  P18 key-attrs(drop), P19 human-gold(drop), P20 fly-lower(drop),
  P21 confidence(drop), P22 more-views-worse(drop), P23 chapter dataset ...

We MOVE the 6 dropped SVGs to _removed_legibility/ (not hard-delete -> reversible),
then renumber the remaining pages contiguously and fix footers 'N / 29' -> 'N / 23'.
Result: 23 pages.
"""
import os, glob, re, shutil

SVG = 'svg_output'
GRAVE = '_removed_legibility'
os.makedirs(GRAVE, exist_ok=True)

DROP = [16, 18, 19, 20, 21, 22]  # page numbers to remove (P17 kept)

# 1) move dropped pages out
for n in DROP:
    p = os.path.join(SVG, 'page_%02d.svg' % n)
    if os.path.exists(p):
        shutil.move(p, os.path.join(GRAVE, 'page_%02d.svg' % n))
        print('moved out:', p)

# 2) collect remaining, sort by old number, renumber 1..K
remaining = sorted(glob.glob(os.path.join(SVG, 'page_*.svg')),
                   key=lambda x: int(re.search(r'(\d+)', os.path.basename(x)).group(1)))
total = len(remaining)
print('remaining pages:', total)

# rename to temp first to avoid collisions
tmpmap = []
for i, p in enumerate(remaining, start=1):
    tmp = os.path.join(SVG, 'tmp_%02d.svg' % i)
    os.rename(p, tmp)
    tmpmap.append((i, tmp))

# 3) finalize names + fix per-page footer 'X / NN' and total
for i, tmp in tmpmap:
    final = os.path.join(SVG, 'page_%02d.svg' % i)
    os.rename(tmp, final)
    s = open(final, encoding='utf-8').read()
    s = re.sub(r'>\s*\d+\s*/\s*\d+\s*<', '>%d / %d<' % (i, total), s)
    open(final, 'w', encoding='utf-8').write(s)

print('done. final pages:', total)
for p in sorted(glob.glob(os.path.join(SVG, 'page_*.svg'))):
    print(' ', os.path.basename(p))
