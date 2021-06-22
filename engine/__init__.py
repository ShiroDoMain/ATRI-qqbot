# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:46 上午
# @Author  : Shiro
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import asyncio
import json

from graia.application.entry import *
from graia.broadcast import Broadcast


class ATRI:
    """
    ATRI的核心，一切都在这里开始
    """

    def __init__(self):
        with open('cfg.json', 'r') as cfg:
            self.cfg = json.load(cfg)
        self.loop = asyncio.get_event_loop()
        self.bcc = Broadcast(loop=self.loop)
        self.app = GraiaMiraiApplication(
            broadcast=self.bcc,
            connect_info=Session(
                host=self.cfg['botConfig']['host'],
                authKey=self.cfg['botConfig']['authKey'],
                account=self.cfg['botConfig']['qq'],
                websocket=True
            )
        )
        self.qqaiAppid = self.cfg['qqai']['appid'] if self.cfg['qqai']['enable'] else None
        self.qqaiKey = self.cfg['qqai']['appkey'] if self.cfg['qqai']['enable'] else None
        self.setuPath = self.cfg['setu']['path'] if self.cfg['setu']['enable'] else None

    def loadBlackList(self) -> list:
        """
        载入黑名单，通常bot的主人不希望bot监听到这些人的消息
        :return: 配置中的黑名单
        """
        return self.cfg['blacklist']

    def refreshBlackList(self, blackList: list):
        self.cfg['backList'] = blackList


atri = ATRI()
