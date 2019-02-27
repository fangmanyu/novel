import time

from wxpy import *

from scrapy_redis.connection import get_redis
from scrapy_redis.picklecompat import loads
from novel_consumption.wxbot import WXBot

logger = logging.getLogger(__name__)


class NovelConsumer(object):
    def __init__(self):
        self.redis = get_redis()

    def consumption(self):
        """
        消费redis中最新的小说章节
        :return: chapter
        """

        while True:
            item = self.redis.lpop("biquge:single:items")
            if item:
                logger.debug('consumer: getItem')
                yield loads(item)
            else:
                time.sleep(3)
            pass


redis = get_redis()


def consumer():
    while True:
        item = redis.lpop("biquge:single:items")
        if not item:
            # msg = yield loads(item)
            msg = yield 'c'
            print('consumer: %s' % msg)
        time.sleep(3)
        pass


def produce(c):
    c.send(None)
    n = 0
    while True:
        print('produce finish')
        c.send(n)

        n += 1


def item_process(item):
    title = item.get('title', '标题')
    book_name = item.get('book_name', '小说名')
    content = item.get('content', '内容').replace('\r\n', '\n\n')
    number = item.get('number', 0)
    msg = '{} {}, 序号： {}\n\n{}\n'.format(book_name, title, number, content)
    return msg


if __name__ == '__main__':
    wx = WXBot()
    friend = wx.get_friend()
    consumer = NovelConsumer()
    for item in consumer.consumption():
        msg = item_process(item)
        print(msg)
        wx.send_msg(msg, friend)

    print('finish')
