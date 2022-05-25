# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 8:32 上午
# @Author  : Shiro
# @Site    :
# @File    : __init__.py.py
# @Software: PyCharm


from typing import Callable, Optional


def cmd(
    text: str,
    command: str,
    func: Callable = None,
    strip: bool = True
) -> Optional[str]:
    if command in text:
        pattern = f"{command}".join(text.split(command)[1:])
        pattern = pattern.strip() if strip else pattern
        if func is not None:
            return func(*pattern)
        return pattern
    return
