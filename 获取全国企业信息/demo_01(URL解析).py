#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: demo_01(URL解析).py
@时间: 2019/3/12 20:16 
@版本：1.0
@作用:爬虫-获取网页数据测试
@逻辑
'''
import requests

def get_html_text(url):
    """
        返回url的文本
    """
    request_obj = requests.post(url, timeout=30)
    print(request_obj.status_code)  # 打印状态码
    print(request_obj.url)  # 打印请求url
    print(request_obj.headers)  # 打印头信息
    print(request_obj.cookies)  # 打印cookie信息
    print(request_obj.text)  # 以文本形式打印网页源码
    print(request_obj.content)  # 以字节流形式打印

    # response = requests.get('http://httpbin.org/get')
    # print(response.text)

    return  request_obj.text

# 主函数
def run():
    url = "http://www.baidu.com"
    txt_value = get_html_text(url)
    # print(txt_value)

if __name__ =="__main__":
    run()