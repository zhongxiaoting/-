"""
    -*- coding: utf-8 -*-
    @Time    : 2021/6/28 20:53
    @Author  : zhongxiaoting
    @Site    : 
    @File    : src.py
    @Software: PyCharm
"""
from conf import setting
from interface import user_interface, bank_interface, shop_interface
from lib import common

# 全局变量，判断用户是否登录
user_login = None

# 1、注册功能
def register():
    while True:
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        identify_password = input("请再次确认密码：").strip()
        # 判断密码是否一致
        if password == identify_password:
            # 调用用户数据接口层
            # flag 接收是否注册成功，msg接收信息
            flag, msg = user_interface.register_interface(username, password)
            # 根据用户flag判断用户是否注册成功
            if flag:
                print(msg)
                break
            else:
                print(msg)


# 2、登录功能
def login():
    while True:
        # 输入数据
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()

        # 判断用户是否登录成功,flag 为0表示用户不存在，1表示登录成功，2表示密码错误,3表示账户被冻结
        res = user_interface.login_interface(username, password)
        # print(res['msg'])

        if res['flag'] == 1:  # 登录成功
            print(res['msg'])
            global user_login
            user_login = username
            break
        elif res['flag'] == 2:  # 密码错误
            print(res['msg'])
            continue
        elif res['flag'] == 3:  # 账户被冻结
            print(res['msg'])
            break
        else:
            print(res['msg'])
            register()  # 注册用户



# 3、查看余额
@common.login_auth
def check_balance():

    balance = user_interface.check_bal_interface(user_login)
    print(f'用户: {user_login}的账户余额为: {balance} 元')



# 4、提现功能
@common.login_auth
def withdraw():
    while True:
        # 用户输入提现的金额数
        input_money = input("请输入金额：").strip()
        # 判断用户输入的是否为数字
        if not input_money.isdigit():
            print("请重新输入！")
            continue
        # 用户提现金额交给接口层来操作
        flag, msg = bank_interface.withdraw_interface(user_login, input_money)
        if flag:
            balance = user_interface.check_bal_interface(user_login)
            print(msg)
            print(f'用户: {user_login} 的账户余额为: {balance} 元')
            break
        else:
            print(msg)
            continue



# 5、还款功能
@common.login_auth
def repay():
    while True:
        # 输入还款金额
        input_money = input("请输入还款金额：").strip()
        # 判断是否是数字
        if not input_money.isdigit():
            print("请重新输入！")
            continue
        flag, msg = bank_interface.repay_interface(user_login, input_money)
        if flag:
            balance = user_interface.check_bal_interface(user_login)
            print(msg)
            print(f'用户: {user_login} 的账户余额为: {balance} 元')
            break
        else:
            print(msg)
            continue



# 6、转账功能
@common.login_auth
def transfer():
    while True:

        """
        1、转账的对象
        2、转账的金额
        :return:
        """
        to_user = input("请输入转账的对象：")
        input_money = input("请输入转账的金额：")
        # 调用转账数据接口层
        flag, msg = bank_interface.transfer_interface(user_login, to_user, input_money)
        if flag:
            balance = user_interface.check_bal_interface(user_login)
            print(msg)
            print(f'用户: {user_login} 的账户余额为: {balance} 元')
            break
        else:
            print(msg)
            continue


# 7、查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(user_login)
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print("当前用户没有流水！")


# 8、购物功能
@common.login_auth
def shopping():
    shopping_car = {}
    # 创建一个商品列表
    shop_list = [
        ['苹果', 5],
        ['天津狗不理包子', 20],
        ['华硕电脑飞行者', 5400],
        ['广东凤爪', 30],
        ['西瓜', 2]
    ]
    while True:
        print("================欢迎来到有趣购物商城======================")
        # 打印商品供用户选择
        for index, shop in enumerate(shop_list):
            shop_name, shop_price = shop
            print(f'编号: {index}', f'  商品名: {shop_name}', f' 价格: {shop_price}')
        print("====================24小时服务哦=========================")
        # 用户输入的选择
        choice = input("请输入要购买的编号（是否结算 y or n）：")
        # 判断是否结算或者加购物车

        if choice == 'y':
            # 加购物车，调用购物车接口
            shop_interface.add_shop_cart_interface(user_login, shopping_car)

            # 获取购物车的接口
            flag = shop_interface.get_shop_car(user_login)
            if flag:
                # 结算，调用商城接口
                flag, msg = shop_interface.shopping_interface(user_login, flag)
                if flag:
                    print(msg)
                    break
                else:
                    print(msg)
            else:
                print("购物车空空如也！不能支付！")
                continue
        # 将商品添加进购物车
        if choice == 'n':
            # 判断购物车是否为空
            if not shopping_car:
                print("购物车是空的，不能添加，请重新输入！")
                continue
            # 加购物车，调用购物车接口
            flag, msg = shop_interface.add_shop_cart_interface(user_login, shopping_car)
            if flag:
                print(msg)
                break

        # 判断是否是数字
        if not choice.isdigit():
            print("请输入正确的编号！")
            continue
        choice = int(choice)
        # 判断是否在列表中
        if choice not in range(len(shop_list)):
            print("请输入正确的编号！")
            continue
        # 获取商品的商品名和单价
        shop_name, shop_price = shop_list[choice]
        # 加入购物车
        # 判断商品是否重复，重复数量+1
        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1
        else:
            # 默认数量为1
            shopping_car[shop_name] = [shop_price, 1]
        # 打印出购物车的商品
        print(shopping_car)


            


# 9、查看购物车
@common.login_auth
def check_shop_cart():
    flag = shop_interface.get_shop_car(user_login)
    if flag:
        print(flag)
    else:
        print("购物车空空如也！")



# 10、管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.admin_run()


# 视图层函数
def run():
    # 创建函数功能字典
    func_dic = {
        '1': register,
        '2': login,
        '3': check_balance,
        '4': withdraw,
        '5': repay,
        '6': transfer,
        '7': check_flow,
        '8': shopping,
        '9': check_shop_cart,
        '10': admin
    }

    # 选择功能菜单
    while True:
        print(
            """
    =============功能菜单================
       ******** 1、注册功能    ********
       ******** 2、登录功能    ********
       ******** 3、查看余额    ********
       ******** 4、提现功能    ********      
       ******** 5、还款功能    ********
       ******** 6、转账功能    ********
       ******** 7、查看流水    ********
       ******** 8、购物功能    ********
       ******** 9、查看购物车  ********
       ******** 10、管理员功能 ********
    ====================================
            """
        )

        choice = input("请输入功能编号：")
        if choice not in func_dic:
            print("请输入正确的编号")
            continue

        # 如果在的话，访问函数
        func_dic.get(choice)()  # 相当于login()
