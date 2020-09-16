# -*- coding: utf-8 -*-
# @Time : 2020/8/7 1:07 下午
# @Author : shiro
# @Software: PyCharm
import asyncio
import hashlib, re, requests

import aiohttp
import saucenao_api


async def CACHE_IMG(url):
    async with aiohttp.request("GET", url) as file:
        data = await file.read()
        with open("cache.jpg", "wb+") as f:
            f.write(data)


async def IQDB_SEARCH(file):
    form = (
        ('file', file),
        ('MAX_FILE_SIZE', '8388608'),
        ('service[]', '1'),
        ('service[]', '2'),
        ('service[]', '3'),
        ('service[]', '4'),
        ('service[]', '5'),
        ('service[]', '6'),
        ('service[]', '11'),
        ('service[]', '13')
    )
    try:
        results = await aiohttp.ClientSession().post(url='https://iqdb.org/', data=form)
        body = await results.text()
        image_url = body.split('https://ascii2d.net/search/url/')[1].split('">')[0]
    except:
        return 'IQDB匹配时发生了无法预知的错误,请重试', 404
    else:
        if 'No relevant matches' not in body:
            result = re.compile(r'<th>(.*)</th>.*"(.*)"><i.*(\d..*%)').findall(body)
            return '来自IQDB的最佳匹配:https:%s\n匹配相似度:%s' % (result[0][1], result[0][2]), image_url
        elif 'No relevant matches' in body:
            return 'IQDB没有匹配到,重定向ASCII2D', image_url
        else:
            return 'IQDB匹配异常,重定向ASCII2D', image_url


# async def ASCII2D_URL_SEARCH(image_url):
#     try:
#         body = requests.get('https://ascii2d.net/search/url/%s' % image_url).text
#         open('cache.txt', 'w').write(body)
#         img_hash = body.split("<div class='hash'>")[1].split('<')[0]
#         img_search = re.compile(r'<h6>\n.*\n.*"(.*)">(.*)</a>\n.*"(.*)">(.*)</a>\n.*\n(.*)').findall(body)
#     except:
#         return '目前ASCII2D匹配异常,待重构解决',404
#     if '失敗' not in body:
#         return '来自ASCII2D的搜索结果:\n结果1:\n画像链接:%s\n画像标题:%s\n画师链接:%s\n画师ID:%s\n出处:%s\n' \
#                '结果2:\n画像链接:%s\n画像标题:%s\n画师链接:%s\n画师ID:%s\n出处:%s' % (
#                    img_search[0][0], img_search[0][1], img_search[0][2], img_search[0][3], img_search[0][4],
#                    img_search[1][0], img_search[1][1], img_search[1][2], img_search[1][3], img_search[1][4]), img_hash
#     elif '失敗' in body:
#         return 'ASCII2D未能搜索到,重定向ASCII2D特征匹配和颜色匹配', img_hash
#     else:
#         return 'ASCII2D匹配异常,重定向ASCII2D特征匹配和颜色匹配', img_hash
#
#
# async def ASCII2D_COLOR_SEARCH(md5):
#     try:
#         result = re.compile(r'<h6>\n.*\n.*"(.*)">(.*)</a>\n.*"(.*)">(.*)</a>\n.*\n(.*)').findall(
#             requests.get('https://ascii2d.net/search/color/%s' % md5).text)[0]
#     except:
#         return '颜色匹配没有找到,重定向SAUCENAO'
#     else:
#         return '''来自ASCII2D的色合検索:\n画像链接:%s\n画像ID:%s\n画师链接:%s\n画师ID:%s''' % (
#             result[0], result[1], result[2], result[3])
#
#
# async def ASCII2D_BOVW_SEARCH(md5):
#     try:
#         result = re.compile(r'<h6>\n.*\n.*"(.*)">(.*)</a>\n.*"(.*)">(.*)</a>\n.*\n(.*)').findall(
#             requests.get('https://ascii2d.net/search/bovw/%s' % md5).text)[0]
#
#     except:
#         return '特征匹配没有找到,重定向SAUCENAO'
#     else:
#         return '''来自ASCII2D的特徴検索:\n画像链接:%s\n画像ID:%s\n画师链接:%s\n画师ID:%s''' % (
#             result[0], result[1], result[2], result[3])


async def SAUCENAO_SEARCH(file):
    try:
        results = saucenao_api.SauceNao().from_file(file)
    except:
        return 'SAUCENAO搜索失败'
    else:
        return '''来自SAUCENAO的搜索:\n结果1:%s\n标题:%s\n画师:%s\n链接:%s\n结果2:\n标题:%s\n画师:%s\n链接:%s''' % (
            len(results), results[0].title, results[0].author, results[0].url, results[1].title, results[1].author,
            results[1].url)


async def GETASCII2D_FROM_RPI(url):
    try:
        reader, writer = await asyncio.open_connection(
            'localhost', 10808)
        print(f'Send: {url}')
        writer.write(url.encode())
        data = await reader.read()
        print('Close the connection')
        writer.close()
    except:
        return 'Master服务器断开'
    else:
        return data.decode()


# async def main():
#     result = await GETASCII2D_FROM_RPI('https://i.pximg.net/img-original/img/2020/08/07/17/02/32/83504544_p0.png')
#     print(result)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())


