#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: get_data_v1.0.py
@时间: 2019/3/24 17:41 
@版本：1.0
@作用:
@逻辑  线程池；IP  框架
'''
import requests
from bs4 import BeautifulSoup

class Qi(object):
    def __init__(self):
        # 不知道，暂时不管
        self.ip_list = [
            '180.163.159.13:443'
        ]
        self.coolie = []
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        b = requests.get('http://www.qichacha.com/search?key=包装', headers=self.header)
        for i in b.cookies:
            print(i.value)
            self.coolie.append(i.value)
        print("b=================:", self.coolie)

    # 获取HTML
    def get_html(self, url, referer='https://m.qichacha.com/'):
        header = {
            'referer': referer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            'Cookie': 'acw_tc={0}; PHPSESSID={1};'.format(self.coolie[1], self.coolie[0])
        }
        html = requests.get(url, headers=header)
        return html.text

    # 解析HTML  获取公司信息
    def parser_home_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        try:
            for i in soup.find('section', id='searchlist').find('tbody').find_all('tr'):
                try:
                    print(i.find('a', 'ma_h1').get_text())
                    print('http://www.qichacha.com' + i.find('a', 'ma_h1')['href'])
                    yield 'http://www.qichacha.com' + i.find('a', 'ma_h1')['href'], i.find('a', 'ma_h1').get_text()
                except:
                    print(i.find('a', 'ma_h1').get_text(),
                          i.find('span', 'nstatus text-warning m-l-xs').get_text().strip())
        except:
            print('没有查到该公司')

    # 解析HTML   获取公司明细信息
    def parser_detail_html(self, html, name):
        basic_list = {}
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('tr')
        # 法人
        try:
            basic_list['legalPersonName'] = soup.find('a', 'bname').get_text()
        except:
            basic_list['legalPersonName'] = ''
        # 企业名
        basic_list['name'] = name
        # 企业logo
        basic_list['logo'] = soup.find('div', 'imgkuang').img['src']
        # 联系方式
        try:
            basic_list['contact'] = soup.find('div', 'content').find_all('div', 'row')[1].find('span',
                                                                                               'cvlu').span.get_text().strip()
        except:
            basic_list['contact'] = ''

        # 官网
        try:
            basic_list['websiteList'] = soup.find('div', 'content').find_all('div', 'row')[2].find_all('span', 'cvlu')[
                -1].get_text()
        except:
            basic_list['websiteList'] = ''
        # 注册资本：
        try:
            basic_list['regCapital'] = content[0].find_all('td')[1].get_text().strip()
        except:
            basic_list['regCapital'] = ''

        # 成立日期：
        try:
            basic_list['estiblishTime'] = content[1].find_all('td')[3].get_text().strip()
        except:
            basic_list['estiblishTime'] = ''
        # 注册号：
        try:
            basic_list['regNumber'] = content[2].find_all('td')[1].get_text().strip()
        except:
            basic_list['regNumber'] = ''

        # 公司类型：
        try:
            basic_list['companyOrgType'] = content[4].find_all('td')[1].get_text().strip()
        except:
            basic_list['companyOrgType'] = ''
        # 所属行业：
        try:
            basic_list['industry'] = content[4].find_all('td')[3].get_text().strip()
        except:
            basic_list['industry'] = ''

        # 营业期限
        try:
            basic_list['operatingPeriod'] = content[8].find_all('td')[3].get_text().strip()
        except:
            basic_list['operatingPeriod'] = ''
        # 企业地址：
        try:
            basic_list['regLocation'] = content[9].find_all('td')[1].get_text().strip().split('查看地图')[0].strip()
        except:
            basic_list['regLocation'] = ''
        # 经营范围：
        try:
            basic_list['range'] = content[-1].find_all('td')[1].get_text().strip()
        except:
            basic_list['range'] = ''
        print(basic_list)

    def main(self):
        # url = 'http://www.qichacha.com/search?key={}'.format(quote(sys.argv[1]))
        url = 'http://www.qichacha.com/search?key={}'.format('包装')
        print("请求的URL:",url)
        home_html = self.get_html(url)
        print("home_html:",home_html)
        for detail_url, name in self.parser_home_html(home_html):
            detail_html = self.get_html(detail_url, url)
            self.parser_detail_html(detail_html, name)

if __name__ == '__main__':
    Qi().main()
