#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: demo_05.py 
@时间: 2019/3/24 18:50 
@版本：1.0
@作用:
@逻辑
'''
import requests
from bs4 import BeautifulSoup

def craw(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
    headers = {'User-Agent':user_agent,

}
    response = requests.get(url,headers = headers)
    print(response.cookies)
    if response.status_code != 200:
        response.encoding = 'utf-8'

        print('ERROR')

    soup = BeautifulSoup(response.text,'lxml')
    # print(soup)
if __name__ == '__main__':
    url = r'http://www.qichacha.com/search?key=%E5%A9%9A%E5%BA%86'
    s1 = craw(url)