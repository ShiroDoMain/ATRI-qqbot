# -*- coding: utf-8 -*-
# @Time : 2020/7/29 5:03 下午
# @Author : shiro
# @Software: PyCharm
import asyncio
import re
import time

from graia.application.entry import (GraiaMiraiApplication, Plain, Session, Source, At, Image,
                                     Group, Member, MessageChain)
from graia.broadcast import Broadcast

from util import translate, ToDay, GetCOVID19Data, weather
from util.AcgImgSearch import IQDB_SEARCH, SAUCENAO_SEARCH, CACHE_IMG, GETASCII2D_FROM_RPI
from util.SendImg import sendstick, stick_cmd
from util.ShaDiao_ana import ana, SendShadiaoAna
from util.StaticText import Text, Strat_Txet, BotChat
from util.translate import language, language_keys
from util.petpet import pet


# 缓存区
Trans_member = {}
Img_search = []
Acg_search = []

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)

qq =  # qq号
authKey =  # mirai-httpapi里设置的authkey
host =  # mirai-http的host:port


app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=host,
        authKey=authKey,
        account=qq,
        websocket=True
    )
)


@bcc.receiver("GroupMessage")
async def group_message_handler(bot: GraiaMiraiApplication, message: MessageChain, group: Group, member: Member):
    # 赶时间，待重构
    if message.asDisplay().endswith(r"天气") and message.asDisplay()[0:3] != "亚托莉":
        start = time.perf_counter()
        c = message.asDisplay()
        await app.sendGroupMessage(
            group.id,
            message.create([
                Plain(text=r"{}".format(weather.weater(c[0: -2])))
            ]
            ))
        end = time.perf_counter() - start
        await app.sendGroupMessage(group.id, message.create([Plain(text='本次查询耗时{:.2f}s'.format(end))]))

    # 怪怪的功能
    if message.asDisplay() in Text.keys():
        if '我是谁' in message.asDisplay() and message.asDisplay() in Text.keys():
            await bot.sendGroupMessage(group.id,
                                       message.create(
                                           [Plain(text=f'{Text["我是谁"] % (member.name, group.name, group.name)}')]),
                                       quote=message[Source][0])
        elif message.asDisplay() == '运行时长':
            await bot.sendGroupMessage(group.id,
                                       message.create([Plain(text=f'目前ATRI已连续运行{int(Text[message.asDisplay()]())}天了,'
                                                                  f'说不定下一秒就该说再见了呢')]),
                                       quote=message[Source][0])
        else:
            await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{Text[message.asDisplay()]}')]),
                                       quote=message[Source][0])
    if message.asDisplay() in stick_cmd:
        await sendstick(bot, group, message[Source][0], message, member.id)
        # await stick_loop
    if message.asDisplay() in ana.keys():
        ShaDiao = asyncio.create_task(SendShadiaoAna(bot, group, message, message[Source][0]))
        await ShaDiao

    # pet摸头
    if message.asDisplay().startswith('摸') and message.has(At):
        await pet(message[At][0].target)
        await app.sendGroupMessage(group, MessageChain.create(
            [Image.fromLocalFile(f'./temp/temp-{message[At][0].target}.gif')]))

    # 闲聊
    if 'ATRI' in message.asDisplay().upper() or '亚托莉' in message.asDisplay():
        if message.asDisplay().startswith('ATRI'):
            if 'ATRI' in message.asDisplay():
                text = re.compile(r'ATRI(.*)').findall(message[Plain][0].text)
            elif '亚托莉' in message.asDisplay():
                text = re.compile(r'亚托莉(.*)').findall(message[Plain][0].text)
            if len(text) == 0:
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text=f'?')]), quote=message[Source][0])
            else:
                await app.sendGroupMessage(group.id, MessageChain.create([Plain(text=f'{BotChat(text[0])}')]),
                                           quote=message[Source][0])
        else:
            await app.sendGroupMessage(group.id, MessageChain.create(
                [Plain(text=f'{BotChat(message.asDisplay().replace("亚托莉" or "ATRI", "你"))}')]),
                                       quote=message[Source][0])


    # 还是闲聊，不过是以at的形式
    if message.has(At) and message[At][0].target == qq:
        if message[Plain][0].text.strip() in Text.keys():
            ...
        elif not message.has(Plain):
            await app.sendGroupMessage(group.id,
                                       MessageChain.create([Plain(text=f'你想说啥?')]),
                                       quote=message[Source][0])

        elif len(message[Plain][0].text) > 1:
            await app.sendGroupMessage(group.id,
                                       MessageChain.create([Plain(text=f'{BotChat(message[Plain][0].text)}')]),
                                       quote=message[Source][0])
        else:
            await app.sendGroupMessage(group.id, MessageChain.create([Plain(text='?')]), quote=message[Source][0])

    if ('取消' in message.asDisplay()) and (member.id in (Img_search or Acg_search)):
        if member.id in Img_search:
            Img_search.remove(member.id)
        elif member.id in Acg_search:
            Acg_search.remove(member.id)

    if '以图搜番' in message.asDisplay() or member.id in Acg_search:
        if message.has(Image):
            await bot.sendGroupMessage(group.id, message.create([Plain(text='图片处理中')]))
            if member.id in Acg_search:
                Acg_search.remove(member.id)
            try:
                result = Strat_Txet['以图搜番'](message.get(Image).url)
            except:
                await bot.sendGroupMessage(group.id, message.create([Plain(text='Not Found')]),
                                           quote=message[Source][0])
            else:
                await bot.sendGroupMessage(group.id, message.create([Plain(
                    text=f'搜索结果\n番剧名:「{result["title_native"]}」\n中文名:《{result["title_chinese"]}》\n英文名:[{result["title_english"]}]')]),
                                           quote=message[Source][0])

        else:
            if member.id not in Acg_search:
                Acg_search.append(member.id)
            await bot.sendGroupMessage(group.id, message.create([Plain(text='发送要搜索的番剧截图')]))

    if '以图搜图' in message.asDisplay() or member.id in Img_search:
        if message.has(Image):
            start_time = time.time()
            if member.id in Img_search:
                Img_search.remove(member.id)
            await bot.sendGroupMessage(group.id, message.create([Plain(text='正在将图片上传到Master服务器\n等待Master服务器响应')]))
            img_url = message.get(Image).url
            await CACHE_IMG(img_url)
            iqdb = await IQDB_SEARCH(open('cache.jpg', 'rb'))
            SaucenNao = await SAUCENAO_SEARCH(open('cache.jpg', 'rb'))
            if iqdb[1] != 404:
                assci = await GETASCII2D_FROM_RPI(iqdb[1])
                await bot.sendGroupMessage(group.id, message.create([
                    Plain(f"{iqdb[0]}\n\n {assci}\n\n{SaucenNao}")]), quote=message[Source][0])
                end_time = time.time() - start_time
                await bot.sendGroupMessage(group.id, message.create([
                    Plain("搜索耗时:%0.1f秒" % end_time)]))
            else:
                await bot.sendGroupMessage(group.id, message.create([
                    Plain(f"{iqdb[0]}\n\n {SaucenNao}")]), quote=message[Source][0])

        else:
            if member.id not in Img_search:
                Img_search.append(member.id)
            await bot.sendGroupMessage(group.id, message.create([Plain(text='请发送要搜索的图片')]))

    # 查询疫情
    if message.asDisplay().startswith('\u67e5\u8be2'):
        # 将消息中的 查询()疫情 提取出来
        City_Find = re.compile(r'\u67e5\u8be2(\S+[^市省])[市省]?\u75ab\u60c5').findall(message.asDisplay())
        if City_Find[0] + '\n' not in GetCOVID19Data.City():
            # 遇到瞎输入或者输入的名称不完整时，提醒
            await bot.sendGroupMessage(group.id,
                                       message.create([Plain(text='数据库中没有此地区(国家(星球))的记录,如果输入的是城市请输入完整城市名,例:查询重庆市疫情')]))
        else:
            # 那就查咯
            await bot.sendGroupMessage(group.id,
                                       message.create([Plain(text=f'{GetCOVID19Data.getData(City_Find[0])}')]))
    if message.asDisplay() == '\u8f9f\u8c23':
        # 从模块那里得到的返回直接发送出去
        await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{GetCOVID19Data.getNews()}')]))

    # 翻译模块
    if "把" and "翻译成" in message.asDisplay():
        await bot.sendGroupMessage(group.id,
                                   message.create([Plain(text=f'{translate.QuickTranslate(message.asDisplay())}')]),
                                   quote=message[Source][0])
    # 重命名TL,排面！
    if message.asDisplay() == 'Stop':
        # 没开始翻译你🐎的翻译
        if member.id not in Trans_member.keys():
            await bot.sendGroupMessage(group.id, message.create([Plain(text='什么?你都没开始怎么结束嘛~')]))
        else:
            del Trans_member[member.id]
            await bot.sendGroupMessage(group.id, message.create([Plain(text='好的，溜了溜了')]))
    elif message.asDisplay().startswith('TL'):
        # 这里对旧思路进行了优化,将user添加进去，顺便带上翻译的语言
        raw_language = re.compile(r'\s(\S+[\u8bed\u6587])\s(\S+[\u8bed\u6587])').findall(message.asDisplay())
        if member.id in Trans_member.keys():
            # 当重复时的处理
            await bot.sendGroupMessage(group.id, message.create([Plain(text='已经开始翻译了，请不要梅开二度(')]))
        elif len(raw_language) == 0:
            pass
        else:
            # 处理消息
            Source_lang = raw_language[0][0]
            target_lang = raw_language[0][1]
            # 如果语言库不匹配的话
            if (Source_lang and target_lang) not in language.keys():
                await bot.sendGroupMessage(group.id, message.create([Plain(text=f'不支持的语言,目前支持的语言有:{language_keys}')]))
            else:
                Trans_member[member.id] = [Source_lang, target_lang]
                await bot.sendGroupMessage(group.id,
                                           message.create([Plain(text=f'开始发送的{Source_lang}翻译成{target_lang}')]))
    # 自行体会
    elif member.id in Trans_member.keys() and message.has(Plain):
        loop = asyncio.create_task(
            translate.send_TL(bot, group, Source, message.asDisplay(), Trans_member[member.id][0],
                              Trans_member[member.id][1]))
        await loop

    # 历史上的今天
    if message.asDisplay() == 'ToDay':
        start = time.perf_counter()
        result = ToDay.Today()
        await bot.sendGroupMessage(group.id, message.create(
            [Plain(text=f'{result}\n本次查询耗时%0.2fs' % (time.perf_counter() - start))]))


if __name__ == '__main__':
    app.launch_blocking()
