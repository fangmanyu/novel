import os
import re

import requests
from fontTools.ttLib import TTFont
from settings import ROOT_PATH


def font_convert(font_html):
    comp = re.compile(r".*(; src: url\('(.*/(.*\.woff))'\))", re.S)
    woff_url = comp.match(font_html).group(2)
    woff_name = comp.match(font_html).group(3)
    content = re.match(r'.*(<span class=".*?">(.*?)</span></em>)', font_html).group(2)

    # 将woff文件和font mapping xml保存到本地
    path = os.path.join(os.path.join(ROOT_PATH, 'font'), woff_name)
    exists = os.path.exists(path)
    if not exists:
        r = requests.get(url=woff_url)
        with open(path, 'wb') as f:
            f.write(r.content)

    font = TTFont(path)
    if not exists:
        font.saveXML(path.replace('woff', 'xml'))

    # mapping
    nums = []
    map_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0',
        'period': '.'
    }
    font_map = font.getBestCmap()
    for mat in re.findall(r'&#(\d+?);', content):
        ca = font_map.get(int(mat))
        nums.append(map_dict[ca])

    return float(''.join(nums)) if '万' in font_html else float(''.join(nums)) / 10000


if __name__ == '__main__':
    html = "@font-face { font-family: XeIPegyY; src: url('https://qidian.gtimg.com/qd_anti_spider/XeIPegyY.eot?') " \
           "format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/XeIPegyY.woff') format('woff'), " \
           "url('https://qidian.gtimg.com/qd_anti_spider/XeIPegyY.ttf') format('truetype'); } .XeIPegyY { " \
           "font-family: 'XeIPegyY' !important;     display: initial !important; color: inherit !important; " \
           "vertical-align: initial !important; }</style><span " \
           "class=\"XeIPegyY\">&#100363;&#100357;&#100364;&#100362;&#100361;</span></em><cite>万字</cite> "
    font_convert(html)
