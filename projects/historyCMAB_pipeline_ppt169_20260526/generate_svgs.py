"""Generate 15 SVG slides for historyCMAB pipeline presentation.
Uses academic_general design spec: Primary #003366, Accent #0066CC, Red #CC0000.
"""
import os, textwrap

OUT = os.path.join(os.path.dirname(__file__), "svg_output")
os.makedirs(OUT, exist_ok=True)

# ── Design tokens ──
PRIMARY = "#003366"
ACCENT = "#0066CC"
RED = "#CC0000"
LIGHT = "#E8F4FC"
WHITE = "#FFFFFF"
TEXT = "#333333"
GRAY = "#666666"
MUTED = "#999999"
CARD = "#F5F7FA"
BORDER = "#D0D7E0"
FONT = "Microsoft YaHei, Arial, sans-serif"

def header_bar(title, page_num=""):
    return f'''  <rect x="0" y="0" width="1280" height="70" fill="{PRIMARY}"/>
  <rect x="0" y="0" width="6" height="70" fill="{RED}"/>
  <text x="40" y="46" fill="{WHITE}" font-family="{FONT}" font-size="28" font-weight="bold">{title}</text>
  <text x="1240" y="46" text-anchor="end" fill="{WHITE}" font-family="{FONT}" font-size="16">{page_num}</text>'''

def keymsg_bar(msg, y=70):
    return f'''  <rect x="0" y="{y}" width="1280" height="48" fill="{LIGHT}"/>
  <rect x="0" y="{y}" width="6" height="48" fill="{ACCENT}"/>
  <text x="40" y="{y+32}" fill="{TEXT}" font-family="{FONT}" font-size="17">{msg}</text>'''

def footer(src="", section="", num=""):
    return f'''  <line x1="40" y1="665" x2="1240" y2="665" stroke="{LIGHT}" stroke-width="1"/>
  <text x="40" y="695" fill="{MUTED}" font-family="{FONT}" font-size="12">{src}</text>
  <text x="640" y="695" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="12">{section}</text>
  <text x="1240" y="695" text-anchor="end" fill="{GRAY}" font-family="{FONT}" font-size="14">{num}</text>'''

def card(x, y, w, h, title, body_lines, title_color=PRIMARY):
    body = "".join(f'<tspan x="{x+15}" dy="22">{l}</tspan>' for l in body_lines)
    return f'''  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{CARD}" stroke="{BORDER}"/>
  <text x="{x+15}" y="{y+28}" fill="{title_color}" font-family="{FONT}" font-size="16" font-weight="bold">{title}</text>
  <text x="{x+15}" y="{y+55}" fill="{TEXT}" font-family="{FONT}" font-size="13">{body}</text>'''

def text_block(x, y, lines, size=15, color=TEXT, line_h=24):
    parts = []
    for i, l in enumerate(lines):
        dy = 0 if i == 0 else line_h
        parts.append(f'<tspan x="{x}" dy="{dy}">{l}</tspan>')
    return f'  <text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" font-size="{size}">{"".join(parts)}</text>'

def svg_wrap(content):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="{WHITE}"/>
{content}
</svg>'''

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg_wrap(content))
    print(f"  wrote {name}")

# ═══════════════════════════════════════════════════
# Page 1: Cover
# ═══════════════════════════════════════════════════
write("01_cover.svg", f'''
  <rect x="0" y="0" width="1280" height="100" fill="{PRIMARY}"/>
  <rect x="0" y="0" width="6" height="100" fill="{RED}"/>
  <text x="640" y="290" text-anchor="middle" fill="{PRIMARY}" font-family="{FONT}" font-size="48" font-weight="bold">跨时代建筑矢量追踪</text>
  <text x="640" y="350" text-anchor="middle" fill="{PRIMARY}" font-family="{FONT}" font-size="48" font-weight="bold">Pipeline 定型与验证</text>
  <text x="640" y="410" text-anchor="middle" fill="{GRAY}" font-family="{FONT}" font-size="24">historyCMAB → CMAB-T 数据产品</text>
  <line x1="440" y1="445" x2="840" y2="445" stroke="{ACCENT}" stroke-width="2"/>
  <circle cx="640" cy="445" r="4" fill="{ACCENT}"/>
  <text x="640" y="500" text-anchor="middle" fill="{TEXT}" font-family="{FONT}" font-size="22">张业成</text>
  <text x="640" y="535" text-anchor="middle" fill="{GRAY}" font-family="{FONT}" font-size="18">清华大学建筑学院  |  导师：龙瀛</text>
  <rect x="0" y="665" width="1280" height="55" fill="{CARD}"/>
  <text x="640" y="698" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="14">2026 年 5 月</text>
''')

# ═══════════════════════════════════════════════════
# Page 2: 研究背景
# ═══════════════════════════════════════════════════
write("02_background.svg", f'''
{header_bar("研究背景", "2")}
{keymsg_bar("构建 CMAB-T，实现全国 3,667 城市双截面建筑实例级跨时代追踪")}
{card(40, 140, 380, 200, "Q1  多分辨率分割可比性",
      ["不同年份影像质量差异", "早期影像系统性粗约 12%", "导致提取结果不可比"])}
{card(450, 140, 380, 200, "Q2  建筑矢量规整化",
      ["分割掩膜锯齿边缘", "粘连和碎片伪影", "矢量化后缺乏几何规整性"])}
{card(860, 140, 380, 200, "Q3  跨时代建筑追踪",
      ["系统偏移 0.5-8.2m", "与真实拆建变化混合", "一对一实例匹配困难"])}
  <rect x="40" y="370" width="1200" height="50" rx="6" fill="{LIGHT}"/>
  <text x="640" y="402" text-anchor="middle" fill="{PRIMARY}" font-family="{FONT}" font-size="15" font-weight="bold">数据规模：训练 8,460 张  |  推理 3,681 历史 + 3,674 现代  |  覆盖 3,667 城市</text>
{footer("", "研究背景", "2/15")}
''')

# ═══════════════════════════════════════════════════
# Page 3: Pipeline 总览
# ═══════════════════════════════════════════════════
# Simple flow boxes
def flow_row(y, label, label_color, boxes):
    parts = [f'  <text x="40" y="{y+28}" fill="{label_color}" font-family="{FONT}" font-size="13" font-weight="bold">{label}</text>']
    x = 180
    bw = 170
    gap = 15
    for i, (t, sub) in enumerate(boxes):
        parts.append(f'  <rect x="{x}" y="{y}" width="{bw}" height="55" rx="4" fill="{CARD}" stroke="{label_color}" stroke-width="1.5"/>')
        parts.append(f'  <text x="{x+bw//2}" y="{y+22}" text-anchor="middle" fill="{TEXT}" font-family="{FONT}" font-size="12" font-weight="bold">{t}</text>')
        parts.append(f'  <text x="{x+bw//2}" y="{y+40}" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="9">{sub}</text>')
        if i < len(boxes) - 1:
            ax = x + bw
            parts.append(f'  <polygon points="{ax+2},{y+22} {ax+gap-2},{y+27} {ax+2},{y+33}" fill="{label_color}"/>')
        x += bw + gap
    return "\n".join(parts)

write("03_pipeline.svg", f'''
{header_bar("最终 Pipeline 总览", "3")}
{keymsg_bar("三个问题逐层递进 | 几何规整化在匹配之后做")}
{flow_row(150, "I. 可比分割", ACCENT, [
    ("卫星影像", "T1 早期 + T2 晚期"),
    ("HRNet 分割", "分辨率匹配, Dice=0.862"),
    ("侵蚀分割", "形态学切割粘连"),
])}
{flow_row(230, "II. 矢量规整化", "#27AE60", [
    ("GAN v7 规整化", "Edge Loss, IoU=0.885"),
    ("矢量化", "DP 简化 1m"),
    ("几何后处理", "RA 0.62→0.78"),
])}
{flow_row(310, "III. 跨时代追踪", "#E67E22", [
    ("偏移估计", "中位NN + 局部500m"),
    ("三轮匹配", "R1=0.4, R2=0.03"),
    ("Split/Merge", "coverage≥30%"),
    ("输出 CMAB-T", "persistent/demolished/new"),
])}
  <text x="640" y="420" text-anchor="middle" fill="{RED}" font-family="{FONT}" font-size="13" font-style="italic">* 几何后处理在匹配之后执行（消融实验：匹配前做匹配率降 5-10%）</text>
  <text x="640" y="445" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="12">DINOv2 语义相似度作为区域变化分层标注（不参与处理决策）</text>
{footer("", "Pipeline 总览", "3/15")}
''')

# ═══════════════════════════════════════════════════
# Pages 4-11: Content pages (text-heavy)
# ═══════════════════════════════════════════════════

content_pages = [
    # (filename, title, page, keymsg, lines)
    ("04_segmentation.svg", "Q1: 多分辨率可比分割", "4",
     "HRNet-W48 + SatlasPretrain + 在线分辨率分布匹配增强, Dice = 0.862",
     ["方法：",
      "  SatlasPretrain 初始化 (Bastani et al., 2023)",
      "  Laplacian 标定：早期 GSD 0.361m vs 晚期 0.330m（粗 12%）",
      "  在线高斯模糊按真实分布采样 sigma in {0, 0.46, 0.67, 0.90, 1.11, 1.37}",
      "  训练 8,460 张 x 9 城市, 4xRTX 4090, 早停 patience=30",
      "",
      "结果：",
      "  Dice = 0.862, mIoU = 0.758 (186/200 epoch)",
      "  极端退化 (sigma=3.0): 增强模型衰减 4.4% vs 无增强 13.4%",
      "  分辨率鲁棒性提升约 3 倍"]),

    ("05_model_compare.svg", "Q1: 模型对比", "5",
     "分布匹配增强对清晰影像提升有限, 但对退化影像鲁棒性提升显著",
     ["模型对比表：",
      "",
      "  HRNet-W48 v2 (分布匹配)    Dice=0.862  mIoU=0.758  ep186  ← 最佳",
      "  HRNet-W48 v2 (无增强)      Dice=0.854  mIoU=0.746  ep27   消融",
      "  OCRNet       (分布匹配)    Dice=0.857  mIoU=0.750  ep40   对比",
      "",
      "建筑实例分离 (侵蚀分割)：",
      "  形态学闭运算 → 渐进侵蚀 → 种子标记 → 距离变换扩展 → 边界切割",
      "  早期建筑实例 +15%, 晚期 +13%, A 类 Dice +0.037"]),

    ("06_gan.svg", "Q2: GAN 对抗式规整化", "6",
     "GAN v7 将锯齿分割掩膜转化为规整建筑轮廓, IoU = 0.885",
     ["架构：",
      "  Generator: EfficientNet-B0 U-Net, 4 通道输入 (RGB + Seg)",
      "  Discriminator: PatchGAN 31x31",
      "",
      "损失函数：L = L_adv + 10 L_L1 + 5 L_IoU + 5 L_edge",
      "  L_IoU: 可微 IoU 损失, 保持建筑面积",
      "  L_edge: 在 GT 建筑边界环带 (膨胀-腐蚀) 加权 L1",
      "         迫使生成器在相邻建筑间生成清晰分割线",
      "",
      "训练：SpaceNet 预训练 → 微调",
      "结果：IoU = 0.885, 直角率 = 0.52 (vs 流匹配 0.43)"]),

    ("07_geometry.svg", "Q2: 几何后处理", "7",
     "直角率 0.623 → 0.784 (+0.161), 10/10 城市一致提升",
     ["四步级联操作：",
      "  1. 矩形拟合：Rect(P) = Area(P) / Area(MRR(P)) > 0.80 → 最小旋转矩形",
      "  2. 边缘平直化：偏离主方向 +/-20 deg 的边对齐到精确角度",
      "  3. 直角校正：内角 90 +/- 20 deg → 精确 90 deg",
      "  4. 短边合并：小于 1.5m 的边合并; 面积守卫 > 15% 则回退",
      "",
      "关键设计决策：",
      "  在匹配之后做 (非匹配之前)",
      "  消融实验：匹配前做 → 匹配率降 5-10%",
      "  原因：矩形拟合在两期中以不同方式改变形状, 压低对应建筑 IoU"]),

    ("08_dinov2.svg", "Q3: DINOv2 语义相似度", "8",
     "区域变化分层标注 | 不参与匹配决策 | 服务于评估和数据产品质量",
     ["方法：",
      "  RoMa CNNandDinov2 编码器, 1024 维特征图",
      "  逐像素余弦相似度 S(p) = f_h(p) . f_m(p) / (||f_h|| ||f_m||)",
      "  高斯平滑 (sigma=5px, ~17m) → 全城市语义相似度地图",
      "",
      "XGBoost 区域变化分类 (670 个专家标注瓦片)：",
      "  A = 结构稳定 (~63%)   B = 局部拆建 (12%)",
      "  C = 格局全变 (~18%)   D = 消失 (4%)   E = 新增 (2%)",
      "  5-fold CV 准确率 72.2%, A 类 P=0.93 R=0.99",
      "",
      "定位：不参与偏移/匹配/split-merge 的任何决策",
      "  为评估指标提供分层基础 (A 类区域才看匹配率)",
      "  为下游数据使用者标注可信度"]),

    ("09_offset.svg", "Q3: 偏移估计", "9",
     "基于建筑质心的两阶段偏移估计, 实测 0.5-8.2m",
     ["v26 两阶段方法：",
      "  1. 全局：建筑质心 kd-tree 最近邻, 中位内点位移",
      "  2. 局部：500m 窗口互惠配对, 逐建筑精化",
      "",
      "为什么不用影像级配准？",
      "  RoMa 等光流方法估计 >20m (严重高估)",
      "  原因：建筑拆除重建后, 光流在不同纹理间建立像素对应 → 无意义大位移",
      "  建筑质心分布宏观稳定, 不受局部外观变化影响",
      "",
      "10 城市实测偏移：",
      "  1442(0.5m) 1801(1.0m) 1140(1.1m) 2448(1.6m) 3085(2.1m)",
      "  142(2.8m) 1981(3.2m) 2622(4.3m) 1360(5.4m) 2333(8.2m)"]),

    ("10_matching.svg", "Q3: 三轮上下文匹配", "10",
     "种子精/扩展广 策略, 1,260 组超参搜索验证",
     ["7 维代价函数：距离 + IoU + 面积比 + 朝向 + 长宽比 + 紧凑度 + Hausdorff",
      "",
      "第一轮 (种子筛选)：",
      "  IoU >= 0.4, 面积比 > 0.3, 朝向差 < 60 deg",
      "  搜索半径 R = max(min(4.0 x offset, 50), 20) m",
      "  贪心一对一分配",
      "",
      "第二轮 (IDW 引导扩展)：",
      "  IoU >= 0.03 (大幅放宽), K=8 近邻反距离加权插值",
      "  回收被严格种子遗漏的匹配",
      "",
      "关键发现：1,260 组超参数搜索",
      "  最优 vs 最差仅差 6% (50.2% vs 44.1%)",
      "  匹配率 50% 上限由分割一致性决定, 非参数瓶颈"]),

    ("11_splitmerge.svg", "Q3: 分裂与合并检测", "11",
     "persistent 43.6% → 68.4%, 回收 1,207 栋误判 demolished",
     ["问题：初始 demolished 57% 过高, 目视确认大量为分割不一致",
      "",
      "物理成因：",
      "  Split (1→N): L 形建筑在晚期拐角处断裂为两个矩形",
      "  Merge (N→1): 相邻建筑残余粘连被提取为连片多边形",
      "  一对一匹配框架无法处理, 错误标记为 demolished + new",
      "",
      "检测方法：",
      "  偏移校正后空间重叠检测 (STR-tree 加速)",
      "  cov(i) = Sum(Area(P_h^i ∩ P_m^j)) / Area(P_h^i)",
      "  coverage >= 30% 且重叠 N>1 → split; 反向 → merge",
      "",
      "结果：215 split + 268 merge, A 类匹配率 45% → 71%"]),
]

for fname, title, pnum, km, lines in content_pages:
    body = text_block(50, 155, lines, size=15, line_h=26)
    write(fname, f'''
{header_bar(title, pnum)}
{keymsg_bar(km)}
{body}
{footer("", title, f"{pnum}/15")}
''')

# ═══════════════════════════════════════════════════
# Page 12: 验证结果
# ═══════════════════════════════════════════════════
# Simple table via text
table_lines = [
    "142 城市验证结果：",
    "",
    "  类别            子类          数量     占比      mean IoU",
    "  ─────────────────────────────────────────────────────────",
    "  persistent                   3,322    68.4%",
    "                  unchanged      447              0.817",
    "                  minor          641              0.597",
    "                  major        2,019              0.566",
    "                  split (1→N)    215              0.670",
    "                  merge (N→1)    268              —",
    "  demolished                   1,534    31.6%     —",
    "  new                          1,315    31.8%     —",
    "",
    "  历史 4,856 栋 | 现代 4,136 栋 | 偏移 2.8m | A 类占比 83% (稳定型城市)",
]
write("12_validation.svg", f'''
{header_bar("142 城市验证结果", "12")}
{keymsg_bar("A 类匹配率 45% → 71% | 持续率 68.4%")}
{text_block(50, 155, table_lines, size=14, line_h=24)}
{footer("", "验证结果", "12/15")}
''')

# ═══════════════════════════════════════════════════
# Page 13: 设计决策
# ═══════════════════════════════════════════════════
decisions = [
    ("1. 几何规整化在匹配之后做", "矩形拟合改变形状, 匹配前做会压低对应建筑 IoU"),
    ("2. 种子精/扩展广 匹配策略", "R1=0.40 保证种子质量, R2=0.03 最大化召回"),
    ("3. 匹配率上限由分割一致性决定", "1,260 组参数最优最差仅差 6%, 非参数瓶颈"),
    ("4. 基于建筑质心的偏移估计", "光流对长时序外观变化敏感, 质心分布宏观稳定"),
    ("5. DINOv2 作为评估分层标注", "不参与处理决策, 为评估和数据产品质量服务"),
]
dec_parts = []
for i, (t, d) in enumerate(decisions):
    y = 140 + i * 90
    dec_parts.append(f'  <rect x="40" y="{y}" width="4" height="70" fill="{ACCENT}"/>')
    dec_parts.append(f'  <text x="60" y="{y+25}" fill="{PRIMARY}" font-family="{FONT}" font-size="17" font-weight="bold">{t}</text>')
    dec_parts.append(f'  <text x="60" y="{y+52}" fill="{GRAY}" font-family="{FONT}" font-size="14">{d}</text>')

write("13_decisions.svg", f'''
{header_bar("关键设计决策", "13")}
{"".join(dec_parts)}
{footer("", "设计决策", "13/15")}
''')

# ═══════════════════════════════════════════════════
# Page 14: 下一步
# ═══════════════════════════════════════════════════
plans = [
    ("1", "10 个消融城市多城市验证", "跨气候区参数泛化性检验"),
    ("2", "全量 3,667 城市跑 Pipeline", "预计数小时内完成 (~2s/城市)"),
    ("3", "人工抽样验证", "3 个稳定型城市各抽 50 个匹配对"),
    ("4", "论文初稿", "投稿 RSE / ISPRS JPRS"),
    ("5", "CMAB-T 数据产品 schema", "字段定义 + 质量标注 + 元数据"),
]
plan_parts = []
for i, (n, t, d) in enumerate(plans):
    y = 145 + i * 85
    plan_parts.append(f'  <circle cx="70" cy="{y+20}" r="18" fill="{ACCENT}"/>')
    plan_parts.append(f'  <text x="70" y="{y+26}" text-anchor="middle" fill="{WHITE}" font-family="{FONT}" font-size="16" font-weight="bold">{n}</text>')
    plan_parts.append(f'  <text x="105" y="{y+18}" fill="{TEXT}" font-family="{FONT}" font-size="17" font-weight="bold">{t}</text>')
    plan_parts.append(f'  <text x="105" y="{y+42}" fill="{GRAY}" font-family="{FONT}" font-size="14">{d}</text>')

write("14_next.svg", f'''
{header_bar("下一步计划", "14")}
{keymsg_bar("从单城市验证走向全国数据产品")}
{"".join(plan_parts)}
{footer("", "下一步", "14/15")}
''')

# ═══════════════════════════════════════════════════
# Page 15: Ending
# ═══════════════════════════════════════════════════
write("15_ending.svg", f'''
  <rect x="0" y="0" width="1280" height="100" fill="{PRIMARY}"/>
  <rect x="0" y="0" width="6" height="100" fill="{RED}"/>
  <text x="640" y="300" text-anchor="middle" fill="{PRIMARY}" font-family="{FONT}" font-size="56" font-weight="bold">感谢聆听</text>
  <text x="640" y="365" text-anchor="middle" fill="{GRAY}" font-family="{FONT}" font-size="24">欢迎批评指正</text>
  <line x1="460" y1="400" x2="820" y2="400" stroke="{ACCENT}" stroke-width="2"/>
  <circle cx="640" cy="400" r="4" fill="{RED}"/>
  <rect x="360" y="440" width="560" height="100" rx="8" fill="{CARD}"/>
  <text x="640" y="478" text-anchor="middle" fill="{TEXT}" font-family="{FONT}" font-size="18">张业成  |  清华大学建筑学院</text>
  <text x="640" y="510" text-anchor="middle" fill="{GRAY}" font-family="{FONT}" font-size="16">cyz575860760@gmail.com</text>
  <rect x="0" y="665" width="1280" height="55" fill="{CARD}"/>
  <text x="640" y="698" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="14">2026 年 5 月</text>
  <text x="1240" y="698" text-anchor="end" fill="{MUTED}" font-family="{FONT}" font-size="14">15/15</text>
''')

print(f"\nAll {len(os.listdir(OUT))} SVGs generated in {OUT}")
