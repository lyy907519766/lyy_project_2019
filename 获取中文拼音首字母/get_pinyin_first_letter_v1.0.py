#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: get_pinyin_first_letter_v1.0.py
@时间: 2019/4/22 15:31 
@版本：1.0
@作用: 将中文拼音首字母 转换为汉语
@逻辑
'''
from pytz import unicode
import logging
import os

# log日志信息
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# 读取的文件绝对路径
read_txt_path = os.path.join(os.getcwd(), 'search_table_list.txt')
# 输出的txt文件名称
write_txt_path = os.path.join(os.getcwd(), 'result_table_list.txt')   # 获取汉字首字母
def multi_get_letter(str_input):
    if isinstance(str_input, unicode):
        unicode_str = str_input
    else:
        try:
            unicode_str = str_input.decode('utf8')
        except:
            try:
                unicode_str = str_input.decode('gbk')
            except:
                print('unknown coding')
                return
    return_list = []
    for one_unicode in unicode_str:
        return_list.append(single_get_first(one_unicode))
    return return_list

def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        # print(asc)
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''

# 读取txt中的数据内容，放入指定的list中
def load_ods_table(table_list_file):
    search_table_list = []
    with open(table_list_file, 'r',encoding="utf-8") as f:
        for line in f:
            if line is not None and line.strip('\n').strip() !="":
                search_table_list.append(line.strip('\n').strip())
    logging.info("读取文件成功，共有{}条数据".format(len(search_table_list)))
    return search_table_list

# 将数据写入txt文件中
def writer_data_txt(write_txt_path,data):
    file = open(write_txt_path,'w')
    for i in range(len(data)):
        result_value = str(data[i])
        # 去掉空格，换行；替换"|"符号
        result_value = result_value.strip()+'\n'
        file.write(result_value)
    file.close()

def main(str_input):
    list1 = multi_get_letter(str_input)
    res = ''
    for i in list1:
        if type(i).__name__ =='bytes':
             i = i.decode()
        res = res+i
    # print(res)
    return res

if __name__ == "__main__":
    logging.info("********开始查询,读取的文件为：{}中。".format(read_txt_path))
    # 01.读取数据，存入指定list
    search_field_name = load_ods_table(read_txt_path)
    # 结果list
    resutl_field_name = []
    # 02.查询
    for index,field_name in enumerate(search_field_name):
        # str_input=u'我们都只发大水发放'
        resutl_field_name.append(main(field_name))
    # 03.输出所有查询的结果
    writer_data_txt(write_txt_path, resutl_field_name)
    logging.info("*******查询完成，结果在{}中。".format(write_txt_path))