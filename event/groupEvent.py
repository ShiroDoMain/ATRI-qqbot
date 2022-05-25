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
from typing import Tuple
from karas.box import (
    Yurine,
    MessageChain,
    Member,
    MemberJoinEvent,
    MemberLeaveEventQuit,
    MemberLeaveEventKick,
    MemberMuteEvent,
    BotGroupPermissionChangeEvent,
    MemberPermissionChangeEvent,
    MemberJoinRequestEvent,
    BotInvitedJoinGroupRequestEvent,
    At,
    Plain,
    Group,
    Source,
    Image,
    FlashImage

)
from karas.event import MemberUnmuteEvent

from model.chatBot import ChatBot
from engine import atri
from model import cmd, sticker, acgTools
# from model.akinatorG import akinatorGame
from model.weather import weather


def markov_eval(res: Tuple):
    text, eval_ = res
    if not eval:
        atri.markov.train(text=text)
    return f"√|{text}" if eval_ else f"×|{text}"


class GroupEvent:
    bot: Yurine
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
    chatBot = atri.chatBot['enable']

    quote = any([conversation['quote'], atri.chatBot['quote']])

    onlyGroup = atri.onlyGroup['list'] if atri.onlyGroup['enable'] else False
    shieldGroup = atri.shieldGroup['list'] if atri.shieldGroup['enable'] else []

    @staticmethod
    @atri.bot.listen(__doc__)
    async def messageEvent(message: MessageChain, member: Member, group: Group):
        """群组消息事件"""
        chain = None
        messagePlain = ''.join([msg.text.strip() for msg in message.fetch(Plain)]) if message.has(Plain) else ''
        atMember = [a.target for a in message.fetch(At)] if message.has(At) else []

        if member.id in atri.loadBlackList():
            return
        if GroupEvent.onlyGroup and group.id not in GroupEvent.onlyGroup:
            return
        if group.id in GroupEvent.shieldGroup:
            return

        mk_gen = cmd(message.to_text(),"#mk",atri.markov.gen) # generate markov
        mk_eval = cmd(message.to_text(),"#mke",markov_eval) # eval markov
        cmd(message.to_text(),"#mkt",atri.markov.train) #train markov
        chain = (mk_gen or mk_eval) and [Plain(mk_gen or mk_eval)]

        if GroupEvent.chatBot:
            if message.has(At) and atri.qq in [mb.target for mb in message.fetch(At)] and group.id not in atri.chatBot['shield']:
                response = await GroupEvent.chat.chat(messagePlain)
                if response['status'] == 'success':
                    chain = [Plain(response['message'])]
                else:
                    chain = [Plain(atri.chatBot['badRequest'])]
            elif all([atri.name in messagePlain.lower(), group.id not in atri.chatBot['shield']]):
                response = await GroupEvent.chat.chat(messagePlain)
                if response['status'] == 'success':
                    chain = [Plain(response['message'])]
                else:
                    chain = [Plain(atri.chatBot['badRequest'])]

        if GroupEvent.conv:
            if not GroupEvent._at and messagePlain in GroupEvent.conversation['msg']:
                chain = [Plain(GroupEvent.conversation['msg'][messagePlain])]
            elif GroupEvent._at and atri.qq in atMember:
                chain = [Plain(GroupEvent.conversation['msg'][messagePlain])]
        if GroupEvent.Sticker:
            patten = sticker.sticker(messagePlain)
            if patten:
                chain = [Image(GroupEvent.StickerPath + patten)]

        if GroupEvent.setu.enable and messagePlain in GroupEvent.setu.cmd:
            setu = GroupEvent.setu.randomSetu()
            chain = [
                    Image(setu)
                    if not GroupEvent.setu.flash else
                    FlashImage(setu)
                ]

        if GroupEvent.acgSearch.enable and messagePlain in GroupEvent.acgSearch.cmd:
            if not message.has(Image):
                chain = [Plain('未能在消息中找到图片')]
                
            else:
                urls = [image.url for image in message.fetch(Image)] if message.has(Image) else []
                searchResultSet = await GroupEvent.acgSearch.ascii2d(urls)
                chain = [Plain('特徴検索:\n%s%s色合検索:\n%s' % ('\n'.join(searchResultSet['特徴検索']),
                                                        '=' * 20,
                                                        '\n'.join(searchResultSet['色合検索'])))
                    ]

            GroupEvent.quote = True
        if GroupEvent.animeSearch.enable and messagePlain in GroupEvent.animeSearch.cmd:
            if not message.has(Image):
                chain = [Plain('未能在消息中找到图片')]
                
            else:
                url = message.fetchone(Image).url
                searchResultSet = await GroupEvent.animeSearch.animeSearch(url)
                chain = [Plain(searchResultSet)]

        if atri.weather:
            if message.to_text().endswith(r"天气"):
                if '今日' in message.to_text().strip() or '今天' in message.to_text().strip():
                    city = re.findall(r'(\S{1,5}[^市省]).?今[日天]?天气', message.to_text().strip())
                    model = 'day'
                else:
                    city = re.findall(r'(\S{1,5}[^市省]).?天气', message.to_text().strip())
                    model = ''
                if city:
                    fn = await weather(city[0], model)
                    if fn:
                        chain = [Image(fn)]

        if message.to_text() in ['吃啥', '恰啥', '吃什么', '今晚吃啥', '今晚吃什么', '等会吃什么', '等会吃啥', '来点吃的']:
            chain = [Image('storage/picture/food/%d.png' % random.randrange(13))]

        if chain:
            await atri.bot.sendGroup(group, chain, quote=message.fetchone(Source) if GroupEvent.quote else None)

    @staticmethod
    @atri.bot.listen(__doc__)
    async def commandEvent(message: MessageChain, member: Member):
        """指令事件"""

    @staticmethod
    @atri.bot.listen(MemberJoinEvent.__name__)
    async def joinEvent(event: MemberJoinEvent):
        """加群事件"""

    @staticmethod
    @atri.bot.listen(MemberLeaveEventQuit.__name__)
    async def leaveEvent(event: MemberLeaveEventQuit):
        """退群事件"""

    @staticmethod
    @atri.bot.listen(MemberLeaveEventKick.__name__)
    async def kickEvent(event: MemberLeaveEventKick):
        """群员被踢出群组事件"""

    @staticmethod
    @atri.bot.listen(MemberMuteEvent.__name__)
    async def muteEvent(event: MemberMuteEvent):
        """禁言事件"""

    @staticmethod
    @atri.bot.listen(MemberUnmuteEvent.__name__)
    async def unMuteEvent(event: MemberUnmuteEvent):
        """取消禁言事件"""

    @staticmethod
    @atri.bot.listen(BotGroupPermissionChangeEvent.__name__)
    async def botPermissionChangeEvent(event: BotGroupPermissionChangeEvent):
        """Bot权限被修改事件"""

    @staticmethod
    @atri.bot.listen(MemberPermissionChangeEvent.__name__)
    async def memberPermissionChangeEvent():
        """群员权限被修改事件"""

    @staticmethod
    @atri.bot.listen(MemberJoinRequestEvent.__name__)
    async def joinGroupEvent(event: MemberJoinRequestEvent):
        """Bot为管理员/群主时接受到加群事件"""

    @staticmethod
    @atri.bot.listen(BotInvitedJoinGroupRequestEvent.__name__)
    async def invitedGroupRequestEvent(event: BotInvitedJoinGroupRequestEvent):
        """Bot接受到邀请加群事件"""
