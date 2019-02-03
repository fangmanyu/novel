# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


class NovelSpiderItem(scrapy.Item):
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
        input_processor=MapCompose(lambda x: x.replace('\u3000', ''), remove_tags, str.strip)
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

    def get_insert_sql(self):
        insert_sql = 'insert into novel_book(book_id, url, title, author, is_finish, tags, description, score, ' \
                     'word_count, click_total, recommend_total, crawl_time) values(%s, %s, %s, %s, %s, %s, %s, %s,' \
                     ' %s, %s, %s, %s) on DUPLICATE key update score=values(score), word_count=values(word_count), ' \
                     'click_total=values(click_total), recommend_total=values(recommend_total), ' \
                     'crawl_time=values(crawl_time), is_finish=values(is_finish);'

        params = (self['book_id'], self['url'], self['title'], self['author'], int(self['is_finish']), self['tags'],
                  self['description'], self['score'], self['word_count'], self['click_total'], self['recommend_total'],
                  self['crawl_time'])

        return insert_sql, params
