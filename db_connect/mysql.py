# -*- coding: UTF-8 -*-
"""
Created on 2017年1月22日
@author: Leo
"""

# 系统库
import sys
import json

# 第三方库
import pymysql

# 项目内部库
from logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='mysql.py').get_logger()


# 错误字典
CODE_dict = {1045: "数据库用户名或者密码错误.",
             1049: "找不到当前数据库.",
             2003: "超时无法连接到数据库,数据库地址或端口错误"}

# SQL配置文件路径
SQL_CONFIG_PATH = "./conf/db.json"

# 初始化一堆数据库语句
# 语句
CREATE_DB = "CREATE DATABASE IF NOT EXISTS national_data DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"
CREATE_CATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS T_CATEGORY (" \
                        "id INT(11) NOT NULL AUTO_INCREMENT COMMENT '主键', " \
                        "category_name VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '节点名称', " \
                        "category_id VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '节点ID', " \
                        "category_parent VARCHAR(255) COLLATE utf8_general_ci COMMENT '父节点', " \
                        "category_type VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '数据类型(年度、月度、季度)', " \
                        "PRIMARY KEY (id)) " \
                        "ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;"

CREATE_YEAR_DATA_TABLE = "CREATE TABLE IF NOT EXISTS T_YEAR_DATA (" \
                         "id INT(11) NOT NULL AUTO_INCREMENT COMMENT '主键', " \
                         "data_name VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '数据名称', " \
                         "data_info FLOAT COLLATE utf8_general_ci COMMENT '数据', " \
                         "data_year VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '数据年份', " \
                         "data_unit VARCHAR(255) COLLATE utf8_general_ci NOT NULL COMMENT '数据单位', " \
                         "PRIMARY KEY (id)) " \
                         "ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;"


# 数据源
class DataSource:
    def __init__(
            self,
            host="127.0.0.1",
            port=3306,
            user="",
            password="",
            db="",
            charset="utf8",
            connect_timeout=2,
            json_config=False):

        # 如果json_config 为False需要检查参数
        if json_config is False and (user == "" or password == "" or db == ""):
            logger.debug("用户名密码或数据库名称不正确,请重试!")
            return

        # 如果json_config 为True则不用看参数是多少了
        if json_config:
            config = self._load_config_from_json()
            host = config['Host']
            port = config['Port']
            user = config['Username']
            password = config['Password']
            db = config['Database']
            logger.debug(
                "用户名:%s\t数据库名称:%s\t\t数据库地址:%s\t数据库端口:%s" %
                (user, db, host, port))

        # 初始化数据库名称需要用到
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._db_name = db

        try:
            # 数据库连接
            self.conn = pymysql.Connect(host=host,
                                        port=port,
                                        user=user,
                                        password=password,
                                        database=db,
                                        charset=charset,
                                        connect_timeout=connect_timeout)
            logger.debug("连接数据库成功!")
            if self._check_table() is not True:
                sys.exit(1)
        except Exception as err:
            # 数据库连接报错处理
            self._db_connect_error_handler(msg=tuple(eval(str(err))))

    def _db_connect_error_handler(self, msg):
        """
        数据库连接报错处理
        :param msg: 错误信息
        :return: 无返回值
        """
        if isinstance(msg[0], int):
            try:
                logger.debug(msg=CODE_dict[msg[0]] + "\t" + "详情: %s" % msg[1])
                # 判断找不到数据库的时候
                if msg[0] == 1049:
                    # 找不到数据库开始创建
                    logger.info("初始化数据库...")
                    self._init_database()
            except KeyError:
                logger.debug(msg=msg[1])

    @staticmethod
    def _load_config_from_json() -> dict:
        """
        从json读取MySQL配置信息
        :return:
        """
        try:
            db_config = json.loads(
                open(SQL_CONFIG_PATH,
                     encoding="UTF-8").read())['MySQL']
        except FileNotFoundError:
            db_config = json.loads(
                open("." + SQL_CONFIG_PATH,
                     encoding="UTF-8").read())['MySQL']
        # 这样输出比较好看
        # print(json.dumps(db_config, indent=4))
        return db_config

    def select_db(self, db_name: str):
        """
        选择数据库
        :param db_name: 数据库名称
        :return: 无返回值
        """
        try:
            self.conn.cursor().execute("USE %s" % db_name)
            logger.info("选择数据库成功! 数据库名: %s " % db_name)
        except Exception as err:
            self._db_connect_error_handler(msg=tuple(eval(str(err))))

    def _init_database(self):
        """
        初始化数据库
        问题:
        1. 初始化语句有点多而且不能动态扩展
        2. 表名没有在配置文件中配置
        :return: 无返回值
        """
        # 游标对象
        try:
            cursor = pymysql.connect(host=self._host,
                                     port=self._port,
                                     user=self._user,
                                     password=self._password,
                                     charset="utf8",
                                     connect_timeout=2).cursor()
            cursor.execute(CREATE_DB)
            logger.info("创建数据库成功! 数据库名: %s " % self._db_name)
            cursor.execute("USE %s" % self._db_name)
            # 初始化表
            self._init_table(cursor=cursor)
        except Exception as err:
            # 无数据库连接
            self._db_connect_error_handler(msg=tuple(eval(str(err))))

    @staticmethod
    def _init_table(cursor):
        """
        创建表
        :return: 无返回值
        """
        cursor.execute(CREATE_CATEGORY_TABLE)
        logger.info("创建表成功! 表名: t_category")
        cursor.execute(CREATE_YEAR_DATA_TABLE)
        logger.info("创建表成功! 表名: t_year_data")

    def _check_table(self) -> bool:
        """
        检查表是否创建成功
        :return: True就是创建成功 False创建失败
        """
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES;")
        res = [table_name[0] for table_name in cursor.fetchall()]
        if len(res) == 0:
            try:
                self.select_db(db_name=self._db_name)
                self._init_table(cursor=cursor)
                return True
            except Exception as err:
                self._db_connect_error_handler(msg=tuple(eval(str(err))))
                return False
        else:
            return True


if __name__ == '__main__':
    d = DataSource(json_config=True)
    print(d.conn)
