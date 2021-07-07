"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/28 21:55
    @Author  : zhongxiaoting
    @Site    : 
    @File    : setting.py
    @Software: PyCharm
"""

import os
# 获取项目的根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 获取db_user的目录
USER_DATA_PATH = os.path.join(BASE_PATH, 'db', 'db_user')
print(USER_DATA_PATH)