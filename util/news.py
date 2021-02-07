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


# def print_data_path_china():
#     data = get_data()['areaTree'][0]['children']
#     path_data = []
#     path_china = []
#     path = str(input('请输入你要查询的省份：'))
#     for i in data:
#         path_china.append(i['name'])
#         path_data.append(i['children'])
#     if path in path_china:
#         num = path_china.index(path)
#         data_path = path_data[num]
#         print('{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}'.format('地区', '累计确诊人数', '相较于昨日确诊人数', '累计疑似病例',
#                                                                               '相较于昨日疑似病例', '累计治愈人数', '相较于昨日治愈人数',
#                                                                               '累计死亡人数', '相较于昨日死亡人数'))
#         for i in data_path:
#             name = i['name']
#             today = i['today']
#             total = i['total']
#             a = '{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}'
#             print(a.format(name, str(total['confirm']), str(today['confirm']), str(total['confirm']),
#                            str(today['suspect']), str(total['heal']), str(today['heal']), str(total['dead']),
#                            str(today['dead'])))
#
#
# if __name__ == '__main__':
#     print(get_data())
#     print(print_data_china())
    # print(print_data_path_china())
