#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ximayala_demo.py
@Time    :   2019/08/20 20:56:41
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   None
'''

import re
import os
import json
import requests
import urllib
from urllib import request
from pypinyin import lazy_pinyin

class XimaLaya(object):
    # 模拟浏览器操作
    def __init__(self):
        self.header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
        }
 
    # 第一步： 根据输入的汉字转换为拼音
    def han_pinyin(self, hanzi):
        pin = lazy_pinyin(hanzi)   # 汉转拼音
        pin = "".join(pin)       # 去除空格
        return pin               # 返回拼音
 
    # 第二步： 根据REST格式去访问喜马拉雅,获取页面的HTML
    def getHtml(self, pinyin):
        url = 'https://www.ximalaya.com/yinyue/' + pinyin
        print("访问的网站是： " + url)
        html = requests.get(url, headers=self.header)
        # apparent_encoding通过调用chardet.detect()来识别文本编码，有些消耗计算资源
        html.encoding = html.apparent_encoding
        # html.encoding = 'utf8'  --> 直接改为UTF8也行
        with open('C:\\foo\\xmly\\html\\' + str(pinyin + '.html'), 'a', encoding='utf-8') as f:
            f.write(html.text)
        return html
 
    # 第三步：根据页面的内容获取对应歌单的albumId的值
    def getAlbumId(self, html):
        albumIdAll = re.findall(r'"albumId":(.*)', (html).text)  # 利用正则进行匹配,获取专辑ID
        # print("专辑信息", albumIdAll)
        with open('C:\\foo\\xmly\\albumIdAll\\' + str('albumIdAll.txt'), 'a', encoding='utf-8') as f:
            for x in albumIdAll:
                f.write(str(x))
        myList = []
        url3 = []
        for i in (albumIdAll[:1]):
            # 获取对应专辑ID的首页
            url2 = 'https://www.ximalaya.com/revision/play/album?albumId=' + i
            # print(url2)
            # 进入对应专辑ID的首页信息
            html2 = requests.get(url2.split(',')[0], headers=self.header)
            # 含有下载URL的集合
            # src   "http://audio.xmcdn.com/group12/M03/2C/AA/wKgDW1WJ7GqxuItqAB8e1LXvuds895.m4a"
            url3 = (re.findall(r'"src":"(.*?)"', (html2).text))
            # 记录信息用的
            myList.append('获取对应专辑ID的首页\r\n' + url2 + '\n---------------------------------------')
            myList.append('含有下载URL的集合\r\n' + html2.text + '\n---------------------------------------')
            myList.append('下载专辑的URL集合\r\n' + str(url3) + '\n---------------------------------------')

            print( html2.text )

            with open('c:\\foo\\xmly\\albumIdAll\\' + str('hhh.txt'), 'a', encoding='utf-8') as f:
                f.write(json.dumps(myList))
            break
        print('done')
        return url3    # 下载专辑的URL集合
 
    # 第四步： 获取专辑名
    def getTitle(self, html):
        t = re.findall(r'"title":"(.*?)"', (html).text)  # 获取titile（歌名）的值
        with open('C:\\foo\\xmly\\albumIdAll\\' + str('albumId_Name.txt'), 'a', encoding='utf-8') as f:
            f.write(str(t))
        return t
 
    # 第五步： 下载歌曲
    def downLoad(self, url, title):
        n = 0
        for i in url:
            try:
                urllib.request.urlretrieve(i, 'c:\\foo\\xmly\\download\\'+str(title[n]+'.m4a'))
                print(str(title[n]), '...【下载成功】')
                n = n + 1
            except:
                print(str(title[n]) + "...【下载失败】")
 
 
if __name__ == '__main__':
 
    fm = XimaLaya()
    # 输入需要下载的歌曲类型
    str1 = fm.han_pinyin("摇滚")
    # 获取对应歌曲类型的首页信息
    html = fm.getHtml(str1)
    # print( html )

    # 获取歌曲类型的首页里面的专辑名称
    title = fm.getTitle(html)
    # print( title )

    # 获取歌曲类型的首页里面的专辑ID
    url3 = fm.getAlbumId(html)
    # print( url3 )

    # 下载对应曲目
    fm.downLoad(url3, title)


