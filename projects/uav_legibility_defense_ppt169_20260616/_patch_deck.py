# -*- coding: utf-8 -*-
import json
d = json.load(open('deck_plan.json', encoding='utf-8'))
slides = d['slides']

patch = {
 'P01': dict(action_title='无人机能把一座城市"看"到多深？——城市级航拍下建筑属性的感知前沿',
             claim='一次城市级无人机测量能把建筑属性的感知前沿向外推进多远'),
 'P03': dict(action_title='建筑数据集长期受限于可观测性——而无人机能推进感知前沿'),
 'P05': dict(action_title='无人机能把城市"看"到多深？感知前沿由两道闸门决定',
             claim='感知前沿 = 可观测性（几何，可改善）∩ 可判读性（定义，砸钱无解）'),
 'P14': dict(action_title='核心发现：感知前沿 = 可观测 ∩ 可判读'),
}
for s in slides:
    if s['page'] in patch:
        s.update(patch[s['page']])

# renumber P15..P28 -> P16..P29
for s in slides:
    n = int(s['page'][1:])
    if n >= 15:
        s['page'] = 'P%02d' % (n + 1)

new = {
  "page": "P15",
  "role": "key_results",
  "action_title": "第一道闸门：卫星18 / 街景28 / 无人机46+19，全城79.8%建筑街景够不着",
  "claim": "没有任何单一传统源超过28/46，且街景对79.8%的建筑物理够不着；无人机以一套采集取代两套并填补内街地块",
  "evidence_sources": [
    {"source_id": "fig:frontier", "locator": "fig6_frontier", "kind": "figure"},
    {"source_id": "tab:frontier", "locator": "perception frontier table", "kind": "table"}
  ],
  "layout_id": "figure_with_stats",
  "rhythm": "dense",
  "speaker_note": "本文最正面、最对口CEUS的核心硬数字。卫星只能物理观测18项屋顶属性，街景只能观测28项立面属性，无人机一次飞行全拿46项，再加19项需要点云的几何属性，65项里19项无人机独占。更关键：全城6836栋79.8%距最近街景点超过25米，街景物理够不着，其立面只有无人机能拍。对标Biljecki 2025的37.6%零覆盖，我们79.8%且能正面填补。审稿防御：用覆盖论证而非配准论证——街景对79.8%建筑是空的，卫星加街景联合也填不满。"
}
ins = next(i for i, s in enumerate(slides) if s['page'] == 'P16')
slides.insert(ins, new)

json.dump(d, open('deck_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('slides now:', len(d['slides']))
for s in d['slides']:
    print(s['page'], '|', s['role'], '|', s['action_title'][:44])
