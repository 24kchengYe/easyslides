# -*- coding: utf-8 -*-
# Fix smart/curly quotes that were wrongly used as XML attribute delimiters in
# page_01.svg, WITHOUT touching legitimate curly quotes inside CJK text content
# (e.g. "看"). Attribute quotes only occur inside tags, between < and >.
import re

f = 'svg_output/page_01.svg'
s = open(f, encoding='utf-8').read()

LD, RD = '“', '”'  # “ ”

def fix_tag(m):
    tag = m.group(0)
    # inside a tag, every curly double-quote is an attribute delimiter -> straight "
    return tag.replace(LD, '"').replace(RD, '"')

# process only text inside < ... > tags
s2 = re.sub(r'<[^>]*>', fix_tag, s)
open(f, 'w', encoding='utf-8').write(s2)

# report residual curly quotes (should only be in text content like 看)
import re as _re
inattr = len(_re.findall(r'=[“”]', s2))
print('remaining broken attr quotes:', inattr)
print('total curly quotes left (legit CJK content ok):',
      s2.count(LD) + s2.count(RD))
