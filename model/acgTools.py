# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 8:38 上午
# @Author  : Shiro
# @File    : acgTools.py
# @Software: PyCharm
import os, random

from engine import atri

setu = atri.setu


class SetuTime:
    path = setu['path']
    enable = setu['enable']
    cmd = setu['command']
    flash = setu['flash']

    @classmethod
    def _loadSetu(cls):
        return os.listdir(atri.setu['path'])

    @classmethod
    def randomSetu(cls):
        setuList = cls._loadSetu()
        s = setuList[random.randrange(len(setuList)) - 1]
        return cls.path + s
