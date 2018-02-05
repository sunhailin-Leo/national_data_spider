# -*- coding: UTF-8 -*-
"""
Created on 2018年1月15日
@author: Leo
"""
# Python内置库
import os
import itertools

# 第三方库
import pandas as pd

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

    def export_category_to_file(self,
                                data,
                                file_name: str,
                                output_path="./output_file",
                                file_type="csv"):
        """
        导出文件(使用pandas)
        :param data: category数据
        :param output_path: 输出路径
        :param file_name: 文件名
        :param file_type: 文件类型
        :return: 无返回值
        """

        # 判断输出文件夹是否存在
        if os.path.exists(output_path) is not True:
            os.mkdir(output_path)
        logger.info("导出到%s中" % file_type)
        # 导出路径
        if file_type == "excel":
            file_type = "xls"
        export_path = output_path + "/" + file_name + "." + file_type
        logger.info("导出路径: %s" % export_path)

        # 构造数据
        data = [list(d.values()) for d in data]
        df = pd.DataFrame(data, columns=["Name", "Code", "Parent_Code", "Type"])

        # 导出
        self.export_file(df=df, export_path=export_path, file_type=file_type)

    def export_data_to_file(self,
                            data,
                            file_name: str,
                            output_path="./output_file",
                            file_type="csv"):
        """
        导出文件(使用pandas)
        :param data: spider数据
        :param output_path: 输出路径
        :param file_name: 文件名
        :param file_type: 文件类型
        :return: 无返回值
        """
        # 判断输出文件夹是否存在
        if os.path.exists(output_path) is not True:
            os.mkdir(output_path)
        logger.info("导出到%s中" % file_type)
        # 导出路径
        if file_type == "excel":
            file_type = "xls"
        export_path = output_path + "/" + file_name + "." + file_type
        logger.info("导出路径: %s" % export_path)

        # 平滑数据 转换Dataframe
        flatten_data = list(itertools.chain.from_iterable(data))
        df = pd.DataFrame(flatten_data, columns=["Value", "Year", "Category_Name", "Unit"])
        df['Year'] = df['Year'].apply(lambda x: x.replace("年", ""))

        # 导出
        self.export_file(df=df, export_path=export_path, file_type=file_type)

    @staticmethod
    def export_file(df: pd.DataFrame, export_path: str, file_type: str):
        """
        导出文件
        :param df: DataFrame
        :param export_path: 路径
        :param file_type: 文件类型
        :return:
        """
        if file_type == "xls":
            df.to_excel(export_path,
                        index=False,
                        encoding="GBK")

        elif file_type == "csv":
            df.to_csv(path_or_buf=export_path,
                      index=False,
                      encoding="GBK")
        else:
            logger.error("Not Support this file type! Please select right type!")
