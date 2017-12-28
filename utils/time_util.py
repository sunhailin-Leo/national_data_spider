# -*- coding: UTF-8 -*-
"""
Created on 2017年12月28日
@author: Leo
"""

import time
import datetime


class TimeUtil:

    @staticmethod
    def millisecond_timestamp():
        return int(round(time.time() * 1000))
