# -*- coding: utf-8 -*-
# @Time : 2020/7/29 7:31 下午
# @Author : shiro
# @Software: PyCharm
import requests


def Today(_init=3):
    Text = requests.get(r'http://www.ipip5.com/today/api.php?type=txt').text.split('\n')
    Text.pop()
    Str = ''
    for text in Text:
        Str = Str + text + '\n'
    if len(Text) > 10:
        return str(Str)
    else:
        _init -= 1
        if _init == 0:
            return '数据拉取失败'
        else:
            return Today(_init)

# Test

# start = time.perf_counter()
# result = Today()
# end = time.perf_counter() - start
# print(result, end)
