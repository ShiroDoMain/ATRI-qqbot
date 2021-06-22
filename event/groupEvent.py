# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 9:42 上午
# @Author  : Shiro
# @Site    : 
# @File    : groupEvent.py
# @Software: PyCharm
"""GroupMessage"""
from engine import atri
from graia.application.entry import *
from graia.broadcast import Broadcast


class GroupEvent:
    bcc: Broadcast
    app: GraiaMiraiApplication

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def messageEvent(message: MessageChain, member: Member, ):
        """群组消息事件"""
        pass

    @staticmethod
    @atri.bcc.receiver(MemberJoinEvent.__name__)
    async def joinEvent(event: MemberJoinEvent):
        """加群事件"""
        pass

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
    async def joinGroupEvent(event:MemberJoinRequestEvent):
        """Bot为管理员/群主时接受到加群事件"""

    @staticmethod
    @atri.bcc.receiver(BotInvitedJoinGroupRequestEvent.__name__)
    async def invitedGroupRequestEvent(event: BotInvitedJoinGroupRequestEvent):
        """Bot接受到邀请加群事件"""
