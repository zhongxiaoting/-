"""
    -*- coding: utf-8 -*-
    @Time    : 2021/7/4 16:18
    @Author  : zhongxiaoting
    @Site    : 
    @File    : admin.py
    @Software: PyCharm
"""

from core import src
from interface import admin_interface


# 添加账户
def add_user():
    src.register()


# 修改用户额度
def change_balance():
    while True:

        # 输入修改的用户名，金额
        username = input("请输入需要修改的用户名：").strip()
        money = input("请输入需要修改的金额：").strip()
        flag, msg = admin_interface.change_balance_interface(username, money)
        if flag:
            print(msg)
            break
        else:
            print(msg)
            continue


# 冻结用户
def lock_user():
    # 冻结用户
    username = input("请输入要冻结的用户：").strip()
    flag, msg = admin_interface.lock_user_interface(username)
    if flag:
        print(msg)
    else:
        print(msg)

admin_dic = {
    '1': add_user,
    '2': change_balance,
    '3': lock_user,
    '4': None
}

def admin_run():
    while True:
        print(
            """
            1、添加账户
            2、修改用户额度
            3、冻结账户
            4、退出
            """
        )

        choice = input("请输入功能编号：")
        if choice not in admin_dic:
            print("请输入正确的编号！")
            continue
        if choice == '4':
            break
        admin_dic.get(choice)()
