# lpr爬虫产品手册 v1



| 文档版本 | 修订日期   | 修订内容 | 修订人 |
| -------- | ---------- | -------- | ------ |
| v 1      | 2019-08-27 | 起草文档 | wdbd   |
|          |            |          |        |







## 一、概述

### 实现目标

本版投产后需要实现以下目标：

- 定时（每月、每日）检查lpr数据，并爬取下载；
- 可爬取历史数据（2019-8-20前）
- 有cli接口，查询最新爬取的数据情况；
- 有cli接口，查询指定日期的lpr数据；
- 有cli接口，爬取指定年份、月份的历史数据；
- 尝试使用 axxxx 框架执行定时任务

### 限制

### 功能结构
xmind脑图

![](C:\python\workspace\lgqm_spider\doc\lpr\lpr v1 开发需求.assets\lpr爬虫.png)

### 名词说明

- LPR：贷款市场报价利率





## 二、业务流程

本应用主要是在线爬取lpr数据，然后存入数据库。其主要的业务流程是：

1. 人工启动服务器上lpr爬取服务：spider；

2. spider查看爬取时机，如是则启动爬虫，否则继续等待；

3. spider爬取url，下载文件到临时文件夹；

4. spider对比下载文件中的内容，如有“新数据”则更新本地文件，并更新数据库；

5. spider继续等待。

   


## 三、接口需求（用户视图）

用户操作，主要使用命令行接口，主要有以下几项操作：

- 启动爬虫服务器
- 查询当前lpr数据
- 查询历史lpr数据
- 爬取历史lpr数据（按年、按月）



### 启动爬虫服务器

命令行接口：

```
python lpr.py start-spider-server
```

参数：

- 无

反馈：

```
python lpr.py start-spider-server

爬取lpr数据，开始于{当前时间} ...
连接测试:
. 数据库连接: 成功
. FTP连接:   成功
连接测试完成！

{当前时间} 爬取中 ...
{当前时间} 爬取成功 ...
```

说明：

- 启动后，要进行连接测试，测试成功才正式启动server，否则终止程序；
- 只有爬到新数据后，才显示日志



### 查询当前lpr数据

命令行接口：

```
python lpr.py now
```

参数：

- 无

反馈：

```
python lpr.py now

日期           1Y       5Y
2019-08-20  4.26     5.21  
```

说明：

- 显示最新的数据日期



### 查询历史lpr数据

命令行接口：

```
python lpr.py --data 20180901
```

参数：

- data   yyyyMMdd格式的日期

反馈：

```
python lpr.py --data 20180901

日期           1Y       5Y
2018-09-01  4.26     5.21  
```

说明：

- 根据参数显示并回显





### 爬取历史lpr数据（按年、按月）

命令行接口：

```
python lpr.py spider-history --year 2019 | --month 201908
```

参数：

- year     按年下载所有的数据（覆盖当前数据）
- month  按月下载数据

反馈：

```
python lpr.py spider-history --year 2019

爬取完成，共下载x个文件，y个日期的数据
```



## 四、技术架构要求

## 数据存储

爬取后的数据存入两个目标地方：

- 阿里云数据库
- FTP目录



## 阿里云数据库结构

阿里云数据库中有表：

- lpr LPR数据

其数据结构为：

```python

# lpr数据表
create table lpr
(
    trade_date  varchar(10)     not null COMMENT '日期' ,
    lrp_1y      decimal(10,6)   COMMENT '一年期利率' ,
    lrp_5y      decimal(10,6)   COMMENT '五年期利率' ,

    PRIMARY KEY (`trade_date`)
)

```



## 五、上线准备

## 



## 附录

## LPR数据下载

下载地址：（excel格式）

```
http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_LPR_Data_2019_8.xls&nameOld=LPR%CA%FD%BE%DD2019_8.xls&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data
```

其中：

1. nameNew 是后台申请文件名，按月
2. nameOld 是下载后生成的文件名，默认是：LPR数据yyyy_M.xls
3. 下载后有 Sheet1 是数据页
4. 有标题行：日期|1Y|5Y
5. 仅有报价日期，20190820前每个交易日都有报价，20190820（含）后仅每月20日有报价；
6. 每列为一种期限的报价，有报价用"4.27"格式显示，无报价用 -- 显示

![1566885864509](C:\python\workspace\lgqm_spider\doc\lpr\lpr v1 开发需求.assets\1566885864509.png)



下载地址：（txt格式）

```
http://www.shibor.org/shibor/web/html/downLoad.html?nameNew=Historical_LPR_Data_2019_8.txt&nameOld=LPR%CA%FD%BE%DD2019_8.txt&shiborSrc=http%3A%2F%2Fwww.shibor.org%2Fshibor%2F&downLoadPath=data
```

其中：

1. 有标题行，有分割线行（第二行）



![1566885938598](C:\python\workspace\lgqm_spider\doc\lpr\lpr v1 开发需求.assets\1566885938598.png)








