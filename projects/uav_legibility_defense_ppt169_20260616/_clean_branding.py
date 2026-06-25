# -*- coding: utf-8 -*-
"""
Clean PPT branding to match the v4 perception-frontier pivot:
 1) every footer 'UAV-CityEngine · 可判读性' -> '感知前沿 · Perception Frontier'
 2) in-body 'UAV-CityEngine' brand word -> neutral wording (advisor: it's "out")
    - 'UAV-CityEngine 框架' / 'UAV-CityEngine框架' -> '本文框架'
    - 'UAV-CityEngine Workbench' -> '本文工作台'
    - 'UAV-CityEngine 工作台' -> '本文工作台'
    - 'UAV-CityEngine 代码' -> '本文代码'
    - '配开源 UAV-CityEngine。' -> '配套开源工作台。'
    - 'UAV-CityEngine 属性路由：' -> '属性路由：'
    - standalone 'UAV-CityEngine' (chapter title 三、框架：UAV-CityEngine) -> '本文方法管线'
NOTE: keeps the body 可判读性 content (P16-P22 second-gate section) untouched.
"""
import glob, re

FOOT_OLD = 'UAV-CityEngine · 可判读性'
FOOT_NEW = '感知前沿 · Perception Frontier'

# order matters: most specific first
BODY = [
    ('UAV-CityEngine Workbench', '本文工作台'),
    ('UAV-CityEngine 工作台', '本文工作台'),
    ('UAV-CityEngine 代码 + catalog 一并发布，供复现与扩展', '本文代码 + catalog 一并发布，供复现与扩展'),
    ('② UAV-CityEngine 代码', '② 本文代码'),
    ('UAV-CityEngine 代码', '本文代码'),
    ('配开源 UAV-CityEngine。', '配套开源工作台。'),
    ('UAV-CityEngine 属性路由：', '属性路由：'),
    ('三、框架：UAV-CityEngine', '三、框架：无人机属性管线'),
    ('UAV-CityEngine · Paper C2', '感知前沿 · Paper C2'),
    ('UAV-CityEngine框架', '本文框架'),
    ('UAV-CityEngine 框架', '本文框架'),
]

changed = []
for f in sorted(glob.glob('svg_output/page_*.svg')):
    s = open(f, encoding='utf-8').read()
    orig = s
    s = s.replace(FOOT_OLD, FOOT_NEW)
    for a, b in BODY:
        s = s.replace(a, b)
    # any stray remaining 'UAV-CityEngine' -> 本文方法
    s = s.replace('UAV-CityEngine', '本文方法')
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)
        changed.append(f)

print('changed files:', len(changed))
# verify none left
left = 0
for f in glob.glob('svg_output/page_*.svg'):
    left += open(f, encoding='utf-8').read().count('UAV-CityEngine')
print('remaining UAV-CityEngine occurrences:', left)
