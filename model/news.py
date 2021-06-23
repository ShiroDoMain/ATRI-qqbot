import json

import requests


def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery341001657575837432268_1581070969707' \
          '&_=1581070969708 '
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Mobile Safari/537.36'}
    res = requests.get(url, headers=headers).text
    a = res.split('jQuery341001657575837432268_1581070969707(')[1].split(')')[0]
    c = json.loads(a)
    data = json.loads(c['data'])
    return data


def print_data_china():
    data = get_data()
    return '''
=================
   今日疫情
-----------------
统计截至时间:
%s
-----------------
全国确诊人数:
%s 
-----------------
现存确诊人数:
%s
-----------------
相较于昨天确诊人数:
%s
-----------------
全国疑似病例:
%s
-----------------
相较于昨天疑似人数:
%s
-----------------
全国治愈人数:
%s
-----------------
相较于昨天治愈人数:
%s
-----------------
全国死亡人数:
%s
-----------------
相较于昨天死亡人数:
%s
=================''' % (str(data['lastUpdateTime']),
                        str(data['chinaTotal']['confirm']),
                        str(data['chinaTotal']['nowConfirm']),
                        str(data['chinaAdd']['confirm']),
                        str(data['chinaTotal']['suspect']),
                        str(data['chinaAdd']['suspect']),
                        str(data['chinaTotal']['heal']),
                        str(data['chinaAdd']['heal']),
                        str(data['chinaTotal']['dead']),
                        str(data['chinaAdd']['dead']))

