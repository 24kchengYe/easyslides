# -*- coding: utf-8 -*-
"""Resync deck_plan.json to the trimmed 23-page SVG set.

Removed SVG pages were old P16,P18,P19,P20,P21,P22 (legibility deep-dive).
In the 29-page deck these are slides at index 15,17,18,19,20,21 (0-based).
After removing, renumber P01..P23 and refresh a few action_titles to match the
edited SVGs (TOC, kept second-gate page, conclusion)."""
import json

d = json.load(open('deck_plan.json', encoding='utf-8'))
sl = d['slides']

# the 6 removed pages by their CURRENT page id in the 29-deck
removed_ids = {'P16', 'P18', 'P19', 'P20', 'P21', 'P22'}
sl = [s for s in sl if s['page'] not in removed_ids]
assert len(sl) == 23, len(sl)

# renumber contiguously
for i, s in enumerate(sl, start=1):
    s['page'] = 'P%02d' % i

# refresh titles to match edited SVGs
retitle = {
 2:  '汇报提纲：无人机把城市建筑的感知前沿推到哪',
 16: '第二道闸门：看得见 ≠ 读得准（诚实分级，含人类金标准验证）',
 21: '结论：无人机把建筑感知前沿显著向外推进',
}
for i, s in enumerate(sl, start=1):
    if i in retitle:
        s['action_title'] = retitle[i]

# the kept second-gate page (now P16) role/evidence: it's the spectrum figure
sl[15]['role'] = 'key_results'
sl[15]['evidence_sources'] = [
    {"source_id": "fig:legibility", "locator": "legibility spectrum", "kind": "figure"}]

d['slides'] = sl
json.dump(d, open('deck_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('deck resynced to', len(sl), 'slides')
for s in sl:
    print(s['page'], s['role'], s['action_title'][:40])
