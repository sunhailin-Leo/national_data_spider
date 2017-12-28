# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""

# 项目内部库
from spiders.category_spider import CategorySpider


class Starter:
    def __init__(self):
        self._category = CategorySpider(data_type="hgnd")

    def start(self):
        self._category.req_data()
        self._category.parse()


if __name__ == '__main__':
    s = Starter()
    s.start()