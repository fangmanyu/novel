import hashlib
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


def remove_character(content, *chars):
    if not isinstance(content, str):
        raise TypeError('content must str type')

    for char in chars:
        content = content.replace(char, '')

    return content


def chapter_content_process(content, replace_rule=None):
    """
    对小说章节内容的处理，用于删除或替换一些文字或字符
    :param content: 需要处理的文字
    :param replace_rule: 自定义替换内容.dict类型
    :return: 处理后的内容
    """
    if not isinstance(content, str):
        raise TypeError('content must str type')

    content = remove_character(content, '\u3000', '\xa0', '\t', '〖∷更新快∷无弹窗∷纯文字∷〗', '请收藏本站阅读最新小说!',
                               'chaptererror();', '本书最快更新网站请百度搜索：，或者直接访问网站')

    for k, v in replace_rule.items() if replace_rule else {}.items():
        content = content.replace(k, v)

    return content


def get_md5(content):
    if isinstance(content, str):
        content = content.encode('utf-8')
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()


if __name__ == '__main__':
    content_str = '\u3000 \u3000dasdad\u3000阿森跟\u3000跟个〖∷更新快∷无弹窗∷纯文字∷〗'
    print(remove_character(content_str, '\u3000', '阿森跟'))
    print(chapter_content_process(content_str, replace_rule={' ': '去玩儿', '个': ''}))
