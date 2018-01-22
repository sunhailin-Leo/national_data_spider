# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""

import sys
import getopt

# 项目内部库
from db_connect.mgo import Mgo
from utils.other_utils import Utils
from logger.LoggerHandler import Logger
from spiders.category_spider import CategorySpider
from spiders.data_spider import NationalDataWebsiteSpider


# 日志中心
logger = Logger(logger='starter.py').get_logger()


class Starter:
    def __init__(self, argv):
        # 命令行参数
        self._args = argv

        # 分类爬虫初始化
        self._category = None

        # 数据爬虫初始化
        self._data_spider = None

        # 工具类
        self._utils = Utils()

    def command(self):
        try:
            opts, args = getopt.getopt(self._args, 'hc:i:', ["category=", "pid="])
        except getopt.GetoptError:
            logger.info('starter.py -c 获取目录信息的id')
            logger.info('starter.py -i <pid> [获取某个id下的年度数据]')
            sys.exit(2)
        # 判断恶意传入参数的行为
        if len(opts) >= 2:
            opts = opts[:1]
        # 获取参数
        for opt, args in opts:
            if opt == ('-h', '--help'):
                logger.info('starter.py -c 获取目录信息的id')
                logger.info('starter.py -i <pid> [获取某个id下的年度数据]')
                sys.exit()
            elif opt in ('-c', '--category'):
                self.category_start(data_type=args)

            elif opt in ('-i', '--pid'):
                logger.info("Choose a data_type: (hgnd is only choice support now, so we set it default!)")
                logger.info("I will expand other choices in next version.")
                self.data_start(pid=args, data_type="hgnd")

    def category_start(self, data_type: str):
        """
        分类爬虫的启动方法

        注: 暂时只是输出. 存储到数据库的版本在下个版本进行开发
        :return: 无返回值
        """
        if self._utils.check_data_type(data_type=data_type):
            logger.info("开始分类爬虫...")
            self._category = CategorySpider(data_type="hgnd")
            self._category.req_data()
            self._category.parse()
        else:
            logger.error("Data type is error!")
            sys.exit(1)

    def data_start(self, pid: str, data_type: str):
        """
        数据爬虫的启动方法
        :param pid: 数据的ID
        :param data_type: 数据类型(目前只支持hgnd)
        :return:
        """
        if self._utils.check_data_type(data_type=data_type):
            logger.info("开始数据爬虫!...")
            self._data_spider = NationalDataWebsiteSpider(pid=pid, data_type=data_type)
            self._data_spider.start_spider()
        else:
            logger.error("Data type or pid is error!")
            sys.exit(1)


if __name__ == '__main__':
    s = Starter(argv=sys.argv[1:])
    s.command()
