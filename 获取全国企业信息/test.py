# -*- coding-8 -*-
import requests
from bs4 import BeautifulSoup
import xlwt


def craw(url, key_word):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    headers = {

        'Host': 'www.qichacha.com',

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.qichacha.com/search?key=' + key_word,
        'Cookie': r'zg_did=%7B%22did%22%3A%20%2215fa403cb9d15f-036a7756df6645-173b7740-100200-15fa403cb9e2c6%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201510617843749%2C%22updated%22%3A%201510626410277%2C%22info%22%3A%201510285233062%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22f62f1e8a5eaa98a4fdd7be63f003baf3%22%7D; UM_distinctid=15fa403d33a86-04e900fd4e3572-173b7740-100200-15fa403d33b3d; CNZZDATA1254842228=770755339-1510283630-https%253A%252F%252Fwww.baidu.com%252F%7C1510623074; _uab_collina=151028523773154434859974; _umdata=2BA477700510A7DFF3E360D067D6CBF26EBF4D0B7616E2F668ACF5B05BA3A15BB7B2A5C9048062DECD43AD3E795C914C698D4F63619694FD3C24BCCF0E0016EF; PHPSESSID=tm27c7utiff9j5iqbh4g1cg0l5; acw_tc=AQAAAIyPMmgK2AUA4oumtwogJ3fbLlic; hasShow=1',
        'Cache-Control': 'no-cache',

    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        response.encoding = 'utf-8'
        print(response.status_code)
        print('ERROR')
    soup = BeautifulSoup(response.text, 'lxml')
    print("soup:",soup)
    # print(soup)
    com_names = soup.find_all(class_='ma_h1')  # 获取公司名称
    # print(com_names)
    # com_name1 = com_names[1].get_text()
    # print(com_name1)
    peo_names = soup.find_all(class_='a-blue')  # 公司法人
    # print(peo_names)
    peo_phones = soup.find_all(class_='m-t-xs')  # 公司号码
    # tags = peo_phones[4].find(text = True).strip()
    # print(tags)
    # tttt = peo_phones[0].contents[5].get_text()
    # print (tttt)
    # else_comtent = peo_phones[0].find(class_='m-l')
    # print(else_comtent)
    # peo_emails=soup.find_all(class_='m-1')
    global com_name_list
    global peo_name_list
    global peo_phone_list
    global com_place_list
    global zhuceziben_list
    global chenglishijian_list
    global email_list
    print('开始爬取数据，请勿打开excel')
    for i in range(0, len(com_names)):
        n = 1 + 3 * i
        m = i + 2 * (i + 1)
        try:
            peo_phone = peo_phones[n].find(text=True).strip()
            com_place = peo_phones[m].find(text=True).strip()
            zhuceziben = peo_phones[3 * i].find(class_='m-l').get_text()
            chenglishijian = peo_phones[3 * i].contents[5].get_text()
            email = peo_phones[n].contents[1].get_text()

            # print('email',email)
            peo_phone_list.append(peo_phone)
            com_place_list.append(com_place)
            zhuceziben_list.append(zhuceziben)
            chenglishijian_list.append(chenglishijian)
            email_list.append(email)
        except Exception:
            print('exception')

    for com_name, peo_name in zip(com_names, peo_names):
        com_name = com_name.get_text()
        peo_name = peo_name.get_text()
        com_name_list.append(com_name)
        peo_name_list.append(peo_name)


if __name__ == '__main__':
    com_name_list = []
    peo_name_list = []
    peo_phone_list = []
    com_place_list = []
    zhuceziben_list = []
    chenglishijian_list = []
    email_list = []

    key_word = input('请输入您想搜索的关键词：')
    print('正在搜索，请稍后')
    for x in range(1, 11):
        if x == 1:
            url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word, x)
        else:
            url = r'http://www.qichacha.com/search_index?key={}&ajaxflag=1&p={}&'.format(key_word, x)
        # url = r'http://www.qichacha.com/search?key={}#p:{}&'.format(key_word,x)
        s1 = craw(url, key_word.encode("utf-8").decode("latin1"))
    workbook = xlwt.Workbook()
    # 创建sheet对象，新建sheet
    sheet1 = workbook.add_sheet('xlwt', cell_overwrite_ok=True)
    # ---设置excel样式---
    # 初始化样式
    style = xlwt.XFStyle()
    # 创建字体样式
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True  # 加粗
    # 设置字体
    style.font = font
    # 使用样式写入数据
    # sheet.write(0, 1, "xxxxx", style)
    print('正在存储数据，请勿打开excel')
    # 向sheet中写入数据
    name_list = ['公司名字', '法定代表人', '联系方式', '注册人资本', '成立时间', '公司地址', '公司邮件']
    for cc in range(0, len(name_list)):
        sheet1.write(0, cc, name_list[cc], style)
    for i in range(0, len(com_name_list)):
        sheet1.write(i + 1, 0, com_name_list[i], style)  # 公司名字
        sheet1.write(i + 1, 1, peo_name_list[i], style)  # 法定代表人
        sheet1.write(i + 1, 2, peo_phone_list[i], style)  # 联系方式
        sheet1.write(i + 1, 3, zhuceziben_list[i], style)  # 注册人资本
        sheet1.write(i + 1, 4, chenglishijian_list[i], style)  # 成立时间
        sheet1.write(i + 1, 5, com_place_list[i], style)  # 公司地址
        sheet1.write(i + 1, 6, email_list[i], style)  # 邮件地址
    # 保存excel文件，有同名的直接覆盖
    workbook.save(r'C:\Users\Administrator\Desktop\test.xls')
    print('the excel save success')