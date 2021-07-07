"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/28 20:47
    @Author  : zhongxiaoting
    @Site    : 
    @File    : start.py
    @Software: PyCharm
"""

"""
程序入口
"""
import os
import sys
from core import src
# 添加解释器的环境变量
sys.path.append(os.path.dirname(__file__))


# 开始执行项目程序
if __name__ == '__main__':
    src.run()



