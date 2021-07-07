"""
    -*- coding: utf-8 -*-
    @Time    : 2021/7/1 21:04
    @Author  : zhongxiaoting
    @Site    : 
    @File    : bank_interface.py
    @Software: PyCharm
"""
from db import db_handler

# 提现功能接口（手续费5%）
def withdraw_interface(username, money):
    # 获取账户中的金额
    money = int(money)
    user_dic = db_handler.select(username)
    balance = user_dic.get('balance')
    # 提现 + 本金
    wd_money = money * 1.05
    # 修改账户的金额
    if balance < wd_money:
        return False, '余额不足，请重新输入！'

    user_dic['balance'] -= wd_money
    # 记录流水
    flow = f'用户：{username} 提现金额￥{money}成功！'
    user_dic["flow"].append(flow)

    # 修改保存
    db_handler.save(user_dic)
    return True, flow


# 还款功能接口
def repay_interface(username, money):
    # 判断是否大于0
    money = int(money)
    if money <= 0:
        # 调用还款接口
        return False, "输入的还款金额不能小于等于0"

    # 获取原有字典中的存款
    user_dic = db_handler.select(username)
    balance = user_dic.get("balance")
    # 修改字典中的金额
    user_dic['balance'] = money + balance
    # 记录流水
    flow = f"用户：{username} 还款金额为￥{money}"
    user_dic['flow'].append(flow)
    # 保存
    db_handler.save(user_dic)
    return True, flow


# 转账功能接口 (手续费1%）
def transfer_interface(username, to_user, money):
    # 判断转账对象是否存在，金额是否大于0
    to_user_dic = db_handler.select(to_user)
    if not to_user_dic:
        return False, f"被转账的对象用户 {to_user} 不存在！"
    money = int(money)
    if money <= 0:
        return False, f"转账的金额不能小于等于0！"
    to_user_balance = to_user_dic.get("balance")
    # 用户金额
    user_dic = db_handler.select(username)
    user_balance = user_dic.get("balance")

    # 判断转账金额小于存款 转账人的存款 - 转账金额
    if user_balance < money * 1.01:
        return False, f"转账金额不足，请重新输入！"
    user_dic['balance'] = user_balance - money * 1.01
    # 被转账对象 + 转账金额
    to_user_dic['balance'] = to_user_balance + money
    # 记录流水
    user_dic_flow = f"用户：{username} 转账 ￥{money} 给用户 {to_user} 成功！"
    user_dic['flow'].append(user_dic_flow)
    to_user_flow = f"用户：{to_user} 收到用户 {username} 转账￥{money} ！"
    to_user_dic['flow'].append(to_user_flow)
    # 保存
    db_handler.save(user_dic)
    db_handler.save(to_user_dic)
    return True, user_dic_flow


# 记录流水接口
def check_flow_interface(username):
    user_dic = db_handler.select(username)
    return user_dic.get("flow")


# 支付接口
def pay_interface(username, cost):
    # 查看用户余额
    user_dic = db_handler.select(username)
    # 判断用户余额是否大于消费总价
    balance = user_dic.get("balance")
    balance = int(balance)
    if balance >= cost:
        balance -= cost
        # 记录流水
        flow = f"用户：{username} 消费了 ￥{cost}"
        user_dic["flow"].append(flow)
        # 余额
        user_dic['balance'] = balance
        # 清除购物车
        user_dic['shop_cart'].clear()
        # 保存数据
        db_handler.save(user_dic)
        return True
    return False