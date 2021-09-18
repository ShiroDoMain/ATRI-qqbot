import aiohttp
from matplotlib import pyplot as plt


async def weather(city,model='day'):
    async with aiohttp.ClientSession() as session:
        model = '1d' if model=='day' else ''
        response = await session.get('http://api.nekomimi.icu/v1/weather%s?city=%s'%(model,city))
        if response.status != 200:
            return False
        data = await response.json()
        if data['status'] != 'success':
            return False
        data =data['data']
        if not model:
            day = data['state']
            maxTem = data['max']
            minTem = data['min']
            plt.clf()
            plt.title('%s七日天气'%city)
            plt.ylim(0,50)
            plt.plot(day,maxTem,'r-',label='最高气温')
            plt.plot(day,minTem,'b-',label='最低气温')
            plt.ylabel('温度')
            plt.legend()
            plt.savefig('temp/%s.jpg'%city)
            return 'temp/%s.jpg'%city
        else:
            plt.clf()
            plt.title('%s24小时天气'%city)
            xlabel = [str(d)+'\n'+w[:-1] for d,w in zip(data['date'],data['wind'])]
            plt.xlim(24)
            plt.ylim(0,120)
            plt.bar(xlabel,data['tem'],label='温度')
            plt.plot(xlabel,data['hum'],'b-',label='湿度')
            plt.plot(xlabel,data['aqi'],'g-*',label='空气质量')
            plt.plot(xlabel,data['ws'],'g->',color='indianred',label='风速')
            plt.legend()
            plt.savefig('temp/%s.jpg'%city)
            return 'temp/%s.jpg'%city

