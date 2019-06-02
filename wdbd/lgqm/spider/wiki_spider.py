#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
临高启明 WIKI 爬取程序

爬取网站：http://lgqm.huijiwiki.com


@File    :   wiki_spider.py
@Time    :   2019/06/02 14:48:32
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   None
'''
from urllib import request
from bs4 import BeautifulSoup as bs
import wdbd.lgqm.tools.html_utils as html_utils


class TongrenArticle:
    """
    同人作品 信息
    """
    id = 0              # 序号
    title = ""          # 标题
    author = ""         # 作者
    key_words = []      # 内容关键字
    types = []          # 主要涉及的方面，地点
    start_time = ""     # 起更时间
    last_update_time = ""   # 最后更新时间
    status = ""         # 状态
    use_status = ""     # 转正状态
    count_of_word = ""  # 字数（千字）
    url = ""            # 文章地址
# ========================================


def get_tongren_list():
    """
    取得同人文章信息

    param :
    return:
    """
    # 同人作品列表页面
    URL =  "http://lgqm.huijiwiki.com/wiki/%E5%90%8C%E4%BA%BA%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8"
    soup = html_utils.get_soup(URL)

    # 开始HTML处理
    article_list = []
    table = soup.find('table'
            ,{'class':'wikitable table sortable'})
    for line in table.find_all('tr'):
        if line.td is not None:
            tds = line.findAll('td')
            if tds[1].get_text().replace("\n", "") != '':

                obj = TongrenArticle()
                obj.id = tds[0].get_text().replace("\n", "")
                obj.title = tds[1].get_text().replace("\n", "")
                obj.author = tds[2].get_text().replace("\n", "")
                obj.key_words = tds[3].get_text().replace("\n", "").split(",")
                obj.types = tds[4].get_text().replace("\n", "").split(",")
                obj.start_time = tds[5].get_text().replace("\n", "")
                obj.last_update_time = tds[6].get_text().replace("\n", "")
                obj.status = tds[7].get_text().replace("\n", "")
                obj.use_status = tds[8].get_text().replace("\n", "")
                obj.url = tds[1].a['href']  # todo 此处可改为完整的变量 
                
                article_list.append(obj)
    return article_list    

def get_tongren_titles():
    """
    爬取所有同人作品清单（标题）

    return: list of string，作品标题文本
    """
    # 同人作品列表页面
    URL =  "http://lgqm.huijiwiki.com/wiki/%E5%90%8C%E4%BA%BA%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8"

    rsp = request.urlopen(URL)  # TODO 这部分需要提炼成一个工具函数
    if rsp.getcode()!= 200:
        print("访问异常！")
    else:
        html = rsp.read().decode('utf-8')
        # print(html)
        soup=bs(html,'html.parser')
        # print(soup.prettify())

        # 开始HTML处理
        title_list = []
        table = soup.find('table'
            ,{'class':'wikitable table sortable'})
        # print(type(table))
        # print(table.tr.th.get_text())
        for line in table.find_all('tr'):
            if line.td is not None:
                article_title = line.findAll('td')[1].get_text()
                article_title = article_title.replace("\n", "")
                if article_title:
                    
                    title_list.append(article_title)
        return title_list

if __name__ == "__main__":
    list = get_tongren_list()
    # print(list)

    for obj in list:
        print("{0} : {1} = {2}".format(obj.id, obj.title, obj.url))

    print(len(list))

