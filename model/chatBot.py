import aiohttp
class ChatBot(object):
    BASE = 'http://nekomimi.icu/'
    def __init__(self):
        self.BASE = 'http://nekomimi.icu/'

    @classmethod
    async def chat(cls,msg:str) -> dict:
        async with aiohttp.request('GET',cls.BASE+'chatbot?msg=%s'%msg) as response:
            if response.status != 200 or (await response.json())['status'] != 'success':
                return {'status':'bad'}
            return await response.json()

