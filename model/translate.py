# -*- coding: utf-8 -*-
# @Time : 2020/7/29 3:59 下午
# @Author : shiro
# @Software: PyCharm
import qqai
import re
from graia.application.entry import Plain
from engine import atri

language = {
    '汉语': 'zh',
    '英语': 'en',
    '日语': 'jp',
    '韩语': 'kr',
    '法语': 'fr',
    '德语': 'de',
    '俄语': 'ru',
    '泰语': 'th',
    '马来西亚语': 'ms',
    '西班牙语': 'es',
    '意大利语': 'it',
    '土耳其语': 'tr',
    '葡萄牙语': 'pt',
    '越南语': 'vi',
    '印度尼西亚语': 'id',
    # 文和语分开，为了照顾某些杠精我真是操碎了心
    '中文': 'zh',
    '英文': 'en',
    '日文': 'jp',
    '韩文': 'kr',
    '法文': 'fr',
    '德文': 'de',
    '俄文': 'ru',
    '泰文': 'th',
    # 新增语言(只是之前懒得加，但是这样似乎Trans会出问题，待重构
    '马来西亚文': 'ms',
    '西班牙文': 'es',
    '意大利文': 'it',
    '土耳其文': 'tr',
    '葡萄牙文': 'pt',
    '越南文': 'vi',
    '印度尼西亚文': 'id'

}
language_keys = '汉语 英语 日语 韩语 法语 德语 俄语 泰语 马来西亚语 西班牙语 意大利语 土耳其语 葡萄牙语 越南语 印度尼西亚语'


# 已废弃，使用lambda代替
def Trans(msg, source, target):
    # 说干就干，重构！
    # 拿到数据
    # 然后交给无情的翻译机器人进行翻译
    # 就这？就这就这就这？
    # return qqai.NLPTrans(appid, key, source=f'{language[source]}', target=f'{language[target]}').run(msg)['data']
    # 发送的事情就交给你了！main！
    pass


async def send_TL(bot, group, source, msg, source_text, target_text):
    TransLate_lang = lambda: \
        qqai.NLPTrans(atri.qqaiAppid,atri.qqaiKey, source=f'{language[source_text]}', target=f'{language[target_text]}').run(msg)[
            'data']  # Trans(msg,source_text,target_text)
    await bot.sendGroupMessage(
        group.id,
        [
            Plain(text=f'{TransLate_lang()["target_text"]}')
        ], quoteSource=source
    )


def QuickTranslate(msg):
    try:
        # 对原始message进行了处理
        raw_language = re.compile(r"把(.*)翻译成(.*[\u8bed\u6587])").findall(msg)
        # 取出了要翻译的语言和目标语言
        trans_language = raw_language[0][0]
        target_language = language[raw_language[0][1].strip()]
        # 对翻译语言判定是属于什么语言
        if target_language not in language.values():
            return f"不支持的语言,目前支持的语言有{language_keys}"
        source_language = qqai.nlp.translate.TextDetect(atri.qqaiAppid, atri.qqaiKey).run(trans_language)['data']['lang']
        # 得到翻译结果
        result = qqai.NLPTrans(atri.qqaiAppid, atri.qqaiKey, source_language, target_language).run(trans_language)['data']['target_text']
        return result
    except:
        return '发生了无法预知的错误'

