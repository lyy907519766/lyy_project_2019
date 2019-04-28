# -*- coding-8 -*-
import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import datetime

'''
  功能：简单获取前10页，50个数据
'''

# http请求组装
def craw(url):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, b',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'acw_tc=b4a39f4515534218216507182460330522962912; hasShow=1',
        # 'Host': 'www.qichacha.com',
        # 'Referer': 'http://www.qichacha.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

    }
    # get请求 allow_redirects=False关闭重定向
    response = requests.get(url, headers=headers)
    # 判断返回的状态码
    if response.status_code != 200:
        response.encoding = 'utf-8'
        print('ERROR  请求失败,返回的状态码：{}'.format(response.status_code))
    # 将返回的文本转为XML
    soup = BeautifulSoup(response.text, 'lxml')
    print("返回的结果soup:",soup)

    # 01.XML中获取公司名称 存入集合
    com_names = soup.find_all(class_='ma_h1')

    # 02.单独 获取法定代表人
    peo_names = soup.findAll(class_='text-primary')

    # 03.获取 法定代表人、注册资本、成立时间，邮箱；电话；地址 的数据  原因：在同一行中 集合
    peo_phones = soup.find_all(class_='m-t-xs')
    # # 04 获取企业经营状态
    # qyjyzt_set = soup.findAll(class_='nstatus text-success-lt m-l-xs')
    # print("qyjyzt_set:",qyjyzt_set)
    # print("soup==============:",soup)

    # 设为全局变量
    global com_name_list
    global peo_name_list
    global peo_phone_list
    global com_place_list
    global zhuceziben_list
    global chenglishijian_list

    print('开始爬取数据，请勿打开excel')
    for i in range(0, len(com_names)):
        # 每个公司有三行数据，
        n = 1 + 3 * i
        m = i + 2 * (i + 1)
        # 联系电话
        peo_phone = peo_phones[n].find(class_='m-l').get_text().strip()
        # print("peo_phones[n]:",peo_phones[n])
        # 注册地址
        com_place = peo_phones[m].find(text=True).strip()
        # print("peo_phones[m]:",peo_phones[m])

        # 注册资本
        zhuceziben = peo_phones[3 * i].find(class_='m-l').get_text()
        # 成立时间
        chenglishijian = peo_phones[3 * i].contents[5].get_text()
        # print("peo_phones[3 * i]:",peo_phones[3 * i])

        peo_phone_list.append(peo_phone)
        com_place_list.append(com_place)
        zhuceziben_list.append(zhuceziben)
        chenglishijian_list.append(chenglishijian)

    # zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    for com_name, peo_name in zip(com_names, peo_names):
        com_name = com_name.get_text()
        peo_name = peo_name.get_text()
        com_name_list.append(com_name)
        peo_name_list.append(peo_name)


if __name__ == '__main__':
    # 公司名称
    com_name_list = []
    # 法人名称
    peo_name_list = []
    # 联系方式
    peo_phone_list = []
    # 公司地址
    com_place_list = []
    # 注册人资本
    zhuceziben_list = []
    # 成立时间
    chenglishijian_list = []

    key_word = input('请输入您想搜索的关键词：')
    print('正在搜索，请稍后')
    # 获取第一页的10条数据
    for x in range(1, 11):
        url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word, x)
        # 执行请求
        s1 = craw(url)

    workbook = Workbook(encoding='utf-8')
    sheet1 = workbook.add_sheet('结果01',cell_overwrite_ok=True)
    print('正在存储数据，请勿打开excel')
    # # 向sheet中写入数据
    name_list = ['公司名字', '法定代表人', '联系方式', '注册人资本', '成立时间', '公司地址']
    for cc in range(0, len(name_list)):
        sheet1.write(0, cc, name_list[cc])
    # 写入数据
    for i in range(0, len(com_name_list)):
        sheet1.write(i + 1, 0, com_name_list[i])  # 公司名字
        sheet1.write(i + 1, 1, peo_name_list[i])  # 法定代表人
        sheet1.write(i + 1, 2, peo_phone_list[i])  # 联系方式
        sheet1.write(i + 1, 3, zhuceziben_list[i])  # 注册人资本
        sheet1.write(i + 1, 4, chenglishijian_list[i])  # 成立时间
        sheet1.write(i + 1, 5, com_place_list[i])  # 公司地址
    # 保存excel文件，有同名的直接覆盖
    now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    workbook.save('./通过关键字{}爬取结果({}).xlsx'.format(key_word,now_date))

    print('the excel save success')