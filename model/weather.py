import aiohttp
from matplotlib import pyplot as plt


async def weather(city):
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://api.nekomimi.icu/v1/weather?city=%s'%city)
        if response.status != 200:
            return False
        data = await response.json()
        if data['status'] != 'success':
            return False
        data =data['data']
        day = data['state']
        maxTem = data['max']
        minTem = data['min']
        plt.clf()
        plt.title('%s天气'%city)
        plt.plot(day,minTem,'b-',label='最低气温')
        plt.plot(day,maxTem,'r-',label='最高气温')
        plt.ylabel('温度')
        plt.legend()
        plt.savefig('storage/tempfile/%s.jpg'%city)
        return 'storage/tempfile/%s.jpg'%city
