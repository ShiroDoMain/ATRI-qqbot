# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 4:36 下午
# @Author  : Shiro
# @Site    : 
# @File    : tempEvent.py
# @Software: PyCharm
"""TempMessage"""
from engine import atri
from karas.box import (
    Yurine,
    MessageChain
)


class TempEvent:
    bot: Yurine

    @staticmethod
    @atri.bot.listen(__doc__)
    async def tempMessage(message: MessageChain):
        """临时消息事件"""
