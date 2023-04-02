# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 2:47 下午
# @Author  : Shiro
# @Site    : 
# @File    : friendEvent.py
# @Software: PyCharm
"""FriendMessage"""
from engine import atri
from karas.box import (
    Yurine,
    Friend,
    MessageChain,
    NewFriendRequestEvent,
    Plain
)

from model.chatBot import ChatBot
from util.db import FriendMessages


friend_db = FriendMessages()


class FriendEvent:
    bot: Yurine

    @staticmethod
    @atri.bot.listen(__doc__)
    async def messageEvent(friend: Friend, message: MessageChain):
        _msg_text = "".join([msg.text.strip() for msg in message.fetch(Plain)]) if message.has(Plain) else ''
        _chain = None
        if message.has(Plain):
            _chat_response = await ChatBot.chat(_msg_text)
            _chain = [Plain(_chat_response["message"] if _chat_response['status'] == 'success' else atri.chatBot['badRequest'])]

        if _chain:
            await atri.bot.sendFriend(friend, _chain)

    @staticmethod
    @atri.bot.listen(NewFriendRequestEvent.type)
    async def newFriendEvent(event: NewFriendRequestEvent):
        """Bot收到请求添加好友事件"""
