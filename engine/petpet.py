from PIL import Image as IMG
from PIL import ImageOps
from moviepy.editor import ImageSequenceClip as imageclip
import numpy
import aiohttp
from io import BytesIO
import os


def _checkDir():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")
    if not os.path.exists("./temp/feel"):
        os.mkdir("./temp/feel")


frame_spec = [
    (27, 31, 86, 90),
    (22, 36, 91, 90),
    (18, 41, 95, 90),
    (22, 41, 91, 91),
    (27, 28, 86, 91)
]

squish_factor = [
    (0, 0, 0, 0),
    (-7, 22, 8, 0),
    (-8, 30, 9, 6),
    (-3, 21, 5, 9),
    (0, 0, 0, 0)
]

squish_translation_factor = [0, 20, 34, 21, 0]

frames = tuple([f'./temp/feel/frame{i}.png' for i in range(5)])


async def save_gif(gif_frames, dest, fps=10):
    """生成 gif"""
    clip = imageclip(gif_frames, fps=fps)
    clip.write_gif(dest)
    clip.close()


async def make_frame(avatar, i, squish=0, flip=False):
    """生成帧"""
    spec = list(frame_spec[i])
    # 将位置添加偏移量
    for j, s in enumerate(spec):
        spec[j] = int(s + squish_factor[i][j] * squish)
    # 读取手
    hand = IMG.open(frames[i])
    # 反转
    if flip:
        avatar = ImageOps.mirror(avatar)
    # 将头像放缩成所需大小
    avatar = avatar.resize((int((spec[2] - spec[0]) * 1.2), int((spec[3] - spec[1]) * 1.2)), IMG.ANTIALIAS)
    # 并贴到空图像上
    gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
    gif_frame.paste(avatar, (spec[0], spec[1]))
    # 将手覆盖（包括偏移量）
    gif_frame.paste(hand, (0, int(squish * squish_translation_factor[i])), hand)
    # 返回
    return numpy.array(gif_frame)


async def pet(member_id, flip=False, squish=0, fps=20) -> None:
    """生成最终图像"""

    url = f'http://q1.qlogo.cn/g?b=qq&nk={str(member_id)}&s=640'
    gif_frames = []
    # 打开头像
    # avatar = Image.open(path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            img_content = await resp.read()

    avatar = IMG.open(BytesIO(img_content))
    for i in range(5):
        gif_frames.append(await make_frame(avatar, i, squish=squish, flip=flip))
    await save_gif(gif_frames, f'./temp/temp-{member_id}.gif', fps=fps)


_checkDir()
