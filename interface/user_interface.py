"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/29 20:22
    @Author  : zhongxiaoting
    @Site    : 
    @File    : user_interface.py
    @Software: PyCharm
"""
import json
import os

from db import db_handler
from lib import common

"""
    用户数据层，接口层
"""


# 注册接口
def register_interface(username, password, balance=15000):
    # 判断用户是否存在
    user_dic = db_handler.select(username)
    # 用户若存在，返回False，重新输入
    if user_dic:
        return False, f'{username}已存在'
    # 对密码进行加密
    password = common.get_pwd_md5(password)
    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,  # 用户余额
        'flow': [],  # 用户流水列表
        'shop_cart': {},  # 购物车记录
        'locked': False,  # Flase用户未被冻结，True用户被冻结
    }

    # 保存数据
    db_handler.save(user_dic)
    # 返回True
    return True, f'{username}注册成功！请登录！'


# 登录接口
def login_interface(username, password):
    # 查看用户是否存在
    user_dic = db_handler.select(username)
    res = {'flag': 0, 'msg': f'用户：{username} 不存在！请先注册！'}
    # 判断用户是否存在
    if user_dic:
        # 判断用户是否被冻结
        if user_dic['locked']:
            res = {'flag': 3, 'msg': f"用户:{username} 已经被冻结！"}
        else:
            # 用户存在，存在验证密码是否正确
            # 对输入的密码进行加密
            password = common.get_pwd_md5(password)
            if password == user_dic.get("password"):
                res = {'flag': 1, 'msg': f'用户：{username} 登录成功！'}
            # 密码错误
            else:
                res = {'flag': 2, 'msg': '密码错误，请重新输入！'}
    return res


# 查询余额接口
def check_bal_interface(username):
    user_dic = db_handler.select(username)
    return user_dic['balance']

