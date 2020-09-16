# -*- coding: utf-8 -*-
# @Time : 2020/8/16 1:49 下午
# @Author : shiro
# @Software: PyCharm
from qqai.nlp.translate import ImageTranslate
from util import appid,key

with open('Imglate.png') as file:
    result = ImageTranslate(appid,key).run('Imglate.png','doc')


print(result)




