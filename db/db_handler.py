"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/29 20:13
    @Author  : zhongxiaoting
    @Site    : 
    @File    : db_handler.py
    @Software: PyCharm
"""

"""
    数据处理层，查看数据
"""

import json
import os
from conf import setting


# 查看数据
def select(username):
    # 写入文件中,以用户的名字为文件名，更好存储多个用户信息
    # 拼接用户路径文件名
    user_path = os.path.join(setting.USER_DATA_PATH, f'{username}.json')
    # 判断用户是否存在
    if os.path.exists(user_path):
        # 打开文件，并返回给接口层
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)  # 转化为python格式
            return user_dic

    # 存在默认返回None


# 保存数据
def save(user_dic):
    # 获取到用户名
    username = user_dic.get('username')
    # 拼接用户路径文件名
    user_path = os.path.join(setting.USER_DATA_PATH, f'{username}.json')

    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)
