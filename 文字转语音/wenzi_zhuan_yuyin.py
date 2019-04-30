#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@作者: LYY
@文件: wenzi_zhuan_yuyin.py
@时间: 2019/4/28 18:25 
@版本：1.0
@作用: 文字转语音
@逻辑
    参考文章：https://zhuanlan.zhihu.com/p/26726297
   01.根据文字库，将文字转为拼音；
   02.根据拼音对比语音库，获取声音
'''
import pygame

def chinese_to_pinyin(x):
    y = ''
    dic = {}
    with open("unicode_py.txt") as f:
        for i in f.readlines():
            dic[i.split()[0]] = i.split()[1]
    for i in x:
        i = str(i.encode('unicode_escape'))[-5:-1].upper()
        try:
            y += dic[i] + ' '
        except:
            y += 'XXXX '
    return y

''' 这里需要建立自己的单个音的音频库 '''
def make_voice(x):
    pygame.mixer.init()
    voi = chinese_to_pinyin(x).split()
    for i in voi:
        if i == 'XXXX':
            continue
        print("i:",i)
        pygame.mixer.music.load("voice/" + i + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            pass
    return None

while True:
    p = input("请输入文字：")
    # 获取的拼音  测试文字：我们都是中国人
    pingyin_str = chinese_to_pinyin(p)
    print("pingyin_str::",pingyin_str)
    make_voice(p)