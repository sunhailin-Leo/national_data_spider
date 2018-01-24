# -*- coding: UTF-8 -*-
"""
Created on 2018年1月15日
@author: Leo
"""

# 项目内部库
from logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='other_utils.py').get_logger()


class Utils:
    @staticmethod
    def _split_by_n(ls, n):
        for i in range(0, len(ls), n):
            yield ls[i:i + n]

    def split_by_n(self, ls, group):
        """
        等分List(有奇偶处理逻辑)
        逻辑: 将多出的部分和倒数第二组进行合并
        :param ls: 需要等分的list
        :param group: 组数
        :return: 返回划分结果
        """
        res = list(self._split_by_n(ls, int(len(ls) / group)))
        if len(res) != group:
            res = res[:-2] + [res[-2] + res[-1]]
        return res

    @staticmethod
    def check_data_type(data_type: str) -> bool:
        """
        校验数据类型
        :param data_type:
        :return: True: 校验成功; False: 校验失败
        """
        # data_type_list = ['hgnd', 'hgjd', 'hgyd']
        data_type_list = ['hgnd']
        if isinstance(data_type, str):
            if data_type not in data_type_list:
                logger.error("Wrong data type and now only support year data(hgnd)!")
                return False
            else:
                return True
        else:
            logger.error("You give wrong type on data_type!")
            return False

    def mgo_to_mysql(self, mongo_data) -> tuple:
        """
        将写入MongoDB的数据转换成mysql的形式
        dict -> tuple
        :return:
        """
        pass
