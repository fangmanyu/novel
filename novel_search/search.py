import logging

import requests
from scrapy import Selector

from novel_spider.settings import SEARCH_BOOK_KEY
from scrapy_redis.connection import get_redis
from scrapy_redis.defaults import REDIS_ENCODING
from scrapy_redis.utils import bytes_to_str

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def search_url(searchkey):
    redis = get_redis()

    name = searchkey
    url = redis.hget(SEARCH_BOOK_KEY, name)
    if url:
        url = bytes_to_str(url, REDIS_ENCODING)
        logger.debug('从缓存中获取%s: %s', name, url)

    if not url:
        api = 'https://www.biquge5200.cc/modules/article/search.php'
        querystring = {"searchkey": searchkey}
        response = requests.get(url=api, params=querystring)
        logger.debug('从 %s 中获取searchkey: %s', api, searchkey)

        node = Selector(text=response.text).xpath('//tr[2]')
        url = node.css(r'.odd a::attr(href)').get()
        name = node.css(r'.odd a::text').get()

        if url:
            redis.hset(SEARCH_BOOK_KEY, name, url)
            logger.debug('%s: %s 存入缓存中' % (name, url))

    return name, url


if __name__ == '__main__':
    book_name, book_url = search_url('怪物乐园')
    print('书名： %s， url: %s' % (book_name, book_url))
