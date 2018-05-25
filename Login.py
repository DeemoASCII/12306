#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-5-24 下午8:03
# @Author  : Elara
# @Site    : 
# @File    : Login.py
# @Software: PyCharm
import json

import urllib3

import chaojiying
from config import s, headers, Chaojiying_kind, Chaojiying_password, Chaojiying_soft_id, Chaojiying_username, username, \
    password

urllib3.disable_warnings()


class Login12306(object):

    def __init__(self):
        self.pic = chaojiying.Chaojiying(Chaojiying_username, Chaojiying_password, Chaojiying_soft_id)

    '''
    登陆12306
    '''

    @staticmethod
    def get_code():
        '''
        获取12306验证码,并且将验证码保存到本地
        :return:
        '''
        code_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
        res = s.get(code_url, headers=headers, verify=False)
        print('正在获取图片验证码！')
        code = res.content
        with open('code.jpg', 'wb') as f:
            f.write(code)
        return code

    def verify_code(self):
        '''
        提交验证码进行验证
        :return:
        '''
        code_content = Login12306.get_code()
        code = self.pic.post_pic(code_content, Chaojiying_kind)
        # print(code)
        data = {
            'answer': code,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        res = s.post(check_url, data=data, headers=headers, verify=False)
        html = json.loads(res.text)
        # print(res.text)
        if html['result_code'] == '4':
            print('验证码校验成功')
            return True
        else:
            print('验证码校验失败，正在重新验证')
            return self.verify_code()

    def login(self):
        '''
        输入账号密码进行登陆
        :return:
        '''
        url1 = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': username,
            'password': password,
            'appid': 'otn'
        }
        res1 = s.post(url1, headers=headers, data=data, verify=False)
        url2 = 'https://kyfw.12306.cn/otn/login/userLogin'
        res2 = s.get(url2, headers=headers, verify=False)
        url3 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = {
            'appid': 'otn'
        }
        res3 = s.post(url3, headers=headers, data=data, verify=False)
        html = json.loads(res3.text)
        # print(html)
        newapptk = html['newapptk']
        url4 = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
            'tk': newapptk
        }
        res4 = s.post(url4, headers=headers, data=data, verify=False)
        html = json.loads(res4.text)
        if html['result_code'] == 0:
            print('账号验证通过，登陆成功')
        else:
            print('账号验证失败，清检查用户名或者密码是否有错误，再重试')
        # url5 = 'https://kyfw.12306.cn/otn/login/userLogin'
        # res5 = s.get(url5,headers=headers,verify=False)
        # print(res5.text)

    def main(self):
        self.verify_code()
        self.login()


if __name__ == '__main__':
    xiao = Login12306()
    xiao.main()
