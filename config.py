#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-24 下午8:26
# @Author  : Elara
# @Site    : 
# @File    : config.py
# @Software: PyCharm

import requests
from fake_useragent import UserAgent

s = requests.session()
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}
# 超级鹰的账户信息，自行修改
Chaojiying_username = ''
Chaojiying_password = ''
Chaojiying_soft_id = 1
# 验证码类型
Chaojiying_kind = 9004

# 12306登陆的账号密码
username = ''
password = ''

# 出发站点
from_station = '长沙'
# 到达站点
to_station = '武汉'
# 购买日期
train_data = '2018-06-22'

# 建立的火车座位信息，不要修改
train_seat = {
    '车次': 3,
    '出发时间': 8,
    '到达时间': 9,
    '坐车历时': 10,
    '一等座': 31,
    '二等座': 30,
    '硬卧': 28,
    '软卧': 23,
    '硬座': 29,
    '无座': 26
}
# 选择要购买的火车，可以输入多个中间用空格隔开
# 动车票暂时购买流程还没完成，请不要选择动车
trains = ['G864']
# 选择要购买的座位，可以输入多个中间用空格隔开
seats = ['二等座']

# 购买的座次代码，不要修改
submit_seat = {
    '硬卧': '3',
    '软卧': '4',
    '硬座': '1',
    '二等座': 'O',
    '一等座': 'M',
    '特等座': 'P'
}

# 一定要是在官网添加过信息的购票人才行，不能随意填写
# 购票人姓名
name = ''
# 购票人身份证
idendity = ''
# 购票人手机号码
mobile = ''
# 购票人序号
user_num = ''

# 接收通知的手机号
phonenumber = ''
