# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 4:36 下午
# @Author  : Shiro
# @Site    : 
# @File    : tempEvent.py
# @Software: PyCharm
"""TempMessage"""
from engine import atri
from graia.application.entry import (
    GraiaMiraiApplication,
    MessageChain
)
from graia.broadcast import Broadcast


class TempEvent:
    app: GraiaMiraiApplication
    bcc: Broadcast

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def tempMessage(message: MessageChain):
        """临时消息事件"""
