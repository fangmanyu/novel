# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags

from items import QiDianBookItem
import datetime
import re
from util.qidian_utils import get_score
from util.common_utils import font_convert


class QidianSpider(CrawlSpider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com', 'book.qidian.com']
    start_urls = ['https://www.qidian.com/']

    rules = (
        Rule(LinkExtractor(allow=r'info/\d+', allow_domains='book.qidian.com'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'all|rank|finish|free|xuanhuan|qihuan|xianxia|youxi|kehuan/', deny=r'mm/'),
        #      follow=True),
    )
    comp = re.compile(r'.*?/info/(\d+)', re.DOTALL)
    score_and_comment_api = "https://book.qidian.com/ajax/comment/index"

    def process_results(self, response, results):
        if isinstance(results, scrapy.Item):
            # 获取评分
            if 'Set-Cookie' in response.headers:
                cookie = str(response.headers.getlist('Set-Cookie')[0])
                csrf = re.match(r'.*?_csrfToken=(.*?);', cookie).group(1)
            else:
                csrf = 'nsH2kveMyA1Gn7metQcu8oNcIdGTPaMma1TrNyzi'
            results['score'] = get_score(results['book_id'], csrf)

            # 获取数据统计
            statistics_list = re.findall(r'<em><style>(@font-face {.*?}.*?</span></em>.*?</cite>)',
                                         response.text, re.DOTALL)
            results['word_count'] = font_convert(statistics_list[0])
            results['click_total'] = font_convert(statistics_list[1])
            results['recommend_total'] = font_convert(statistics_list[3])

            yield results

    def parse_item(self, response):
        book_loader = ItemLoader(item=QiDianBookItem(), response=response)
        book_loader.default_output_processor = TakeFirst()

        tag_node = response.xpath('//div[@class="book-state"]/ul/li[1]')
        tag_list = remove_tags(response.css('.book-information .book-info .tag').extract_first()).split()
        if '作者自定义标签' in tag_node.xpath('/b/text()').extract_first(''):
            tag_node.xpath('/div[@class="detail"]').extract_first('')
            tag_list.append(remove_tags(
                tag_node.xpath('/div[@class="detail"]').extract_first()).split())
        book_loader.add_value('tags', ','.join(tag_list))
        book_loader.add_css('title', 'meta[name="keywords"]::attr(content)')
        book_loader.add_css('author', '.book-information .book-info h1 span a::text')
        book_loader.add_css('description', '.book-intro p')
        book_loader.add_value('url', response.url)
        book_loader.add_value('is_finish', '完本' in tag_list)
        book_loader.add_css('last_chapter', '.update .detail .cf a::text')
        book_loader.add_css('last_chapter_update_time', '.update .detail .cf .time::text')
        book_loader.add_value('crawl_time', datetime.datetime.now())
        book_id = self.comp.match(response.url).group(1)
        book_loader.add_value('book_id', book_id)

        return book_loader.load_item()
