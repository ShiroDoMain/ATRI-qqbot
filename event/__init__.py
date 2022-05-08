# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:24 上午
# @Author  : Shiro
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from graia.application.entry import (
    BotOnlineEvent,
    BotOfflineEventDropped,
    BotOfflineEventForce
)

from engine import atri
from event import (
    groupEvent,
    friendEvent,
    tempEvent
)

"""ATRI的事件处理模块""" 


@atri.bcc.receiver(BotOnlineEvent.type)
async def onlineEvent():
    atri.app.logger.info("Bot登陆成功")


@atri.bcc.receiver(BotOfflineEventForce.type)
async def offlineEvent():
    atri.app.logger.error('Bot被迫离线')


@atri.bcc.receiver(BotOfflineEventDropped.type)
async def offlineDropEvent():
    atri.app.logger.error('Bot与服务器断开连接')


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
