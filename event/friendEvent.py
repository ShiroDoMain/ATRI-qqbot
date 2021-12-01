# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 2:47 下午
# @Author  : Shiro
# @Site    : 
# @File    : friendEvent.py
# @Software: PyCharm
"""FriendMessage"""
from engine import atri
from graia.application.entry import (
    Friend,
    GraiaMiraiApplication,
    MessageChain,
    NewFriendRequestEvent,
    Plain
)
from graia.broadcast import Broadcast
from model.chatBot import ChatBot


class FriendEvent:
    app: GraiaMiraiApplication
    bcc: Broadcast

    @staticmethod
    @atri.bcc.receiver(__doc__)
    async def messageEvent(friend: Friend, message: MessageChain):
        _msg_text = "".join([msg.text.strip() for msg in message[Plain]]) if message.has(Plain) else ''
        if message.has(Plain):
            _chat_response = await ChatBot.chat(_msg_text)
            _chain = MessageChain.create(
                [
                    Plain(_chat_response["message"] if _chat_response['status'] == 'success' else atri.chatBot['badRequest'])
                ]
            )

        if _chain:
            await atri.app.sendFriendMessage(friend, _chain)

    @staticmethod
    @atri.bcc.receiver(NewFriendRequestEvent.type)
    async def newFriendEvent(event: NewFriendRequestEvent):
        """Bot收到请求添加好友事件"""
