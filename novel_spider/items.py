# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags, remove_tags_with_content


class NovalSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QiDianBookItem(scrapy.Item):
    book_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    is_finish = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field(
        input_processer=MapCompose(lambda x: x.replace('\u3000', ''), remove_tags, str.strip)
    )
    # 评分
    score = scrapy.Field()
    # 字数
    word_count = scrapy.Field()
    # 总点击量
    click_total = scrapy.Field()
    # 总推荐量
    recommend_total = scrapy.Field()
    # 最新章节
    last_chapter = scrapy.Field()
    # 最新章节更新时间
    last_chapter_update_time = scrapy.Field()
    # 爬取时间
    crawl_time = scrapy.Field()
