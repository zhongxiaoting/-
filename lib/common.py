"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/29 21:34
    @Author  : zhongxiaoting
    @Site    : 
    @File    : common.py
    @Software: PyCharm
"""
import hashlib
from core import src

# 密码加密
def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = "一二三四五，上山打老鼠"
    md5_obj.update(salt.encode('utf-8'))
    return md5_obj.hexdigest()


# 登录功能装饰器
def login_auth(func):

    def wapper(*args, **kwargs):
        if src.user_login:
            res = func(*args, **kwargs)
        else:
            print("未登录，不能享受更多的功能")
            res = src.login()
        return res

    return wapper
