"""
    -*- coding: utf-8 -*-
    @Time    : 2021/7/4 16:29
    @Author  : zhongxiaoting
    @Site    : 
    @File    : admin_interface.py
    @Software: PyCharm
"""

from db import db_handler


# 管理员修改用户金额
def change_balance_interface(username, money):
    # 判断用户输入的是否是数字
    if not money.isdigit():
        return False, "输入错误，请重新输入！"
    # 判断用户是否存在
    user_dic = db_handler.select(username)
    if user_dic:
        # 修改用户金额
        user_dic['balance'] = int(money)
        db_handler.save(user_dic)
        return True, f"修改用户 {username} 的金额成功！"
    return False, f"修改的用户 {username} 不存在，请重新输入!"


# 冻结用户
def lock_user_interface(username):
    # 判断用户是否存在
    user_dic = db_handler.select(username)
    if user_dic:
        user_dic['locked'] = True
        db_handler.save(user_dic)
        return True, f"用户 {username} 冻结成功！"
    return False, f"用户 {username} 不存在！请重新输入！"
