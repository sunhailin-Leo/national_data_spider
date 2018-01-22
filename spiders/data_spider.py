# -*- coding: UTF-8 -*-
"""
Created on 2017年1月20日
@author: Leo
"""

import sys
import json
import logging
import requests
import urllib.parse as up
from pymongo import MongoClient

# 项目内部库
from logger.LoggerHandler import Logger
from utils.time_util import TimeUtil
from utils.UserAgentMiddleware import UserAgentRotate
from utils.other_utils import Utils


# 日志中心
logger = Logger(logger='data_spider.py').get_logger()


class NationalDataWebsiteSpider:
    def __init__(self,
                 pid: str,
                 data_type: str,
                 db_name="national_data",
                 col_name="test_1"):
        """
        :param pid: pid是爬取的表的id
        :param data_type: data_type是数据类型
        """
        self._pid = pid

        # 需要知道链接所对应数据是年度、季度、月度
        # 年度: hgnd; 季度: ; 月度: ;
        self._data_type = data_type

        # 时间类
        self._t = TimeUtil()

        # URL的一些参数
        self._wds = up.quote("[]")
        self._dfwds = up.quote('[{"wdcode":"zb","valuecode":"' + self._pid + '"}]')
        self._url = "http://data.stats.gov.cn/easyquery.htm" \
                    "?m=QueryData" \
                    "&dbcode=" + self._data_type + "" \
                    "&rowcode=zb" \
                    "&colcode=sj" \
                    "&wds=" + self._wds + "" \
                    "&dfwds=" + self._dfwds + "" \
                    "&k1=" + str(self._t.millisecond_timestamp())
        logging.info(self._url)

        # 对应数据长度选项表(目前都选最后一个)  --- 暂时还未使用需要和数据类型进行对应
        self._year = ['LAST5', 'LAST10', 'LAST20']
        self._season = ['LAST6', 'LAST12', 'LAST18']
        self._month = ['LAST13', 'LAST24', 'LAST36']

        # UserAgent生成器
        self._ua = UserAgentRotate()

        # 工具方法
        self._util = Utils()

        # 初始化页面url
        self.referer_url = "http://data.stats.gov.cn/easyquery.htm?cn=C01&zb=" + self._pid + "&valuecode=LAST20"

        # 初始化headers
        self.headers = None

        # 请求返回的结果(初始化)
        self._json_res = None

        # 数据库配置(暂时)
        self._db_name = db_name
        self._col_name = col_name

    def _headers(self):
        """
        生成一个header
        :return: 无返回值
        """
        self.headers = {
            "Referer": self.referer_url,
            "User-Agent": self._ua.ua_generator()['User-Agent'],
            "X-Requested-With": "XMLHttpRequest"
        }

    def _request(self):
        """
        请求url获取返回值
        :return: 无返回值
        """
        response = requests.get(url=self._url, headers=self.headers)
        html_content = response.content.decode("UTF-8")
        self._json_res = json.loads(html_content)

    def _parse(self):
        """
        解析请求方法返回的数据
        :return: 无返回值
        """
        json_res = self._json_res
        if json_res is None:
            logger.error("Request can not get the data return. Please try again later!")
            sys.exit(1)

        # 获取category名称和数据单位
        name_list = []
        unit_list = []
        for name in json_res['returndata']['wdnodes'][0]['nodes']:
            name_list.append(name['name'])
            unit_list.append(name['unit'])

        # 时间轴
        year_list = []
        for year in json_res['returndata']['wdnodes'][1]['nodes']:
            year_list.append(year['name'])

        # 数据
        data_list = []
        for data in json_res['returndata']['datanodes']:
            data_list.append(data['data']['data'])
        data_list = self._util.split_by_n(ls=data_list, group=len(name_list))

        final = [{"name": name_list[i],
                  "year": year_list,
                  "data": data_list[i],
                  "unit": unit_list[i]} for i in range(len(name_list))]

        # 写进数据(暂时将数据库写入代码丢在这, MongoDB数据库连接类已经写好, 暂时还没使用)
        conn = MongoClient(host="127.0.0.1", port=27017)
        db = conn[self._db_name]
        col = db[self._col_name]
        for each_data in final:
            col.insert(each_data)

    def start_spider(self):
        """
        启动类
        :return: 无返回值
        """
        self._headers()
        self._request()
        self._parse()


if __name__ == '__main__':
    national = NationalDataWebsiteSpider(pid='A0203', data_type='hgnd')
    national.start_spider()
