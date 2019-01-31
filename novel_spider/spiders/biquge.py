# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BiqugeSpider(CrawlSpider):
    name = 'biquge'
    allowed_domains = ['www.qu.la']
    start_urls = ['https://www.qu.la/']

    rules = (
        Rule(LinkExtractor(allow=r'book/\d+?/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
