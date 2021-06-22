#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 22:54
# @Author  : Shiro
# @File    : Core.py
# @Software: PyCharm
from event import friendEvent, groupEvent, tempEvent, atri


class core:
    @staticmethod
    def run():
        ge: groupEvent.GroupEvent()
        fe: friendEvent.FriendEvent()
        te: tempEvent.TempEvent()
        try:
            atri.app.launch_blocking()
        except KeyboardInterrupt:
            atri.app.logger.info("exit")
