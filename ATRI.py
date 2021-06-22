# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 4:40 下午
# @Author  : Shiro
# @Site    : 
# @File    : ATRI.py
# @Software: PyCharm
from engine import atri
if __name__ == '__main__':
    try:
        atri.app.launch_blocking()
    except KeyboardInterrupt:
        atri.app.logger.info("exit")

