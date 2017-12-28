# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""


class DataSpider:
    def __init__(self, pid: str, long: -1):
        """
        :param pid: pid是爬取的表的id
        :param long: 长度选择,不同表都有限制,目前都是选最后一个,所以默认写了-1
        """
        self._pid = pid

        # 对应数据长度选项表(目前都选最后一个)
        year = ['LAST5', 'LAST10', 'LAST20']
        season = ['LAST6', 'LAST12', 'LAST18']
        month = ['LAST13', 'LAST24', 'LAST36']

        # 需要知道链接所对应数据是年度、季度、月度
        self._data_type = ""

    def _post_data(self):
        data = {
            "m": "QueryData",
            "dbcode": self._data_type,
            "rowcode": "zb",
            "colcode": "sj",
            "wds": [],
            "dfwds": [{"wdcode": "zb", "valuecode": self._pid}],
            "k1": "时间戳"
        }
        return data
