# -*- coding: utf-8 -*-
# @Time : 2020/7/30 4:00 下午
# @Author : shiro
# @Software: PyCharm
import aiohttp
from graia.application.entry import Plain

ana = {
    '舔狗语录': 'https://chp.shadiao.app/api.php',
    '骂我': 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn',
    '鸡汤': 'https://du.shadiao.app/api.php',
    '祖安语录': 'https://nmsl.shadiao.app/api.php?lang=zh_cn',
}


async def Wget(url: str, headers=None, typ="plain"):
    print(2)
    if not headers:
        headers = {}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=2)) as session:
        async with session.get(url, headers=headers) as res:
            if typ == "plain":
                return res.status, await res.text()
            elif typ == "json":
                return res.status, await res.json()
            else:
                raise ValueError("Unknown type:", typ)


async def SendShadiaoAna(bot, group, message, source):
    print(1)
    await bot.sendGroupMessage(group, message.create([Plain(text=f'{(await Wget(ana[message.asDisplay()]))[1]}')]),
                               quote=source)
