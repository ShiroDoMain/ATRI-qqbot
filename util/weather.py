# -*- coding: utf-8 -*-
# @Time : 2020/3/9 12:34 下午
# @Author : shiro
# @Software: PyCharm
from urllib import request
import re
from util import cs


def weater(name):
    if cs.city(name) == 0:
        return '{}查询失败'.format(name)
    else:
        url = 'http://www.weather.com.cn/weather/{}.shtml'.format(cs.city(name))
        req = request.Request(url)
        weekly_weather = request.urlopen(req).read().decode('utf-8')
        seven_days = re.findall(r'\<h1\>([1-9].*)\</h1>\n.*\n.*\n.*\>(.*)\</p>\n.*\n\<span\>([0-9]*).*\>(['
                                r'0-9].*)\</i\>\n',
                                weekly_weather)
        # with open('wt.txt','a+') as file:
        #     file.writelines(weekly_weather)
        # print(weekly_weather)
        # print(seven_days)
        return '''
=====================
%s近几日天气
---------------------
%s |%s
最高温度%s°C|最低温度%s
---------------------
%s |%s
最高温度%s°C|最低温度%s
---------------------
%s |%s
最高温度%s°C|最低温度%s
---------------------
%s |%s
最高温度%s°C|最低温度%s
---------------------
%s |%s
最高温度%s°C|最低温度%s
---------------------
        ''' % (name, seven_days[0][0], seven_days[0][1], seven_days[0][2], seven_days[0][3],
               seven_days[1][0], seven_days[1][1], seven_days[1][2], seven_days[1][3],
               seven_days[2][0], seven_days[2][1], seven_days[2][2], seven_days[2][3],
               seven_days[3][0], seven_days[3][1], seven_days[3][2], seven_days[3][3],
               seven_days[4][0], seven_days[4][1], seven_days[4][2], seven_days[4][3])
        # for day in seven_days:
        #     tq = [day[0], day[1], day[2], day[3], '\n']
        # return tq
        # return '近三天天气',seven_days[0: 3]


# print(weater('重庆'))
