#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-24 下午10:24
# @Author  : Elara
# @Site    : 
# @File    : Query_ticket.py
# @Software: PyCharm
import json
import time
from urllib.parse import unquote

import urllib3

from config import s, headers, from_station, to_station, train_data, train_seat, trains, seats
from station import station_name

urllib3.disable_warnings()


class Queryticket(object):
    '''
    查询余票
    '''

    def __init__(self):
        self.station1, self.station2 = Queryticket.train_station()
        self.from_station = self.station1[from_station]
        self.to_station = self.station1[to_station]
        self.train_data = train_data
        self.train_desc = {}

    @staticmethod
    def train_station():
        '''
        对车站信息做一个整理
        :return:
        '''
        global station_name
        station_name = station_name.split('@')
        train_stations1 = {}
        train_stations2 = {}
        for i in station_name[1:]:
            i = i.split('|')
            train_stations1[i[1]] = i[2]
            train_stations2[i[2]] = i[1]
        return train_stations1, train_stations2

    def query_station(self):
        '''
        查询车次信息
        :return:
        '''
        url = 'https://kyfw.12306.cn/otn/leftTicket/query'
        data = {
            'leftTicketDTO.train_date': self.train_data,
            'leftTicketDTO.from_station': self.from_station,
            'leftTicketDTO.to_station': self.to_station,
            'purpose_codes': 'ADULT',
        }
        res = s.get(url, params=data, headers=headers, verify=False)
        result = json.loads(res.text)['data']['result']
        if result:
            return result
        else:
            print('很抱歉，按您的查询条件，当前未找到从{}到{}的列车。清重试'.format(self.station2[self.from_station],
                                                          self.station2[self.to_station]))
            exit()

    def parse_station(self, result):
        '''
        解析查询结果
        :return:
        '''
        train_informations = []
        for station_detial in result:
            train_information = str(station_detial).split('|')
            train_informations.append(train_information)
        return train_informations

    def left_ticket(self, train_informations):
        '''
        检测余票并且购买
        :param train_informations:
        :return:
        '''
        for train_information in train_informations:
            self.train_desc[train_information[3]] = train_information
            # print('车次{},出发时间：{},到达时间：{},软卧车票剩余：{},硬卧车票剩余：{},硬座车票剩余：{},无座车票剩余：{}'.format(train_information[3],
            #                                                                             train_information[8],
            #                                                                             train_information[9],
            #                                                                             train_information[23],
            #                                                                             train_information[28],
            #                                                                             train_information[29],
            #                                                                             train_information[26]))
        try:
            for train in trains:
                for seat in seats:
                    if self.train_desc[train][train_seat[seat]] != '无' and self.train_desc[train][
                        train_seat[seat]] != '':
                        print('车次{}有{}票{}张，将为你购买'.format(self.train_desc[train][3], seat,
                                                         self.train_desc[train][train_seat[seat]]))
                        return self.train_desc[train_information[3]], seat
                    else:
                        print('车次{}暂无余票，重新检测'.format(self.train_desc[train][3]))
                        time.sleep(1)
                        return self.main()
        except KeyError:
            print('车次信息输入有误，清检查过后重新输入')
            exit()

    def main(self):
        result = self.query_station()
        train_informations = self.parse_station(result)
        train_information, seat = self.left_ticket(train_informations)
        print(train_information)
        return train_information, seat


if __name__ == '__main__':
    test = Queryticket()
    test.main()
