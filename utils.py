#!/usr/bin/env python3

import time

def log(*args, **kwargs):
    """
    用 log 代替 print
    time.time() 返回 Unix time
    再转为常用时间格式
    """
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)