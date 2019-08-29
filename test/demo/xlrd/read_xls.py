#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   read_xls.py
@Time    :   2019/08/29 13:21:06
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   使用 xlrd 类库，读取 xls 文件，代码示范
'''

import xlrd
import os


FILE = os.getcwd() + '\\test\\demo\\xlrd\\lpr.xls'


def load_excel():
    """
    读取xls文件
    """
    try:
        workbook = xlrd.open_workbook( filename="xxxx.xls" )
    except FileNotFoundError as ffe:
        print( str(ffe) )
    
    

def read_sheet():
    """
    worksheet操作
    """
    try:
        workbook = xlrd.open_workbook( filename=FILE )
        
        print( "Sheet数：{0}".format(workbook.nsheets) )
        # 1
        print( "表单名列表：{0}".format(workbook.sheet_names()) )
        # ['Sheet1']
        print( "shett对象：{0}".format(workbook.sheets()) )
        # [<xlrd.sheet.Sheet object at 0x000002163AD5A710>]
        print( "按名取sheet：{0}".format(workbook.sheet_by_name('Sheet1')) )
        # <xlrd.sheet.Sheet object at 0x000001D06527A7F0>
        print( "按序号取sheet：{0}".format(workbook.sheet_by_index(0)) )
        # <xlrd.sheet.Sheet object at 0x000001D06527A7F0>

        # 获得当前活动(active)的sheet？

    except FileNotFoundError as ffe:
        print( str(ffe) )    


def read_sheet_info():
    """
    获得Sheet的信息
    """
    try:
        workbook = xlrd.open_workbook( filename=FILE )
        
        sheet = workbook.sheet_by_index(0)

        print( "总行数{0}, 总列数{1}".format( sheet.nrows, sheet.ncols ) )
        # 总行数14, 总列数3

    except FileNotFoundError as ffe:
        print( str(ffe) )    


def read_by_row():
    """
    按行读取数据示范
    """
    try:
        workbook = xlrd.open_workbook( filename=FILE )
        sheet = workbook.sheet_by_index(0)

        # 方式一：
        start_row = 0
        for row_index in range(start_row, sheet.nrows):
            line = ""
            for col_index in range(0, sheet.ncols):
                line += str(sheet.cell( row_index, col_index ).value) + "|"
            print("{0}:{1}".format( row_index+1, line ))
        # 1:日期|1Y|5Y|
        # 2:43678.39634680556|4.31|---|
        # 3:43679.39634685185|4.31|---|
        # ...

        # 方式二：
        for row_index, row in enumerate(sheet.get_rows()):
            for col_index, cell in enumerate(row):
                print("{0},{1}:{2}".format( row_index+1, col_index+1, cell.value ))
        # 1,1:日期
        # 1,2:1Y
        # 1,3:5Y
        # 2,1:43678.39634680556
        # 2,2:4.31
        # 2,3:--- 

    except FileNotFoundError as ffe:
        print( str(ffe) )  





def read_date_cells():
    """
    读取 日期类型的单元格
    """
    try:
        workbook = xlrd.open_workbook( filename=FILE )
        sheet = workbook.sheet_by_index(0)

        # 读取第2行，第1列
        print( sheet.cell(2-1, 1-1).value ) # 43678.39634680556
        dt_value = xlrd.xldate.xldate_as_datetime(sheet.cell_value(2-1, 1-1), 0)
        print( type(dt_value) ) # <class 'datetime.datetime'>
        print( dt_value )   # 2019-08-01 09:30:44.364000
        # 转换
        print( dt_value.strftime('%Y%m%d') )    # 20190801
    except FileNotFoundError as ffe:
        print( str(ffe) )  



if __name__ == "__main__":
    read_date_cells()

