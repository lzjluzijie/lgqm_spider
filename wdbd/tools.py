#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2019/08/29 15:40:22
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   全项目工具类

功能包括：
- 日志
- 数据库访问
- 配置文件


'''

import logging.config
import os
import sqlite3
import time
import datetime
from configparser import ConfigParser

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# =====================================================================================
# 全局常量：

LOGGER_NAME = 'wdbd'

PROJECT_NAME = 'fd'

# sqlalchemy是否输出SQL明细日志
sqlalchemy_echo = False


# 默认配置文件
# #PROJECT# 是项目根目录
DEFAULT_CONFIG_FILES = {
    'config_file': r'#PROJECT#config{0}config.cfg'.format(os.path.sep),  # 默认配置文件
    'log_config_file': r'#PROJECT#config{0}log.cfg'.format(os.path.sep),  # 默认日志配置文件
    'db_cfg_file': r'#PROJECT#config{0}db.cfg'.format(os.path.sep),  # 默认数据库连接配置文件
}

DATE_DB_FORMAT = '%Y%m%d'  # 日期格式，数据库存放格式

DATE_VIEW_FORMAT = '%Y-%m-%d'  # 日期格式，查看格式

DATETIME_DB_FORMAT = '%Y%m%d %H%M%S'  # 日期格式，数据库存放格式

DATETIME_VIEW_FORMAT = '%Y-%m-%d %H:%M:%S'  # 日期格式，查看格式

# 创建对象的基类:
Base = declarative_base()
# the_engine = None
# session_class = None

# =====================================================================================
# 基础服务函数

# 项目根路径
def get_project_root_path():
    """
       取得项目根路径
       支持win / mac 操作系统
       :return: str, path of project root
       """
    curr_path = os.path.abspath(os.path.dirname(__file__))
    root_path = curr_path[:curr_path.find(PROJECT_NAME + os.path.sep) + len(PROJECT_NAME + os.path.sep)]
    return root_path


# 当前目录绝对路径
def get_current_path():
    """
    取得当前的绝对路径

    支持win / mac 操作系统

    如 c:\\fdsafs\\ 或 /User/jack/prjects/

    :return: str，绝对路径
    """
    return os.getcwd() + os.path.sep


# =====================================================================================
# 数据库工具

# 获得数据库连接
def get_conn(vender=None, mode=None, cfg_path=None):
    """
    取得数据库连接
    默认无参数，则根据配置文件取数据库连接信息
    有参数，则根据参数去配置文件中取相应连接信息

    如果无法连接，则抛出 Exception
    :param vender: str, 默认None, 数据库类型Vender
    :param mode: str, 默认None，环境标识
    :param cfg_path: str, 默认None，配置文件所在路径
    :return: connection连接对象
    """

    if cfg_path is None:
        cfg_file_path = DEFAULT_CONFIG_FILES.get('db_cfg_file').replace('#PROJECT#', get_project_root_path())
    else:
        cfg_file_path = cfg_path

    try:
        cfg = Config(path=cfg_file_path)
        if vender is None:
            vender = cfg.get('db', 'VENDER')
        if mode is None:
            # mode = cfg.get('db', 'MODE')
            # 从config.cfg中读取APP_STATUS
            mode = get_app_status()

    except:
        print('config file = {0}'.format(cfg_file_path))
        raise Exception('数据库配置文件错误!')

    if vender == 'sqlite3':
        try:
            url = cfg.get('db', 'sqlite3.{0}.file_path'.format(mode))
            url = url.replace('#PROJECT#', get_project_root_path())
            conn = sqlite3.connect(url)
        except Exception as e:
            raise Exception('sqlite3 连接失败!error_msg={0}'.format(str(e)))
    elif vender == 'mysql':
        try:
            conn = mysql.connector.connect(
                host=cfg.get('db', 'mysql.{0}.host'.format(mode)),  # 数据库主机地址
                user=cfg.get('db', 'mysql.{0}.user'.format(mode)),  # 数据库用户名
                passwd=cfg.get('db', 'mysql.{0}.password'.format(mode)),  # 数据库密码
                database=cfg.get('db', 'mysql.{0}.db'.format(mode)),
                buffered=True
            )
        except Exception as ee:
            raise Exception('mysql 连接失败! error_msg = {0}'.format(str(ee)))
    else:
        raise Exception('无效的数据库VENDER')

    return conn


# 数据库连接测试
def conn_test(vender=None, mode=None, cfg_path=None):
    """
    数据库连接测试

    尝试连接数据库，只支持 mysql 和 sqlite3 数据库

    :param vender: str, 默认None, 数据库类型Vender
    :param mode: str, 默认None，环境标识
    :param cfg_path: str, 默认None，配置文件所在路径
    :return: bool, 是否连接成功
    """
    con = None

    try:
        con = get_conn(vender=vender, mode=mode, cfg_path=cfg_path)
        if con:
            return True
        else:
            return False
    except:
        return False
    finally:
        if con:
            con.close()


def get_db_session(vender=None, mode=None, cfg_path=None):
    """
    取得数据库连接session
    
    Returns:
        [type] -- [description]
    """
    if cfg_path is None:
        cfg_file_path = DEFAULT_CONFIG_FILES.get('db_cfg_file').replace('#PROJECT#', get_project_root_path())
    else:
        cfg_file_path = cfg_path

    try:
        cfg = Config(path=cfg_file_path)
        if vender is None:
            vender = cfg.get('db', 'VENDER')
        if mode is None:
            # mode = cfg.get('db', 'MODE')# todo 要修改
            mode = get_app_status()
    except:
        # print('config file = {0}'.format(cfg_file_path))
        raise Exception('数据库配置文件错误!')


    # the_engine = create_engine('mysql+mysqlconnector://dev:dev_61875707@rm-bp13oao7f763scs44yo.mysql.rds.aliyuncs.com:3306/fdata_dev')
    the_engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?charset=utf8'.format(
                cfg.get('db', 'mysql.{0}.user'.format(mode)),
                cfg.get('db', 'mysql.{0}.password'.format(mode)),
                cfg.get('db', 'mysql.{0}.host'.format(mode)),
                cfg.get('db', 'mysql.{0}.db'.format(mode)),
                buffered=True
            )
            , echo=sqlalchemy_echo
            )
    session_class = sessionmaker(bind=the_engine)
    
    return session_class()


def get_pandas_conn(vender=None, mode=None, cfg_path=None):
    """
    取得pandas模式的数据库连接

    :param vender: str, 默认None, 数据库类型Vender
    :param mode: str, 默认None，环境标识
    :param cfg_path: str, 默认None，配置文件所在路径
    :return: conn，数据库对象
    """
    if cfg_path is None:
        cfg_file_path = DEFAULT_CONFIG_FILES.get('db_cfg_file').replace('#PROJECT#', get_project_root_path())
    else:
        cfg_file_path = cfg_path

    try:
        cfg = Config(path=cfg_file_path)
        if vender is None:
            vender = cfg.get('db', 'VENDER')
        if mode is None:
            # mode = cfg.get('db', 'MODE')# todo 要修改
            mode = get_app_status()
    except:
        # print('config file = {0}'.format(cfg_file_path))
        raise Exception('数据库配置文件错误!')

    if vender == 'sqlite3':
        try:
            url = 'sqlite:///' + cfg.get('db', 'sqlite3.{0}.file_path'.format(mode))
            url = url.replace('#PROJECT#', get_project_root_path())
            engine = create_engine(url)
            conn = engine.connect()
        except:
            raise Exception('sqlite3 连接失败!')
    elif vender == 'mysql':
        try:
            engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}?charset=utf8'.format(
                cfg.get('db', 'mysql.{0}.user'.format(mode)),
                cfg.get('db', 'mysql.{0}.password'.format(mode)),
                cfg.get('db', 'mysql.{0}.host'.format(mode)),
                cfg.get('db', 'mysql.{0}.db'.format(mode)),
                buffered=True

            ))
            conn = engine.connect()
        except Exception as ee:
            raise Exception('mysql 连接失败! msg = {0}'.format(str(ee)))
    else:
        raise Exception('无效的数据库VENDER')

    return conn


# =====================================================================================
# 配置工具包
class Config:
    """
    键值类型配置文件，工具包
    """

    # 配置文件对象
    _cp = None

    def __init__(self, path=None):
        """
        初始化参数
        如配置文件不存在，则抛出 IOException
        :param path: str,default:None,配置文件绝对路径
                        #PROJECT#表示项目根目录
        """

        if path is None:
            # path = get_project_root_path() + 'config' + os.path.sep + 'config.cfg'
            path = DEFAULT_CONFIG_FILES.get('config_file').replace('#PROJECT#', get_project_root_path())

        if not os.path.exists(path):
            raise Exception('路径{0}非法'.format(path))
        self._cp = ConfigParser()
        self._cp.read(path, encoding='utf-8')

    def get(self, section, key):
        """
        按 key 获得配置值字符串

        如果没有找到，则返回None

        :param section: str，section名
        :param key: str, key名
        :return: str or None
        """
        try:
            return self._cp.get(section=section, option=key)
        except:
            return None

    def get_cp(self):
        """
        获得配置对象
        :return:
        """
        return self._cp


# =====================================================================================
# 日志服务

# 调用日志器
def logger(config_file_path=None):
    """
    返回一个日志器
    :rtype:
    :param config_file_path: str 配置文件路径
    :return: logger日志器
    """
    if config_file_path is None:
        config_file_path = DEFAULT_CONFIG_FILES.get('log_config_file').replace('#PROJECT#', get_project_root_path())
    if not os.path.exists(config_file_path):
        raise Exception('日志配置文件未找到！（path={0}）'.format(config_file_path))

    logging.config.fileConfig(config_file_path)
    return logging.getLogger(LOGGER_NAME)


# 记录SQL语句
def log_sql(sql):
    """
    记录SQL语句

    :param sql: str，执行的SQL语句
    :return: None
    """

    logger().debug('SQL : {0}'.format(sql))


class DateUtils:
    """
    日期时间工具类

    """

    @staticmethod
    def today(format_datestr=DATE_DB_FORMAT):
        """
        取得系统当前日期字符串

        :param format_datestr: str，默认是数据库格式
        :return: str
        """
        return time.strftime(format_datestr, time.localtime(time.time()))

    @staticmethod
    def now(format_datestr=DATETIME_VIEW_FORMAT):
        """
        取得系统当前日期字符串

        :param format_datestr: str，默认是数据库格式
        :return: str
        """
        return time.strftime(format_datestr, time.localtime(time.time()))

    @staticmethod
    def now_db_format():
        """
        取得系统当前日期字符串

        :param format_datestr: str，默认是数据库格式
        :return: str
        """
        return time.strftime(DATETIME_DB_FORMAT, time.localtime(time.time()))

    @staticmethod
    def to_db_format(date_str):
        """
        将显示格式的日期字符 转成 数据库格式的日期字符

        :param date_str: str
        :return: str
        """
        try:
            time_struct = time.strptime(date_str, DATE_VIEW_FORMAT)
            return time.strftime(DATE_DB_FORMAT, time_struct)
        except:
            return "N/A"

    @staticmethod
    def to_view_format(db_view_str):
        """
        将数据库格式的日期字符 转成 显示格式的日期字符

        :param db_view_str:
        :return:
        """
        try:
            time_struct = time.strptime(db_view_str, DATE_DB_FORMAT)
            return time.strftime(DATE_VIEW_FORMAT, time_struct)
        except:
            return "N/A"

    
    @staticmethod
    def get_dates(start_date, end_date, date_str_formatter=DATE_DB_FORMAT):
        """
        取得日期之间的所有日期（String输出）

        包括 start_date 和 end_date 两个日期

        param start_date: str yyyyMMdd 格式，开始日期（包括）
        param end_date: str yyyyMMdd 格式，结束日期（包括）
        date_str_formatter: str，默认为yyyyMMdd
        return : list of str, 之间的所有日期列表，按早到晚排序
        """
        try:
            start_dt = datetime.datetime.strptime(start_date, DATE_DB_FORMAT) 
            end_date = datetime.datetime.strptime(end_date, DATE_DB_FORMAT) 
            if start_dt>end_date:
                start_dt,end_date = end_date,start_dt

            return_dates = []
            for i in range((end_date - start_dt).days+1):
                day = start_dt + datetime.timedelta(days=i)
                return_dates.append( datetime.datetime.strftime(day, date_str_formatter) )

            return return_dates
        except :
            return []


class DbUtils:
    """
    数据库工具类
    """

    @staticmethod
    def execute_sql(sql, conn=None, is_log=False, is_commit=True):
        """
        执行SQL语句

        参数SQL如果是单个String则执行单个语句，如果是list则执行多个语句

        :param sql: string or list of string，执行的SQL语句
        :param conn: 数据库连接,默认为空则从配置文件中取
        :param is_log: bool, 是否记日志，默认为False
        :param is_commit: bool，是否提交，默认为是（如果失败，自动回滚）
        :return: None
        :raise: Exception 执行过程中的异常
        """
        # 处理sql
        if sql is None or len(sql) == 0:
            raise Exception('执行SQL语句为空！')
        sql_list = []  # 真正执行的列表
        if type(sql) is str:
            sql_list.append(sql)
        elif type(sql) is list:
            sql_list = sql

        # 数据库连接
        _conn = conn
        try:
            if conn is None:
                _conn = get_conn()
        except Exception as e:
            raise Exception('数据库连接失败！' + str(e))
        try:
            cur = _conn.cursor()
            for single_sql in sql_list:
                if is_log:
                    log_sql(single_sql)
                cur.execute(single_sql)
            if is_commit:
                _conn.commit()
                if is_log:
                    logger().debug('数据库提交')
            cur.close()
        except Exception as e:
            logger().error('SQL执行异常，{0}'.format(str(e)))
            if is_commit:
                _conn.rollback()
                if is_log:
                    logger().debug('数据库回滚')
        finally:
            if conn is None:
                _conn.close()


    @staticmethod
    def query(sql, conn=None, is_log=False, dictionary=True):
        """
        执行SQL查询，返回记录集

        :param sql: str，执行的单个SELECT SQL语句
        :param conn: 数据库连接,默认为空则从配置文件中取
        :param is_log: bool, 是否记日志，默认为False
        :param dictionary: bool, 默认True，默认返回dict可用字段名查询，False则返回list，用索引号查询
        :return: dictionary or list
        """

        # 数据库连接
        _conn = conn
        try:
            if conn is None:
                _conn = get_conn()
        except Exception as e:
            raise Exception('数据库连接失败！' + str(e))
        try:
            cur = _conn.cursor(dictionary=dictionary)
            if is_log:
                log_sql(sql)
            cur.execute(sql)
            record_set = cur.fetchall()
            cur.close()

            return record_set
        except Exception as e:
            logger().error('SQL执行异常，{0}'.format(str(e)))
        finally:
            if conn is None:
                _conn.close()


    @staticmethod
    def query_count(table_name, where_sql=None, conn=None, is_log=False):
        """
        查询 某表总记录数

        :param table_name: str，表名
        :param where_sql: str，条件语句
        :param conn: connection ，默认为None使用配置文件中定义内容，数据库连接
        :param is_log: bool, 是否记日志，默认为False
        :return: int 记录数
        """
        sql = "select count(*) as  count_all from {table_name} ".format(table_name=table_name)
        if where_sql is not None:
            sql += " where " + where_sql
        data = DbUtils.query(sql=sql, conn=conn, is_log=is_log)
        if data is not None and len(data) > 0:
            return data[0]["count_all"]
        else:
            raise Exception('运算错误')


    @staticmethod
    def has_table(table_name, con=None):
        """
        按表名查询表是否存在

        :param table_name: str，表名
        :param con: connection，数据库连接，如果为空则使用配置文件
        :return: boolean
        """
        if table_name is None:
            return False

        if con is None:
            con = get_conn()
        sql = "SELECT TABLE_NAME "
        sql += " from information_schema.TABLES  "
        sql += " where table_schema='{db_name}' AND TABLE_NAME='{table_name}' AND table_type='BASE TABLE' " \
            .format(table_name=table_name, db_name=con.database)
        # print(sql)
        rs = DbUtils.query(sql)
        if len(rs) == 0:
            return False
        else:
            return True



def get_app_status():
    """
    取得当前应用的环境，如DEV、TEST、
    """
    return Config().get(section="app", key="APP_STATUS")
