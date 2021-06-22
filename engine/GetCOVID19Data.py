# -*- coding: utf-8 -*-
# @Time : 2020/7/30 4:47 下午
# @Author : shiro
# @Software: PyCharm
import requests, random, time


def City():
    with open('util/City.txt') as file:
        return file.read()


def getData(city, _init=3):
    try:
        CityData = requests.get(f'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province={city}').json()['results'][0]
        return f'''地区(国家):{CityData['provinceName']}
现存确诊人数{CityData['currentConfirmedCount']}人
累计确诊人数{CityData['confirmedCount']}人
疑似感染人数{CityData['suspectedCount']}人
治愈人数{CityData['curedCount']}人
死亡人数{CityData['deadCount']}人
数据来源于丁香园(https://www.dxy.cn)
最后统计于{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(CityData["updateTime"] / 1000))}'''
    except:
        _init -= 1
        if _init == 0:
            return '数据拉取失败'
        else:
            return getData(city, _init)


def getNews():
    try:
        fakeNews = \
            requests.get(
                f'https://lab.isaaclin.cn/nCoV/api/rumors?page={random.randrange(1, 2)}&num={random.randrange(100)}').json()[
                'results'][0]
        return f'''标题:{fakeNews['title']}
概述:{fakeNews['mainSummary']}
内容:{fakeNews['body']}'''
    except:
        print('get news fail,retry')
        getNews()
