from wxpy import *
import logging
import time

logger = logging.getLogger(__name__)


class WXBot(object):
    def __init__(self):
        self.bot = Bot(cache_path=True)
        self.limit_count, self.limit_speed = self.send_limit()
        logger.info('limit_count: {}, limit_speed{}'.format(self.limit_count, self.limit_speed))

    def get_friend(self, name='魅丶泣'):
        return ensure_one(self.bot.friends().search(name))

    @dont_raise_response_error
    def send_msg(self, msg, friend):
        if not isinstance(friend, Friend):
            raise TypeError("friend type is %s, not %s" % (type(Friend), type(friend)))

        print('限制时间间隔： %f' % self.limit_speed)
        time.sleep(3)
        friend.send(msg)

    def send_limit(self):
        def action():
            self.bot.file_helper.send()
        result = detect_freq_limit(action)
        return result


if __name__ == '__main__':
    wx = WXBot()
    wx.send_msg('你好\n你好', wx.get_friend())

