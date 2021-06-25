# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:46 上午
# @Author  : Shiro
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import asyncio
import json
import os
import re
from typing import (
    List,
    Optional,
    Match
)

from graia.application.entry import (
    GraiaMiraiApplication,
    Session,
)
from graia.broadcast import Broadcast


class ATRI:
    """
    ATRI的核心，一切都在这里开始
    """

    def __init__(self):
        with open('cfg.json', 'r', encoding='utf-8') as cfg:
            self.cfg = json.load(cfg)
        self.loop = asyncio.get_event_loop()
        self.bcc = Broadcast(loop=self.loop)
        self.qq = self.cfg['botConfig']['qq']
        self.app = GraiaMiraiApplication(
            broadcast=self.bcc,
            connect_info=Session(
                host=self.cfg['botConfig']['host'],
                authKey=self.cfg['botConfig']['authKey'],
                account=self.qq,
                websocket=True
            )
        )
        self.qqai = self.cfg['qqai']['enable']
        self.setu = self.cfg['setu']
        self.sticker = self.cfg['sticker']
        self.onlyGroup = self.cfg['onlyGroup']
        self.shieldGroup = self.cfg['shieldGroup']
        self.shieldFriend = self.cfg['shieldFriend']
        self.illustrationSearch = self.cfg['illustrationSearch']
        self.animeSearch = self.cfg['animeSearch']

        self.qqaiAppid = self.cfg['qqai']['appid'] if self.cfg['qqai']['enable'] else None
        self.qqaiKey = self.cfg['qqai']['appkey'] if self.cfg['qqai']['enable'] else None
        self.setuPath = self.cfg['setu']['path'] if self.cfg['setu']['enable'] else None
        self.stickerPath = self.cfg['sticker']['path'] if self.cfg['sticker']['enable'] else None

    def loadBlackList(self) -> list:
        """
        载入黑名单，通常bot的主人不希望bot监听到这些人的消息
        :return: 配置中的黑名单
        """
        return self.cfg['blackList']

    def loadSticker(self) -> List[Optional[Match[str]]]:
        """
        载入sticker
        :return: 一个包含了jpg,png,gif,webp文件的match列表
        """
        stickers = []
        for sticker in os.listdir(self.cfg['sticker']['path']):
            name = re.match(r'(.*)\.[jpgw].*', sticker)
            if name:
                stickers.append(name)
        return stickers

    def refreshBlackList(self, blackList: list):
        self.cfg['backList'] = blackList


atri = ATRI()

from event import (
    friendEvent,
    groupEvent,
    tempEvent
)


class Core:
    @staticmethod
    def run():
        ge: groupEvent.GroupEvent()
        fe: friendEvent.FriendEvent()
        te: tempEvent.TempEvent()
        try:
            atri.app.launch_blocking()
        except KeyboardInterrupt:
            atri.app.logger.info("exit")
