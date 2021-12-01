# -*- coding: utf-8 -*-
# @Time    : 2021/6/23 8:38 上午
# @Author  : Shiro
# @File    : acgTools.py
# @Software: PyCharm
import asyncio
import os
import random
import re
from typing import Union

import aiohttp
from aiohttp import ClientSession
from typing.io import IO

from engine import atri

setu = atri.setu
search = atri.illustrationSearch


class SetuTime:
    path = setu['path']
    enable = setu['enable']
    cmd = setu['command']
    flash = setu['flash']

    @classmethod
    def _loadSetu(cls):
        return os.listdir(atri.setu['path'])

    @classmethod
    def randomSetu(cls):
        setuList = cls._loadSetu()
        s = setuList[random.randrange(len(setuList)) - 1]
        return cls.path + s


class AcgSearch:
    enable = search['enable']
    cmd = search['command']

    @classmethod
    async def _IQDB(cls, fp):
        dataForm = (
            ('file', fp),
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
        async with ClientSession().post(
                url="https://iqdb.org/",
                data=dataForm
        ) as response:
            if response.status != 200:
                return
            body = await response.text()
        if 'No relevant matches' not in body:
            result = re.compile(r'<th>(.*)</th>.*"(.*)"><i.*(\d..*%)').findall(body)
            return '匹配:https:%s\n相似度:%s' % (result[0][1], result[0][2])
        else:
            return

    @classmethod
    async def ascii2d(
            cls,
            urls: Union[list, str] = None,
            file: IO = None,
            _loop=None
    ):
        """
        ascii2d的以图搜图
        :param urls: 列表或者单个图片链接
        :param file: 列表或者单个图片文件
        :param _loop:
        :return:
        """
        BASE = 'http://ascii2d.nekomimi.icu'
        searchResult = {
            '色合検索': [],
            '特徴検索': []
        }

        async def _process(Resultset: list):
            return '画像链接:%s\n画像标题:%s\n画师链接:%s\n画师ID:%s\n出处:%s\n' % (
                Resultset[0][0],
                Resultset[0][1],
                Resultset[0][2],
                Resultset[0][3],
                Resultset[0][4]
            )

        client = aiohttp.ClientSession()
        if _loop:
            asyncio.set_event_loop(_loop)
        for _url in urls:
            try:
                pattern = r'<h6>\n.*\n.*"(.*)">(.*)</a>\n.*"(.*)">(.*)</a>\n.*>(.*)<'
                colorSearchUrl = BASE + '/search/url/' + _url
                colorSearch = await client.get(colorSearchUrl)
                if colorSearch.status != 200:
                    break
                colorSearchResult = await colorSearch.text()
                colorSearchResultSet = await _process(re.compile(pattern=pattern).findall(colorSearchResult))
                searchResult['色合検索'].append(colorSearchResultSet)
                bovwSearchUrl = re.compile(pattern=r'<span><a href="(.*)">特徴検索').findall(colorSearchResult)
                bovwSearch = await client.get(BASE + bovwSearchUrl[0])
                if bovwSearch.status != 200:
                    break
                bovwSearchResult = await bovwSearch.text()
                bovwSearchResultSet = await _process(re.compile(pattern=pattern).findall(bovwSearchResult))
                searchResult['特徴検索'].append(bovwSearchResultSet)
            except RuntimeError:
                pass
        await client.close()
        return searchResult


class AnimeSearch:
    BASE = 'https://trace.moe'
    enable = atri.animeSearch['enable']
    cmd = atri.animeSearch['command']

    @classmethod
    async def _wget(cls, url):
        async with aiohttp.ClientSession() as client:
            response = await client.get(cls.BASE + '/api/search?url=' + url)
            data = await response.json()
            if response.status != 200:
                return False
            data = data['docs'][0]
            date = data['from']
            _m = (date-(3600*(date*3600)))//60
            _s = date%60
            date = '%d:%s:%d'%(date%3600,_m if _m >= 10 else f'0{_m}',_s if _s >= 10 else f'0{_s}')
            return '匹配番剧:%s\n匹配相似度:%.2f%s\n匹配位置:%s' % (
                data['title'],
                data['similarity'] * 10,
                '%',
                date
            )

    @classmethod
    async def animeSearch(cls, url, _count=3):
        result = await cls._wget(url)
        if not result:
            while _count:
                result = cls._wget(url)
                _count -= 1
        return result if result else 'Not Found'


