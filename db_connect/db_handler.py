# -*- coding: UTF-8 -*-
"""
Created on 2018年1月27日
@author: Leo
"""

# Python内部库
import sys
from collections import OrderedDict

# 第三方库
from pymongo.database import Database
from pymysql.connections import Connection

# 项目内部库
from logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='db_handler.py').get_logger()


class DBHandler:
    def __init__(self,
                 db_connect_pool: list,
                 data_list: list,
                 mgo_col_name=None,
                 mysql_query=None):
        """
        :param db_connect_pool: 连接池
        :param data_list: 数据
        :param mgo_col_name: MongoDB集合名
        :param mysql_query: SQL语句
        """

        # 数据库连接池
        self._pool = db_connect_pool

        # 数据
        self._data = data_list

        # MongoDB的一些配置
        self._mgo_col_name = mgo_col_name

        # MySQL的一些配置
        self._query = mysql_query

    def cast(self):
        """
        数据转换 Orderdict/dict -> tuple
        :return:
        """
        if isinstance(self._data[0], OrderedDict):
            tuple_list = \
                [tuple(data.values()) for data in self._data]
            return tuple_list
        if isinstance(self._data[0], dict):
            tuple_list = \
                [self._cast_single_tuple(data=data) for data in self._data]
            return tuple_list

    @staticmethod
    def _cast_single_tuple(data):
        """
        转换单个数据 主要用于dict -> tuple
        因为Python3.5以下的dict都是无序的.
        :param data:
        :return:
        """
        return tuple([data['category_name'],
                      data['category_id'],
                      data['category_parent'],
                      data['category_type']])

    def _insert_mongodb(self, mgo_conn: Database):
        """
        MongoDB写入方法
        :param mgo_conn: MongoDB的连接对象
        :return: 无返回值
        """
        try:
            col = mgo_conn[self._mgo_col_name]
            col.insert_many(documents=[dict(data) for data in self._data],
                            ordered=True)
            logger.info("MongoDB数据写入完成")
        except Exception as err:
            logger.error(err)

    def _insert_mysql(self, mysql_conn: Connection):
        """
        MySQL写入方法
        :param mysql_conn: MySQL连接对象
        :return: 无返回值
        """
        if self._query is not None:
            # 转换
            insert_data = self.cast()
            cursor = mysql_conn.cursor()
            try:
                execute_result = cursor.executemany(query=self._query, args=insert_data)
                mysql_conn.commit()
                logger.info("MySQL数据写入完成! 返回信息: %s" % str(execute_result))
            except Exception as err:
                logger.error(err)
                mysql_conn.rollback()
            finally:
                mysql_conn.close()
        else:
            logger.debug("MySQL数据库语句不正确或为空.")
            sys.exit(1)

    def insert_data(self):
        """
        根据数据库连接池选择数据源入口
        :return:
        """
        for conn in self._pool:
            if isinstance(conn, Database):
                self._insert_mongodb(mgo_conn=conn)
            if isinstance(conn, Connection):
                self._insert_mysql(mysql_conn=conn)
