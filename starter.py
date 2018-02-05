# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""

# Python内置库
import sys
import getopt

# 项目内部库
from db_connect.mgo import Mgo
from db_connect.mysql import Mysql
from db_connect.db_handler import DBHandler
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

        # 初始化数据库连接池
        self.db_connect_pool = []

        # 加载数据库
        # # MongoDB
        self._mgo = Mgo().conn
        self._connect_info(conn_res=self._mgo, db_type="MongoDB")
        # # MySQL
        self._mysql = Mysql(json_config=True).conn
        self._connect_info(conn_res=self._mysql, db_type="MySQL")

    def _connect_info(self, conn_res, db_type: str):
        """
        检查数据库连接情况,并写入连接池
        :param conn_res: 连接结果
        :param db_type: 数据库类型名称
        :return: 无返回值
        """
        if conn_res is not None:
            logger.info("%s 数据库连接成功!" % db_type)
            self.db_connect_pool.append(conn_res)
            return True
        else:
            logger.info("%s 数据源没有启用,请检查配置文件或检查数据库连接情况!" % db_type)
            return False

    def command(self):
        """
        获取用户指令
        :return: 无返回值
        """
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
            try:
                self._category.req_data()
                self._category.parse()
                result = self._category.node_list
            except Exception as err:
                logger.error(err)
            else:
                logger.info("分类总条数: %d 条" % len(result))
                if len(self.db_connect_pool) != 0:
                    logger.info("爬取结束,数据开始入库...")
                    db = DBHandler(
                        db_connect_pool=self.db_connect_pool,
                        data_list=result,
                        mgo_col_name="t_category",
                        mysql_query="INSERT INTO t_category(category_name, category_id, category_parent, category_type)"
                        " VALUES (%s, %s, %s, %s)"
                    )
                    db.insert_data()
                else:
                    logger.info("导出到Excel中...")
                    logger.info("功能待开发...敬请期待")

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
            self._data_spider = NationalDataWebsiteSpider(pid=pid,
                                                          data_type=data_type)
            try:
                result = self._data_spider.start_spider()
            except Exception as err:
                logger.error(err)
            else:
                if len(self.db_connect_pool) != 0:
                    logger.info("爬取结束开始入库...")
                    db = DBHandler(
                        db_connect_pool=self.db_connect_pool,
                        data_list=result,
                        mgo_col_name="t_year_data",
                        mysql_query="INSERT INTO t_year_data(data_info, data_year, data_name, data_unit) "
                                    "VALUES (%s, %s, %s, %s)"
                    )
                    db.insert_data()
                else:
                    logger.info("导出到Excel中...")
                    logger.info("功能待开发...敬请期待")
        else:
            logger.error("Data type or pid is error!")
            sys.exit(1)


if __name__ == '__main__':
    s = Starter(argv=sys.argv[1:])
    s.command()
