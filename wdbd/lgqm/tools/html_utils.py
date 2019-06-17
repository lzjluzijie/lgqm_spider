#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
HTML爬虫工具类

@File    :   html_utils.py
@Time    :   2019/06/02 15:06:17
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   None
'''
from urllib import request
from bs4 import BeautifulSoup as bs



def get_soup(url, encoding="utf-8"):
    """
    取得HTML的BS4对象
    
    Arguments:
        url {string} -- 解析完成的BeautiflSoup对象
    """
    if url is None:
        return None

    rsp = request.urlopen(url)
    if rsp.getcode()!= 200:
        print("访问异常！")
    else:
        html = rsp.read().decode(encoding)
        # print(html)
        soup=bs(html,'html.parser')
        soup.prettify()
        # print(soup.prettify())
        return soup

if __name__ == "__main__":
    print("hello")