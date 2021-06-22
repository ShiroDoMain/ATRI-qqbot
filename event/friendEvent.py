# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 2:47 下午
# @Author  : Shiro
# @Site    : 
# @File    : friendEvent.py
# @Software: PyCharm
"""FriendMessage"""
from engine import atri
from graia.application.entry import *
from graia.broadcast import Broadcast


class FriendEvent:
    app: GraiaMiraiApplication
    bcc: Broadcast

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def messageEvent(friend: Friend, message: MessageChain):
        """好友消息事件"""

    @staticmethod
    @atri.bcc.receiver(NewFriendRequestEvent.type)
    async def newFriendEvent(event: NewFriendRequestEvent):
        """Bot收到请求添加好友事件"""
