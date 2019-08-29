#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download_demo.py
@Time    :   2019/08/27 15:05:35
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   python互联网下载文件的实例程序
'''

import urllib 
# import urllib2 
import requests


# print("downloading with urllib 1") 
# # url = 'http://www.pythontab.com/test/demo.zip'  
# url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_LPR_Data_2019_8.txt&nameOld=LPR%CA%FD%BE%DD2019_8.txt&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data'
# print("downloading with urllib 2")
# urllib.request.urlretrieve(url, "LPR 201908.txt")

print("downloading with urllib 1")  
url = 'http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_LPR_Data_2019_8.txt&nameOld=LPR%CA%FD%BE%DD2019_8.txt&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data'
print("downloading with urllib 2")

r = requests.get(url) 
r.encoding = 'utf-8'
with open("LPR 201908.txt", mode="wb") as code:
    code.write( r.content )
    # code.write( r.text )

