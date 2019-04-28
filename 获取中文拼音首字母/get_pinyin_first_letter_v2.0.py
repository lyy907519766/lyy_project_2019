#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: wenzi_zhuan_yuyin.py
@时间: 2019/4/28 18:25 
@版本：2.0
@作用: 获取中文首字母
@逻辑
'''
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


# 汉字转为拼音  获取拼音首字母
def chinese_to_pinyin(x):
    y = ''
    dic = {}
    with open("unicode_py.txt") as f:
        for i in f.readlines():
            dic[i.split()[0]] = i.split()[1]
    for i in x:
        hanzi_flag = is_chinese(i)
        if hanzi_flag:
            # unicode-escape是对unicode编码的字节流，两个字节两个字节转义，并对每两个字节一起以16进制输出
            i = str(i.encode('unicode_escape'))[-5:-1].upper()
            try:
                # 获取编码表中的拼音的首字母，然后转为小写
                y += dic[i][0].lower()
            except:
                # 异常的值直接相加
                y += i
        else:
            # 非汉字不识别，直接相加
            y += i
    return y

def is_chinese(uchar):
    """判断一个unicode是否是汉字  可以直接输入汉字，同样识别"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

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

if __name__ == "__main__":
    logging.info("********开始查询,读取的文件为：{}中。".format(read_txt_path))
    # 01.读取数据，存入指定list
    search_field_name = load_ods_table(read_txt_path)
    # 结果list
    resutl_field_name = []
    # 02.查询
    for index,field_name in enumerate(search_field_name):
        # str_input=u'我们都只发大水发放'
        resutl_field_name.append(chinese_to_pinyin(field_name))

    # 03.输出所有查询的结果
    writer_data_txt(write_txt_path, resutl_field_name)
    logging.info("*******查询完成，结果在{}中。".format(write_txt_path))
