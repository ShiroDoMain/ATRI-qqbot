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

from karas.box import (Yurine)


class ATRI:
    """
    ATRI的核心，一切都在这里开始
    """

    def __init__(self):
        with open('cfg.json', 'r', encoding='utf-8') as cfg:
            self.cfg = json.load(cfg)
        self.loop = asyncio.get_event_loop()
        self.qq = self.cfg['botConfig']['qq']
        name = self.cfg['botConfig']['botName']
        self.botConfig = self.cfg.get("botConfig")
        self.bot = Yurine(
            host=self.botConfig.get("host"),
            port=self.botConfig.get("port"),
            qq=self.qq,
            verifyKey=self.botConfig.get("verifyKey"),
            loop=self.loop,
            loggerLevel=self.botConfig.get("logLevel"),
            logToFile=self.botConfig.get("logToFile").get("enable"),
            logFileName=self.botConfig.get("logToFile").get("file") if self.botConfig.get("logToFile").get("enable") else None
        )
        self.name = name if name != "" else self.bot.fetchBotProfile().nickname

        self.setu = self.cfg['setu']
        self.sticker = self.cfg['sticker']
        self.onlyGroup = self.cfg['onlyGroup']
        self.shieldGroup = self.cfg['shieldGroup']
        self.shieldFriend = self.cfg['shieldFriend']
        self.illustrationSearch = self.cfg['illustrationSearch']
        self.animeSearch = self.cfg['animeSearch']
        self.chatBot = self.cfg['chatBot']
        self.weather = self.cfg['weather']

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
