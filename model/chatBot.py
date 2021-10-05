import aiohttp


class ChatBot(object):
    BASE = 'http://api.nekomimi.icu/v1/'

    @classmethod
    async def chat(cls, msg: str) -> dict:
        async with aiohttp.request('GET', cls.BASE + 'chat?msg=%s' % msg) as response:
            if response.status != 200 or (await response.json())['status'] != 'success':
                return {'status': 'bad'}
            return await response.json()
