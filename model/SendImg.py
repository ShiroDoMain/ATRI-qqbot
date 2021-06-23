# -*- coding: utf-8 -*-
# @Time : 2020/7/30 9:11 上午
# @Author : shiro
# @Software: PyCharm
import os
import random
import time

from PIL import ImageFont, Image as img, ImageDraw
from graia.application.entry import (Plain, Image)

from engine import atri

stick_name = {
    '爬': '爬.gif',
    '你好ATRI': '啊？.jpg',
    '随机涩图': lambda: os.listdir(atri.cfg["setuPath"])[
        random.randrange(len(os.listdir(atri.cfg["setuPath"])) - 1)],
}
stick_cmd = ['报时', '爬', '你好ATRI', '随机涩图', '贴贴']
SendImgCount = {

}


def draw_text_img(now_time, ask):
    with img.open('picture/time.jpg') as image:
        img_draw = ImageDraw.Draw(image)
        time_font = ImageFont.truetype('Font/PUTHIAfont.ttf', 23)
        word_font = ImageFont.truetype('Font/HYXinHaiXingKaiW.ttf', 25)
        img_draw.text((0, 263), now_time, font=time_font, fill=(0, 0, 0))
        i = 0
        for word in ask:
            i += 25
            img_draw.text((87, i), word, font=word_font, fill=(0, 0, 0))
        image.save("picture/time_cache.jpg")


# 报时消息
def ask(time):
    if time in range(0, 6):
        return '我睡着了!'
    elif time in range(6, 7):
        return '快点起床!'
    elif time in range(7, 8):
        return '快恰早饭!'
    elif time in range(8, 11):
        return '滚去学习!'
    elif time in range(11, 12):
        return '去恰午饭!'
    elif time in range(12, 13):
        return '去睡午觉!'
    elif time in range(13, 16):
        return '快去学习!'
    elif time in range(16, 18):
        return '去吃晚饭!'
    elif time in range(18, 22):
        return '快点上号!'
    elif time in range(22, 25):
        return '滚去睡觉！'


# 添加发送图片
async def sendstick(bot, group, source, msg_par, id=None):
    # 这该死的路径居然是取的main的路径，草了
    if msg_par.asDisplay() == "报时":
        time_24 = time.strftime("%H:%M", time.localtime(time.time()))
        send_ask = ask(int(time.strftime("%H", time.localtime(time.time()))))
        draw_text_img(time_24, send_ask)

        await bot.sendGroupMessage(group, msg_par.create([
            Image.fromLocalFile('picture/time_cache.jpg'),
            Plain(text=f'\n现在是北京时间=>{time.strftime("%H点%M分%S秒", time.localtime(time.time()))}')]), quote=source)
    elif msg_par.asDisplay() == '随机涩图':
        # TODO ：偶尔会出现index out，等以后学会py了再修复,下 次 一 定
        # 别问，问就是lambda真好
        # 判定次数
        if id not in SendImgCount.keys():
            # 初次直接发送然后添加
            SendImgCount[id] = []
            SendImgCount[id].append(1)
            imgname = stick_name['随机涩图']()
            await bot.sendGroupMessage(group.id,
                                       msg_par.create([Image.fromLocalFile(f'{atri.cfg["setuPath"]}/%s' % imgname).asFlash()]))
            await bot.sendGroupMessage(group.id, msg_par.create(
                [Plain('图片链接:https://www.pixiv.net/artworks/%s' % imgname[0:-7])]))

        elif SendImgCount[id][0] < 3 and len(SendImgCount[id]) == 1:
            # 如果次数少于三次
            SendImgCount[id][0] += 1
            imgname = stick_name['随机涩图']()
            await bot.sendGroupMessage(group.id, msg_par.create([
                # 发！
                Image.fromLocalFile(f'{atri.cfg["setuPath"]}/%s' % imgname).asFlash()]))

            await bot.sendGroupMessage(group.id, msg_par.create(
                [Plain('图片链接:https://www.pixiv.net/artworks/%s' % imgname[0:-7])]))

            # 记一次
        elif len(SendImgCount[id]) == 1 and SendImgCount[id][0] >= 3:
            # 如果超过三次就加上时间
            SendImgCount[id].append(time.time())
            await bot.sendGroupMessage(group.id, msg_par.create([Plain(text='做人不要太贪心哦，每获取三次需要等待一分钟')]))
        else:
            # 在这里提醒冲过头了
            if int(time.time() - SendImgCount[id][1]) < 60:
                await bot.sendGroupMessage(group.id,
                                           msg_par.create([Plain(
                                               text='才过去%0.1fs呢' % int(abs(SendImgCount[id][1] - time.time())))]))
            else:
                del SendImgCount[id]
    elif msg_par.asDisplay() == '贴贴':
        i = random.randrange(0, 2)
        if i:
            await bot.sendGroupMessage(group, msg_par.create([Image.fromLocalFile('picture/yes.jpg')]))
        else:
            await bot.sendGroupMessage(group, msg_par.create([Image.fromLocalFile('picture/no.jpg')]))
    else:  # msg_par.asDisplay() in stick_name.keys() and msg_par.asDisplay() != '随机涩图':
        await bot.sendGroupMessage(group.id, msg_par.create([Image.fromLocalFile(f'picture/%s' % stick_name[msg_par.asDisplay()])]))
print(stick_name['你好ATRI'])

