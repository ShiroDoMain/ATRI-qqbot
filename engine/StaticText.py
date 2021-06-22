# -*- coding: utf-8 -*-
# @Time : 2020/7/30 8:28 上午
# @Author : shiro
# @Software: PyCharm
import qqai
import requests
import time
from engine import atri


def getAcgList():
    url = 'https://bangumi.bilibili.com/api/timeline_v2_global'
    r = requests.get(url).json()
    result = r['result']
    return '''--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------
番剧名称:%s 
地区:%s
更新时间:%s
--------------------------''' % (result[0]['title'], result[0]['area'], result[0]['lastupdate_at'],
                                 result[1]['title'], result[1]['area'], result[1]['lastupdate_at'],
                                 result[2]['title'], result[2]['area'], result[2]['lastupdate_at'],
                                 result[3]['title'], result[3]['area'], result[3]['lastupdate_at'],
                                 result[4]['title'], result[4]['area'], result[4]['lastupdate_at'],
                                 result[5]['title'], result[5]['area'], result[5]['lastupdate_at'],
                                 result[6]['title'], result[6]['area'], result[6]['lastupdate_at'])


Text = {
    "功能列表": 'ATRIbot使用方法：\n'
            '1:发送 [地方名]天气 获取当地天气;\n'
            '2:发送 TL [源语言](例:中文) [目标语言](英语),开始将发送的消息翻译成目标语言,'
            '发送Stop停止翻译.\n'
            'PS: 亦可发送 把xxxx翻译成英语(中文 or other) 快速翻译\n'
            '3：■■■■■■■■■■■■■■■■■■■■；\n'
            '4:发送 查询xx(地方名)疫情 可以获取当地疫情情况\n'
            '5:发送[报时]可以发送当前时间\n'
            '6:发送 ATRI[or艾特](要说的话)，例如 ATRI你今天穿的什么颜色的胖次进行情景对话\n'
            '7.发送[每日番剧]获取当日番剧更新列表\n'
            '8.发送[ToDay]返回当天在历史上发生的重要事件(几率返回None)\n'
            '9.发送 以图搜番[图片] 尝试以图片搜索番剧\n'
            '10.发送 以图搜图[图片] 尝试以图片搜索原图出处和地址链接\n'
            'NOTE:另外还有些顺手添加的小功能(舔狗语录，鸡汤等等)'
            '     # 毕竟我是高性能的嘛\n',
    '我是谁': '你名叫%s。住在%s的別墅區一帶，未婚。你在%s摸鱼。每天都要划水到晚上8點才能回家。你不抽煙，酒僅止於淺嘗。晚上11點摸鱼，每天要摸鱼足8個小時。摸鱼前，你一定喝一杯溫牛奶，然後做20'
           '分鐘的柔軟操，上了床，馬上摸鱼。摸鱼到天亮，早上起來就像嬰兒一樣不帶任何疲勞和壓力迎接第二天。醫生都說你沒有任何異常。你在向我說明你是一直希望保持內心平靜生活的人，'
           '不執著於勝負，不糾結於煩惱，不樹立讓你夜不能摸的敵人，這就是你對社會的態度，也知道這是你的幸福。不過就算打起來你也不會輸給任何人就是了。',
    '你是谁': '高性能吃饭机器人',
    '运行时长': lambda: ((time.time() - 1589000279) / 86400),
    '每日番剧': getAcgList(),
    '不够涩': '那你发啊kora！'
}

Strat_Txet = {
    '以图搜番': lambda url: requests.get('https://trace.moe/api/search?url=%s' % url).json()['docs'][0],
}


def BotChat(msg, _init=3):
    result = qqai.TextChat(atri.qqaiAppid, atri.qqaiKey).ask(msg)
    print(result)
    if result.isspace():
        if _init == 0:
            return '今天吃啥？'
        else:
            _init -= 1
            return BotChat(msg, _init)
    else:
        return result


end_cache = 'bot'
End_Text = {
    'bot': '诶？？？？？'
}
