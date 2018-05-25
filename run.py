#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-24 下午10:25
# @Author  : Elara
# @Site    : 
# @File    : run.py
# @Software: PyCharm

import Login
import Query_ticket
import Order_ticket


def main():
    test1 = Login.Login12306()
    test1.main()
    test2 = Query_ticket.Queryticket()
    train_information,seat = test2.main()
    test3 = Order_ticket.Order_ticket(train_information,seat)
    test3.main()


if __name__ == '__main__':
    main()
