# -*- coding: utf-8 -*-
# @Time : 2020/8/2 9:01 上午
# @Author : shiro
# @Software: PyCharm
import qqai
from engine import Plain


async def sendMessage(bot, groupId, source, msg):
    await bot.sendGroupMessage(groupId, [Plain(text=f'{msg}')], source)
