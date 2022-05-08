# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:24 上午
# @Author  : Shiro
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
from karas.box import (
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


@atri.bot.listen(BotOnlineEvent.type)
async def onlineEvent():
    atri.bot.logging.info("Bot登陆成功")


@atri.bot.listen(BotOfflineEventForce.type)
async def offlineEvent():
    atri.bot.logging.error('Bot被迫离线')


@atri.bot.listen(BotOfflineEventDropped.type)
async def offlineDropEvent():
    atri.bot.logging.error('Bot与服务器断开连接')



class Core:
    @staticmethod
    def run():
        groupEvent.GroupEvent()
        friendEvent.FriendEvent()
        tempEvent.TempEvent()
        atri.bot.run_forever()
