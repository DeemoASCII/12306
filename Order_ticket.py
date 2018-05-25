#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-25 上午11:05
# @Author  : Elara
# @Site    : 
# @File    : Order_ticket.py
# @Software: PyCharm
import json
import re
from datetime import datetime
from urllib.parse import unquote

from twilio.rest import Client

from config import s, headers, train_data, from_station, to_station, submit_seat, name, idendity, mobile, user_num, \
    phonenumber


class Order_ticket(object):
    '''
    购买车票
    '''

    def __init__(self, train_information, seat):
        self.train_information = train_information
        self.secretStr = train_information[0]
        self.REPEAT_SUBMIT_TOKEN = ''
        self.key_check_isChange = ''
        self.seat = seat

    def check_user(self):
        '''
        检查用户是否登陆
        :return:
        '''
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = {
            '_json_att=': ''
        }
        res = s.post(url, data=data, headers=headers, verify=False)
        # print(res.text)

    def submit_order(self):
        '''
        提交购票请求
        :return:
        '''
        # print(self.secretStr)
        self.secretStr = unquote(self.secretStr)
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': self.secretStr,
            'train_date': train_data,
            'back_train_date': train_data,
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': from_station,
            'query_to_station_name': to_station,
            'undefined': '',
        }
        res = s.post(url, data=data, headers=headers, verify=False)
        url1 = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {
            '_json_att': ''
        }
        res = s.post(url1, data=data, headers=headers, verify=False)
        # print(res.text)
        return res.text

    def parse(self, html):
        '''
        对购票页面信息解析
        :param html:
        :return:
        '''
        reg1 = re.compile(r'globalRepeatSubmitToken = \'(.*?)\'', re.S)
        self.REPEAT_SUBMIT_TOKEN = re.findall(reg1, html)[0]
        reg2 = re.compile(r'\'key_check_isChange\':\'([\s\S]*?)\'', re.S)
        self.key_check_isChange = re.findall(reg2, html)[0]

    def check_info(self):
        '''
        确认信息是否正确页面
        :return:
        '''
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': '{},0,1,{},1,{},{},N'.format(submit_seat[self.seat], name, idendity, mobile),
            'oldPassengerStr': '{},1,{},{}_'.format(name, idendity, user_num),
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN,
        }
        res = s.post(url, data=data, headers=headers, verify=False)
        print(res.text)

    def get_count(self):
        '''
        确认数量
        :return:
        '''
        global train_data
        year_s, mon_s, day_s = train_data.split('-')
        data_time = datetime(int(year_s), int(mon_s), int(day_s))
        data_time = datetime.strftime(data_time, '%a %b %d %Y %X')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            'train_date': '{} GMT+0800 (CST)'.format(data_time),
            'train_no': self.train_information[2],
            'stationTrainCode': self.train_information[3],
            'seatType': '{}'.format(submit_seat[self.seat]),
            'fromStationTelecode': self.train_information[6],
            'toStationTelecode': self.train_information[7],
            'leftTicket': self.train_information[12],
            'purpose_codes': '00',
            'train_location': self.train_information[15],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN,
        }
        res = s.post(url, data=data, headers=headers, verify=False)
        print(res.text)

    def confirm_order(self):
        '''
        确认提交
        :return:
        '''
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            'passengerTicketStr': '{},0,1,{},1,{},{},N'.format(submit_seat[self.seat], name, idendity, mobile),
            'oldPassengerStr': '{},1,{},{}_'.format(name, idendity, user_num),
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.train_information[12],
            'train_location': self.train_information[15],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN,
        }
        res = s.post(url, data=data, headers=headers, verify=False)
        html = json.loads(res.text)
        if html['data']['submitStatus']:
            print('订票成功啦！请30分钟内到官网进行支付')
            return Order_ticket.message()

    @staticmethod
    def message():
        '''
        发送短信的方法
        :return:
        '''
        account_sid = 'AC0e807460f2cbb139a10ce253a5fda9dd'
        auth_token = '64baa89b33b3e01f6b83d31f9b342a6c'
        client = Client(account_sid, auth_token)

        client.messages.create(to="+86{}".format(phonenumber),  # 区号+你的手机号码
                               from_="17372043030",  # 你的 twilio 电话号码
                               body="Little cutie you have booked successfully,now you have 30 minutes to pay it,please go to the official website to pay it!")

    def main(self):
        self.check_user()
        html = self.submit_order()
        self.parse(html)
        self.check_info()
        self.get_count()
        self.confirm_order()


if __name__ == '__main__':
    Order_ticket.message()
