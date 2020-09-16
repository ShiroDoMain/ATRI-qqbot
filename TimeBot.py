import time
from graia.application.entry import (GraiaMiraiApplication, Session, MessageChain, Group, Member, Plain, Image, FlashImage, Quote, Source, Friend)
from graia.broadcast import Broadcast
import asyncio
from PIL import Image as IMG, PSDraw, ImageFont, ImageDraw

GP = [963407871,494453985,1027106983]

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:2333",
        authKey="INITKEY50BuhiTH",
        account=1977987864,
        websocket=True
    )
)

def time_draw(time_now,msg):
    with IMG.open('img/time.jpg') as image:
        img_draw = ImageDraw.Draw(image)
        img_draw.text((0,263), time_now, font=ImageFont.truetype('Font/PUTHIAfont.ttf', 23), fill=(0,0,0))
        i = 0
        for word in msg:
            i += 25
            img_draw.text((87,i),word,font=ImageFont.truetype('Font/HYXinHaiXingKaiW.ttf',25),fill=(0,0,0))
        image.save("img/time_cache.jpg")


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



async def tell_time(bot, message):
    lt = int(time.strftime("%H%M%S", time.localtime(time.time())))
    ht = int(time.strftime("%H", time.localtime(time.time())))
    time_num = int(lt / 10000)
    time_draw(time.strftime("%H:%M", time.localtime(time.time())),ask(ht))
    for ID in GP:
        if time_num == 7:
            v = await bot.uploadVoice(open('www.amr','rb'))
            await bot.sendGroupMessage(ID,message.create([v]))
        await bot.sendGroupMessage(ID, message.create([Image.fromLocalFile(f'img/time_cache.jpg')]))


async def Run(bot, message):
    last_time = time.localtime()
    while True:
        curr_time = time.localtime()
        if curr_time.tm_sec < 50 and curr_time.tm_min < 59 and curr_time.tm_min != 0:
            wait_time = 50 - curr_time.tm_sec
            await asyncio.sleep(wait_time)
        elif curr_time.tm_min == 0 and \
                curr_time.tm_hour != last_time.tm_hour:
            asyncio.ensure_future(tell_time(bot, message))
            last_time = curr_time
            print(time.strftime("Time: %H:%M:%S"))
            await asyncio.sleep(20)


@bcc.receiver('GroupMessage')
async def Time(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if message.asDisplay() == '开启整点报时' and member.id == 1808107177:
        GP.append(group.id)
        await app.sendGroupMessage(group.id, message.create([Plain(text=f'{group.id}已开启整点报时')]))
        task =  asyncio.create_task(Run(app,message))
        await task
    if message.asDisplay() == '关闭整点报时' and member.id == 1808107177:
        GP.remove(group.id)
        await app.sendGroupMessage(group.id, message.create([Plain(text=f'{group.id}已关闭整点报时')]))


if __name__ == '__main__':
    app.launch_blocking()
