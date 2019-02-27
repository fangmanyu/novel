import sys
import threading

from scrapy.cmdline import execute

from novel_search.search import search_url
from novel_spider.settings import ROOT_PATH
from scrapy_redis.connection import get_redis
from scrapy_redis.picklecompat import loads

sys.path.extend(ROOT_PATH)
redis = get_redis()


def lpush():
    name, url = search_url('怪物乐园')
    redis.lpush('biquge_single:start_urls', url)
    global timer
    timer = threading.Timer(300, lpush)
    timer.start()


if __name__ == '__main__':
    execute(["scrapy", "crawl", "biquge:single"])
    # lpush()
    # for item in redis.lrange("biquge:items", 0, 1000):
    #     obj = loads(item)
    #     print(obj)

