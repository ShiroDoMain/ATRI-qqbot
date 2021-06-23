# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:42 上午
# @Author  : Shiro
# @Site    :
# @File    : groupEvent.py
# @Software: PyCharm
"""GroupMessage"""
import json

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

from engine import atri
from model import sticker, acgTools


class GroupEvent:
    bcc: Broadcast
    app: GraiaMiraiApplication
    setu = acgTools.SetuTime()
    with open('interaction.json', 'r') as c:
        conversation = json.load(c)
    conversation = conversation['conversation']
    conv = conversation['enable']
    _at = conversation['at']
    quote = conversation['quote']
    Sticker = atri.sticker["enable"]
    StickerPath = atri.sticker['path']
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
        messagePlain = message.get(Plain)[0].text.strip() if message.has(Plain) else None
        atMember = [a.target for a in message.get(At)] if message.has(At) else []

        if member.id in atri.loadBlackList():
            return
        if GroupEvent.onlyGroup and group.id not in GroupEvent.onlyGroup:
            return
        if group.id in GroupEvent.shieldGroup:
            return

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
            print(setu)
            chain = MessageChain.create(
                [
                    Image.fromLocalFile(setu)
                    if not GroupEvent.setu.flash else
                    Image.fromLocalFile(setu).asFlash()
                ]
            )

        if chain:
            await atri.app.sendGroupMessage(group, chain, quote=message.get(Source)[0] if GroupEvent.quote else None)

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
