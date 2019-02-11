# -*- coding: utf-8 -*-
import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import Rule

from items import Chapter
from scrapy_redis.spiders import RedisCrawlSpider
from util.common_utils import get_md5


class BiqugeCrawlSpider(RedisCrawlSpider):
    name = 'biquge:crawl'
    allowed_domains = ['www.biquge5200.cc']
    start_urls = ['https://www.biquge5200.cc/']
    rules = (
        Rule(LinkExtractor(allow=r'\d+?_\d+?/', allow_domains='www.biquge5200.cc'), follow=True),
        Rule(LinkExtractor(allow=r'\d+?_\d+?/\d+.html', allow_domains='www.biquge5200.cc'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'\w+?xiaoshuo/'), follow=True),
    )

    def process_results(self, response, results):
        if not isinstance(results, Chapter):
            return results

        results['chapter_id'] = get_md5(results['book_name'] + results['title'])
        yield results

    def parse_item(self, response):
        loader = ItemLoader(item=Chapter(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('content', '#content')
        loader.add_css('title', '.bookname h1::text')
        loader.add_xpath('book_name', '//div[@class="con_top"]/a[3]/text()')
        loader.add_value('url', response.url)
        loader.add_value('chapter_id', response.url)
        loader.add_value('crawl_time', datetime.datetime.now())

        return loader.load_item()
