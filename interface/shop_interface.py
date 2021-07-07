"""
    -*- coding: utf-8 -*-
    @Time    : 2021/7/6 20:55
    @Author  : zhongxiaoting
    @Site    : 
    @File    : shop_interface.py
    @Software: PyCharm
"""

"""
商城接口
"""
from interface import bank_interface
from db import db_handler


# 商品文件中购物车的商品数量
def get_shop_car(username):
    user_dic = db_handler.select(username)
    # 判断是否有商品
    shop_cart = user_dic.get("shop_cart")
    if not shop_cart:
        return False
    return shop_cart





# 商品准备接口
def shopping_interface(username, shopping_cart):
    cost = 0
    # 商品的个数和价格
    for price_number in shopping_cart.values():
        price, number = price_number

        # 总价格
        cost += price * number

    # 银行结算接口
    flag = bank_interface.pay_interface(username, cost)
    if flag:
        return True, f"支付成功，用户：{username} 消费 ￥{cost}"
    else:
        return False, "支付失败，余额不足！"


# 将商品添加进购物车
def add_shop_cart_interface(username, shop_car):
    # 判断原有的文件中购物车是否有数据
    user_dic = db_handler.select(username)
    # 判断当前用户选择的商品是否存在
    for shop_name, price_number in shop_car.items():
        # 商品名称在购物车中，+1
        if shop_name in user_dic['shop_cart']:
            user_dic['shop_cart'][shop_name][1] += price_number[1]
        # 商品不在购物车中,更新到购物车中
        else:
            user_dic['shop_cart'].update({shop_name: price_number})
    # 保存数据
    db_handler.save(user_dic)
    return True, f"添加购物车成功！"

