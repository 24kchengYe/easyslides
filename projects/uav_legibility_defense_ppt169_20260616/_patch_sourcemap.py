# -*- coding: utf-8 -*-
import json
d = json.load(open('deck_plan.json', encoding='utf-8'))
sm = d['source_map']
have = {s['id'] for s in sm}
# fix stale paper title
for s in sm:
    if s['id'] == 'paper:main':
        s['title'] = 'How Far Can a Drone See a City? (Perception Frontier)'
# add frontier figure + table sources
add = [
  {"id": "fig:frontier", "type": "figure", "path": "images/fig6_frontier.png",
   "title": "perception frontier (SV distance map + coverage curve + source bars)",
   "parent_source": "paper:main"},
  {"id": "tab:frontier", "type": "table", "path": "sources/paper_v3.pdf",
   "title": "perception frontier across sources (18/28/46+19)",
   "parent_source": "paper:main"},
]
for a in add:
    if a['id'] not in have:
        sm.append(a)
json.dump(d, open('deck_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('source_map now:', len(sm), 'ids:', [s['id'] for s in sm])
