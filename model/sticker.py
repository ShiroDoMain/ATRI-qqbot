#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 21:05
# @Author  : Shiro
# @File    : sticker.py
# @Software: PyCharm
from typing import Optional

from engine import atri


def sticker(patten: str) -> Optional[str]:
    """
    匹配对应的Sticker
    :param patten: 匹配对象
    :return: 匹配成功后返回对应的sticker
    """
    stickers = atri.loadSticker()
    stickerList = [s.group(1) for s in stickers]
    if patten in stickerList:
        return stickers[stickerList.index(patten)].group(0)
    return None
