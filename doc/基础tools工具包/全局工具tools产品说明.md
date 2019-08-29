# 全局工具Tools产品说明

## 概述

全局工具是一个wdbd.tools.py文件，提供诸如日志、数据库连接等项目级别工具。

V 1 拥有几个工具：

- 日志API
- 配置文件读取
- 数据库连接API
- 日期格式工具，tools.DateUtils  （改为 date_utils）
- 数据库工具，tools.DbUtils （改为 db_utils）

本文就不同的工具进行逐一说明，最后部分还有tools迁移与可用性测试工具



### 下一步优化计划：

- 开发，配置测试命令行工具
- 开发，安装（初始化）工具
- 将代码实现，迁移到 tool.tools_impl.py 中





## 0 安装与使用



### 安装

**第一步 文件复制**

将以下文件和文件夹复制到您项目的源代码目录下：

- [文件] wdbd/tools.py
- [目录] wdbd/tool

将 目录config复制到项目根目录下

**第二步 全局常量修改**

打开tools.py，找到并修改以下常量：

| 常量         | 值说明                                     |
| ------------ | ------------------------------------------ |
| LOGGER_NAME  | 默认wdbd，一般不用修改                     |
| PROJECT_NAME | 默认fd，需要改成您自己的项目名，注意大小写 |

**第三步 运行install工具**

wdbd.tool.install.py 工具可以根据配置文件创建所需要的基本目录等，具体实现的功能如下：

- 创建日志存放目录， c:\\foo\\log\\
- 



### 依赖的类库：

基础类库：Anaconda 3.7

其他类库：

- mysql-connector
- sqlalchemy
- 











## 1 日志

tools提供日志输出工具，使得代码简单的调用

使用日志示例：

```python
import wdbd.tools as tl
tl.logger().info("balaba...")
# 控制台输出：[Thu, 29 Aug 2019 21:35:08][INFO ] balaba...
```

### 1 API介绍

tools中提供了一组全局函数，方便用户记录日志，下面是这些API的调用示例：

```python
# 普通调用：
tl.logger().info("balaba...")
# 控制台输出：[Thu, 29 Aug 2019 21:35:08][INFO ] balaba...

# 记录数据库SQL(日志级别默认DEBUG)：
sql_str = 'select * from employee'
tl.log_sql( sql_str )
```

说明：

- log_sql 使用默认记录器，记录级别为DEBUG

### 2 配置

日志通过 \\config\\log.cfg 文件实现配置。有几种常见配置操作：

#### 修改日志输出级别

- 默认是DEBUG以上输出（含DEBUG）

- 可修改 [logger_wdbd].level 属性，改成 DEBUG|INFO 等的一种


#### 修改日志输出方式

- 默认是 控制台和文件同时输出
- 可修改 [logger_wdbd].handlers 属性，控制输出目标，可配置多个用, 分割
- 输出目标stream，是输出到控制台
- 输出目标filert，是输出到日志文件

#### 修改日志文件存放路径

- 默认输出到 C:\\foo\\log\\ 目录下；
- 可修改 [handler_filert].args 属性，在第一个参数中指定输出路径

### 3 单元测试

单元测试文件，存放在 test.wdbd.tools_testcases 模块中，有测试文件

- test_log 测试日志输出



## 2 配置文件



## 3 数据库连接



## A 测试工具



## B 迁移工具

- 文件复制
- tool全局变量修改



## C 全局API清单

使用 

```python
from wdbd.tools import * 
```

就可以使用全局API，有：

- get_project_root_path()	获得当前项目根路径
- get_conn()     取得数据库连接
- conn_test      数据库连接测试（不对外）
- get_db_session  sqlalchemy系列
- get_pandas_conn
- logger()   获得日志记录类
- log_sql()  记录SQL语句

计划新增：

- get_config()

 













