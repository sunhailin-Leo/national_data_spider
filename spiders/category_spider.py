# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""

# 内部库
import requests

# 项目内部库
from utils.UserAgentMiddleware import UserAgentRotate


class CategorySpider:
    def __init__(self, data_type: str):
        # 根URL
        self._root_url = "http://data.stats.gov.cn/easyquery.htm"

        # request对象
        self._req = None

        # 数据类型 hgnd年度数据, hgjd季度数据, hgyd月度数据
        data_type_list = ['hgnd', 'hgjd', 'hgyd']
        if data_type not in data_type_list:
            raise ValueError("Wrong data type")
        self._data_type = data_type

        # UserAgent生成器
        self._ua = UserAgentRotate()

    def _post_data(self, _id="zb"):
        """
        构造请求数据
        :param _id: 节点id
        :return:
        """
        data = {
            "id": _id,
            "dbcode": self._data_type,
            "wdcode": "zb",
            "m": "getTree"
        }
        return data

    def _headers(self):
        """
        返回一个header
        :return: header
        """
        return self._ua.ua_generator()

    def req_data(self, data=None):
        """
        请求
        :return:
        """
        if data is None:
            self._req = requests.post(url=self._root_url,
                                      data=self._post_data(),
                                      headers=self._headers())
        else:
            self._req = requests.post(url=self._root_url,
                                      data=data,
                                      headers=self._headers())

    def parse(self):
        """
        解析页面json
        :return:
        """
        json_res = self._req.json()
        for node in json_res:
            # print(node)
            # name = node['name']
            # data_id = node['id']
            is_parent = node['isParent']
            if is_parent:
                # 存在子节点的继续递归
                self.req_data(data=self._post_data(_id=node['id']))
                self.parse()
            else:
                # 不存在则输出
                print(node)