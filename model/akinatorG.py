# -*- coding: utf-8 -*-
# @Time    : 7/26/2021 9:21 PM
# @Author  : Siltal
# @Site    :
# @File    : akinatorG.py
# @Software: PyCharm
"""need VPN"""

import akinator
from graia.application import MessageChain
from graia.application.message.elements.internal import Plain, Image

from engine import atri


class akinatorGame():
    aki = akinator.Akinator()
    AkinatorCmd = atri.Akinator['command'] if atri.Akinator['enable'] else []
    hold = False
    end = False

    @staticmethod
    async def process(messagePlain: str, group, member):
        """
        处理游戏进度
        :param messagePlain
        :param group
        :param member
        """
        global a, q
        if messagePlain == "exit":
            akinatorGame.hold = False
            akinatorGame.end = False

        if akinatorGame.end:  # 评价结果
            if messagePlain.lower() == "yes" or messagePlain.lower() == "y":
                await atri.app.sendGroupMessage(group, MessageChain.create(
                    [
                        Plain("Yay")
                    ]
                ))
            else:
                await atri.app.sendGroupMessage(group, MessageChain.create(
                    [
                        Plain("Oof")
                    ]
                ))
            akinatorGame.end = False
        if akinatorGame.hold and messagePlain in [
            'yes', 'y', '0',
            'no', 'n', '1',
            'i', 'idk', 'i dont know', "i don't know", '2',
            'probably', 'p', '3',
            'probably not', 'pn', '4'
        ]:  # 分支过程中
            a = messagePlain
            if a == "b":
                try:
                    q = akinatorGame.aki.back()
                    await atri.app.sendGroupMessage(group, MessageChain.create(
                        [
                            Plain(q)
                        ]
                    ))
                except akinator.CantGoBackAnyFurther:
                    pass
            else:
                q = akinatorGame.aki.answer(a)
                await atri.app.sendGroupMessage(group, MessageChain.create(
                    [
                        Plain(q + "\n\t"),
                        Plain(f"{akinatorGame.aki.progression}%")
                    ]
                ))

            if akinatorGame.aki.progression > 99:  # 给出结果
                akinatorGame.hold = False
                akinatorGame.aki.win()
                await atri.app.sendGroupMessage(group, MessageChain.create(
                    [
                        Plain(
                            f"It's {akinatorGame.aki.first_guess['name']} ({akinatorGame.aki.first_guess['description']})! Was I correct?\n"),
                        Image.fromNetworkAddress(akinatorGame.aki.first_guess['absolute_picture_path'])
                    ]
                ))
                akinatorGame.end = True

        if messagePlain in akinatorGame.AkinatorCmd and not akinatorGame.hold:  # start
            akinatorGame.end = False
            akinatorGame.hold = True
            await atri.app.sendGroupMessage(group, MessageChain.create(
                [
                    Plain("Please wait...\n"
                          '''yes or y or 0 for YES
no or n or 1 for NO
i or idk or i dont know or i don't know or 2 for I DON’T KNOW
probably or p or 3 for PROBABLY
probably not or pn or 4 for PROBABLY NOT'''
                          ),
                ]
            ))
            q = akinatorGame.aki.start_game("cn")
            await atri.app.sendGroupMessage(group, MessageChain.create(
                [
                    Plain(q + "\n\t"),
                    Plain(f"{akinatorGame.aki.progression}%")
                ]
            ))
