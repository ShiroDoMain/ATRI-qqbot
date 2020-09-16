# -*- coding: utf-8 -*-
# @Time : 2020/7/29 7:31 下午
# @Author : shiro
# @Software: PyCharm
import requests, time


def Today():
    Text = requests.get(r'http://www.ipip5.com/today/api.php?type=txt').text.split('\n')
    # 把最后那个不顺眼的干掉，别问，干掉就完事了
    Text.pop()
    Str = ''
    for text in Text:
        Str = Str + text + '\n'
    if Str is not None and (len(Text) > 10):
        # 即使新加了判定还是会偶尔返回None？smjb鬼玩意，傻逼py
        return str(Str)
    else:
        # 没错，递归，优雅就vans了
        Today()


# Test

# start = time.perf_counter()
# result = Today()
# end = time.perf_counter() - start
# print(result, end)



