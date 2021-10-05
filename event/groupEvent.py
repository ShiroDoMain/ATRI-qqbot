# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:42 上午
# @Author  : Shiro
# @Site    :
# @File    : groupEvent.py
# @Software: PyCharm
"""GroupMessage"""
import json
import random
import re

from graia.application.entry import (
    GraiaMiraiApplication,
    MessageChain,
    Member,
    MemberJoinEvent,
    MemberLeaveEventQuit,
    MemberLeaveEventKick,
    MemberMuteEvent,
    MemberUnmuteEvent,
    BotGroupPermissionChangeEvent,
    MemberPermissionChangeEvent,
    MemberJoinRequestEvent,
    BotInvitedJoinGroupRequestEvent,
    At,
    Plain,
    Group,
    Source,
    Image

)
from graia.broadcast import Broadcast
from model.chatBot import ChatBot
from engine import atri
from model import sticker, acgTools
# from model.akinatorG import akinatorGame
from model.weather import weather


class GroupEvent:
    bcc: Broadcast
    app: GraiaMiraiApplication
    chat = ChatBot()
    setu = acgTools.SetuTime()
    acgSearch = acgTools.AcgSearch()
    animeSearch = acgTools.AnimeSearch()
    with open('interaction.json', 'r') as c:
        conversation = json.load(c)
    conversation = conversation['conversation']
    conv = conversation['enable']
    _at = conversation['at']

    Sticker = atri.sticker["enable"]
    StickerPath = atri.sticker['path']
    Akinator = atri.Akinator["enable"]
    chatBot = atri.chatBot['enable']

    quote = any([conversation['quote'], atri.chatBot['quote']])

    onlyGroup = atri.onlyGroup['list'] if atri.onlyGroup['enable'] else False
    shieldGroup = atri.shieldGroup['list'] if atri.shieldGroup['enable'] else []

    @staticmethod
    def chainBuild(elements: list) -> MessageChain:
        """构建消息链"""
        return MessageChain.create(elements)

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def messageEvent(message: MessageChain, member: Member, group: Group):
        """群组消息事件"""
        chain = None
        messagePlain = ''.join([msg.text.strip() for msg in message[Plain]]) if message.has(Plain) else None
        atMember = [a.target for a in message.get(At)] if message.has(At) else []

        if member.id in atri.loadBlackList():
            return
        if GroupEvent.onlyGroup and group.id not in GroupEvent.onlyGroup:
            return
        if group.id in GroupEvent.shieldGroup:
            return

        if GroupEvent.chatBot:
            if all([message.has(At), atri.qq in [mb.target for mb in message[At]],group.id not in atri.chatBot['shield']]):
                response = await GroupEvent.chat.chat(messagePlain)
                if response['status'] == 'success':
                    chain = GroupEvent.chainBuild([Plain(response['message'])])
                else:
                    chain = GroupEvent.chainBuild([Plain(atri.chatBot['badRequest'])])
            elif all([atri.name in messagePlain.lower(), group.id not in atri.chatBot['shield']]):
                response = await GroupEvent.chat.chat(messagePlain)
                if response['status'] == 'success':
                    chain = GroupEvent.chainBuild([Plain(response['msg'])])
                else:
                    chain = GroupEvent.chainBuild([Plain(atri.chatBot['badRequest'])])

        # if GroupEvent.Akinator:
        #     await akinatorGame.process(messagePlain,group,member)

        if GroupEvent.conv:
            if not GroupEvent._at and messagePlain in GroupEvent.conversation['msg']:
                chain = GroupEvent.chainBuild(
                    [
                        Plain(GroupEvent.conversation['msg'][messagePlain])
                    ]
                )
            elif GroupEvent._at and atri.qq in atMember:
                chain = MessageChain.create(
                    [
                        Plain(GroupEvent.conversation['msg'][messagePlain])
                    ]
                )
        if GroupEvent.Sticker:
            patten = sticker.sticker(messagePlain)
            if patten:
                chain = MessageChain.create(
                    [Image.fromLocalFile(GroupEvent.StickerPath + patten)]
                )
        if GroupEvent.setu.enable and messagePlain in GroupEvent.setu.cmd:
            setu = GroupEvent.setu.randomSetu()
            chain = MessageChain.create(
                [
                    Image.fromLocalFile(setu)
                    if not GroupEvent.setu.flash else
                    Image.fromLocalFile(setu).asFlash()
                ]
            )
        if GroupEvent.acgSearch.enable and messagePlain in GroupEvent.acgSearch.cmd:
            if not message.has(Image):
                chain = MessageChain.create(
                    [
                        Plain('未能在消息中找到图片')
                    ]
                )
            else:
                urls = [image.url for image in message[Image]] if message.has(Image) else []
                searchResultSet = await GroupEvent.acgSearch.ascii2d(urls)
                chain = MessageChain.create(
                    [
                        Plain('特徴検索:\n%s%s色合検索:\n%s' % ('\n'.join(searchResultSet['特徴検索']),
                                                        '=' * 20,
                                                        '\n'.join(searchResultSet['色合検索'])))
                    ]
                )
            GroupEvent.quote = True
        if GroupEvent.animeSearch.enable and messagePlain in GroupEvent.animeSearch.cmd:
            if not message.has(Image):
                chain = MessageChain.create(
                    [
                        Plain('未能在消息中找到图片')
                    ]
                )
            else:
                url = message[Image][0].url
                searchResultSet = await GroupEvent.animeSearch.animeSearch(url)
                chain = MessageChain.create(
                    [
                        Plain(searchResultSet)
                    ]
                )

        if atri.weather:
            if message.asDisplay().endswith(r"天气"):
                if '今日' in message.asDisplay().strip() or '今天' in message.asDisplay().strip():
                    city = re.findall(r'(\S{1,5}[^市省]).?今[日天]?天气', message.asDisplay().strip())
                    model = 'day'
                else:
                    city = re.findall(r'(\S{1,5}[^市省]).?天气', message.asDisplay().strip())
                    model = ''
                if city:
                    fn = await weather(city[0], model)
                    if fn:
                        chain = MessageChain.create([Image.fromLocalFile(fn)])

        if message.asDisplay() in ['吃啥', '恰啥', '吃什么', '今晚吃啥', '今晚吃什么', '等会吃什么', '等会吃啥', '来点吃的']:
            chain = MessageChain.create([Image.fromLocalFile('img/sticker/food/%d.png' % random.randrange(13))])

        if chain:
            await atri.app.sendGroupMessage(group, chain, quote=message[Source][0] if GroupEvent.quote else None)

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def commandEvent(message: MessageChain, member: Member):
        """指令事件"""

    @staticmethod
    @atri.bcc.receiver(MemberJoinEvent.__name__)
    async def joinEvent(event: MemberJoinEvent):
        """加群事件"""

    @staticmethod
    @atri.bcc.receiver(MemberLeaveEventQuit.__name__)
    async def leaveEvent(event: MemberLeaveEventQuit):
        """退群事件"""

    @staticmethod
    @atri.bcc.receiver(MemberLeaveEventKick.__name__)
    async def kickEvent(event: MemberLeaveEventKick):
        """群员被踢出群组事件"""

    @staticmethod
    @atri.bcc.receiver(MemberMuteEvent.__name__)
    async def muteEvent(event: MemberMuteEvent):
        """禁言事件"""

    @staticmethod
    @atri.bcc.receiver(MemberUnmuteEvent.__name__)
    async def unMuteEvent(event: MemberUnmuteEvent):
        """取消禁言事件"""

    @staticmethod
    @atri.bcc.receiver(BotGroupPermissionChangeEvent.__name__)
    async def botPermissionChangeEvent(event: BotGroupPermissionChangeEvent):
        """Bot权限被修改事件"""

    @staticmethod
    @atri.bcc.receiver(MemberPermissionChangeEvent.__name__)
    async def memberPermissionChangeEvent():
        """群员权限被修改事件"""

    @staticmethod
    @atri.bcc.receiver(MemberJoinRequestEvent.__name__)
    async def joinGroupEvent(event: MemberJoinRequestEvent):
        """Bot为管理员/群主时接受到加群事件"""

    @staticmethod
    @atri.bcc.receiver(BotInvitedJoinGroupRequestEvent.__name__)
    async def invitedGroupRequestEvent(event: BotInvitedJoinGroupRequestEvent):
        """Bot接受到邀请加群事件"""
