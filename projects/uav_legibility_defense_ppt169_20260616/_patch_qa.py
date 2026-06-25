# -*- coding: utf-8 -*-
import json
d = json.load(open('deck_plan.json', encoding='utf-8'))
sl = d['slides']
# add human-gold table to source_map if missing
ids = {s['id'] for s in d['source_map']}
if 'tab:human_gold' not in ids:
    d['source_map'].append({
        "id": "tab:human_gold", "type": "table", "path": "sources/paper_v3.pdf",
        "title": "human gold-standard validation (40 buildings)",
        "parent_source": "paper:main"})
# P19 (idx18): human gold -> table evidence
sl[18]['evidence_sources'] = [
    {"source_id": "tab:human_gold", "locator": "human gold-standard table", "kind": "table"}]
# P20 (idx19): fly-lower is a conceptual argument, reclassify as method_or_model
sl[19]['role'] = 'method_or_model'
json.dump(d, open('deck_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('patched P19 evidence -> table; P20 role -> method_or_model')
