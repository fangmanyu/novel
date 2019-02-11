import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from items import Chapter
from scrapy_redis.spiders import RedisSpider


class BiqugeSingleNovelSpider(RedisSpider):
    """
    笔趣阁爬取一本小说
    """
    name = "biquge:single"
    allowed_domains = ['www.biquge5200.cc']
    redis_key = 'biquge_single:start_urls'

    custom_settings = {
        'ITEM_PIPELINES': {
            'novel_spider.pipelines.NovelSpiderPipeline': 10,
            'novel_spider.pipelines.BiqugeSinglePipeline': 1,
        }
    }

    def parse(self, response):
        number = 1
        for node in response.xpath(r'//div[@id="list"]/dl/dt[2]/following::dd'):
            chapter_url = node.css('a::attr(href)').extract_first()
            yield scrapy.Request(chapter_url, dont_filter=True, meta=dict(number=number), callback=self.parse_item)
            number += 1
        pass

    def parse_item(self, response):
        loader = ItemLoader(item=Chapter(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('content', '#content')
        loader.add_css('title', '.bookname h1::text')
        loader.add_xpath('book_name', '//div[@class="con_top"]/a[3]/text()')
        loader.add_value('url', response.url)
        loader.add_value('chapter_id', response.url)
        loader.add_value('crawl_time', datetime.datetime.now())
        loader.add_value('number', response.meta['number'])

        yield loader.load_item()
