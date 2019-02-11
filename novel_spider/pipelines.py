# -*- coding: utf-8 -*-

import logging

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi

from util.common_utils import get_md5

logger = logging.getLogger(__name__)


class NovelSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class RedisPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    """
    使用twisted的异步容器，将写入数据库操作变为异步操作
    """

    def __init__(self, db_pool):
        self.__db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        """
        获取settings.py中的配置信息(固定写法)
        :param settings:
        :return:
        """
        db_parameters = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB_NAME'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True,
            cursorclass=DictCursor
        )
        # 可以将dict转变为可变参数
        # 创建异步数据库连接池
        db_pool = adbapi.ConnectionPool('MySQLdb', **db_parameters)

        # 实例化对象
        return cls(db_pool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.__db_pool.runInteraction(self.do_insert, item)
        # 添加异步异常处理
        query.addErrback(self.handle_error, spider, item)
        return item

    def do_insert(self, cursor, item):
        """
        执行具体插入逻辑
        :param cursor:
        :param item:
        :return:
        """
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        logger.debug('插入item: {}'.format(item['url']))

    def handle_error(self, failure, spider, item):
        """
        处理异步插入异常
        :param failure:
        :param spider:
        :param item:
        :return:
        """
        insert_sql, params = item.get_insert_sql()
        logger.error(insert_sql)
        logger.error(params)
        logger.error(failure)


class BiqugeSinglePipeline(object):
    def process_item(self, item, spider):
        item['chapter_id'] = get_md5(item['book_name'] + item['title'])
        return item
