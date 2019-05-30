#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
md文件工具函数集合

@File    :   md_utils.py
@Time    :   2019/05/30 21:43:54
@Author  :   Jeffrey Wang
@Version :   1.0
@Contact :   shwangjj@163.com
@Desc    :   None
'''

# here put the import lib
import os


def del_blank_lines(file, blank_line_limit=2):
    """
    删除源文件中多余的空行，默认2行以上空行删除到只剩1行

    param file: str，文件路径
    param blank_line_limit: int，遇到几个空行要删除
    return:
    """
    DEL_LINE_FLAG = 'DEL_THIS_LINE'
    if os.path.exists(file) == False:
        print("文件{0}不存在".format(file))
        return
    
    # 给空行做标记
    with open(file,"r",encoding="UTF-8") as f:
        lines = f.readlines()
        blank_lines = 0     # 空行计数
        for no, line in enumerate(lines):
            if line.replace(" ", "") == '\n':
                blank_lines += 1
                if blank_lines > (blank_line_limit-1):
                    lines[no] = DEL_LINE_FLAG
            else:
                blank_lines = 0
    
    # 删除空行
    print('共删除空行{0}行'.format(lines.count(DEL_LINE_FLAG)))
    while range(lines.count(DEL_LINE_FLAG)):
        lines.remove(DEL_LINE_FLAG)

    # 输出
    with open(file,"w",encoding="UTF-8") as f_out:
        f_out.writelines(lines)
    

if __name__ == "__main__":
    dir = "C:\\github\\lgqm_story\\同人作品\\看不见的敌人\\"
    file = dir + "看不见的敌人•第1节 消失的老毕.md"

    del_blank_lines(file)
