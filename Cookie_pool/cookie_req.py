import json
import os

import requests
from soupsieve.util import string
from account_saver import RedisClient

CONN = RedisClient('account', 'pkulaw')
CONNA = RedisClient('cookies', 'pkulaw')

USERNAME = ''
USERPASSWORD = ''


def first_login_reqck(username, userpassword):
    global cookieID
    url1 = 'https://www.pkulaw.cn/case/CheckLogin/Login'

    data1 = {
        'Usrlogtype': '1',
        'ExitLogin': '',
        'menu': 'case',
        'CookieId': '',
        'UserName': username,
        'PassWord': userpassword,
        'jz_id': '0',
        'jz_pwd': '0',
        'auto_log': '0'
    }

    data2 = {
        'Usrlogtype': '1',
        'ExitLogin': '',
        'menu': 'case',
        'CookieId': 'gwqimjpsnpemccguu4ns3d0d',
        'UserName': '',
        'PassWord': '',
        'jz_id': '',
        'jz_pwd': '',
        'auto_log': ''
    }

    headers1 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '113',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Host': 'www.pkulaw.cn',
        'Origin': 'https://www.pkulaw.cn',
        'Referer': 'https://www.pkulaw.cn/Case/',
        'sec-ch-ua': '"Google Chrome 79"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    headers2 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '112',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'ASP.NET_SessionId=gwqimjpsnpemccguu4ns3d0d; CookieId=gwqimjpsnpemccguu4ns3d0d; QINGCLOUDELB=0c115dd3e70db1dd010b1763523580a8eb34b25dd41eaed32dbb495bb1e757e5',
        'DNT': '1',
        'Host': 'www.pkulaw.cn',
        'Origin': 'https://www.pkulaw.cn',
        'Referer': 'https://www.pkulaw.cn/Case/',
        'sec-ch-ua': '"Google Chrome 79"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.Session( )
        res = response.post(url = url1, data = data1, headers = headers1, timeout = 10)
        cookies1 = res.cookies.get_dict( )
        cookieId = cookies1.get('CookieId')
        print('CookieId: ' + string(cookieId))
        cookieID = cookieId
        print('firstlogcookie: ' + string(cookies1))
        with open('./Cookies/firstlogCookie.txt', 'w', encoding = 'utf-8') as f:
            for key, value in cookies1.items( ):
                f.write(key + "=" + string(value) + "; ")
        f.close( )
        with open('./Cookies/firstlogCookie.txt', 'rb+') as f1:
            f1.seek(-2, os.SEEK_END)
            f1.truncate( )
        f1.close( )
    except Exception as e1:
        print("Error1: " + string(e1))
        pass

    try:
        with open('./Cookies/firstlogCookie.txt', 'r', encoding = 'utf-8') as f2:
            cookies2 = f2.readline( )
            print("cookies2: " + string(cookies2))
            print("headers2: " + string(headers2))
            headers2.update(Cookie = cookies2)
            print("headers2: " + string(headers2))
            print("data2: " + string(data2))
            data2.update(CookieId = cookieID)
            print("data2: " + string(data2))
        f2.close( )
        response1 = requests.Session( )
        res1 = response1.post(url = url1, data = data2, headers = headers2, timeout = 10)
        return cookies2
    except Exception as e2:
        print("error2: " + string(e2))
        pass


class pkulaw_cookie_req(object):
    def __init__(self, username=USERNAME, userpassword=USERPASSWORD):
        self.username = username
        self.userpassword = userpassword

    def get_cookie(self):
        usernames = CONN.scan( )
        for username in usernames:
            print(username)
        # userpassword = username
        # print(username,userpassword)
        # cookie = first_login_reqck(username,userpassword)
        # print(cookie)
        # cj = json.dumps(cookie)
        # print(cj)
        # CONNA.set('cookieID:'+username, cj)


pk = pkulaw_cookie_req()
pk.get_cookie()