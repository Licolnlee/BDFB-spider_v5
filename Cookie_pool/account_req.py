import json
import os
from urllib.parse import urlencode
from account_saver import RedisClient
from cssselect import xpath
from lxml import html, etree
from pyquery import PyQuery as pq

import chardet
import requests
import redis
import re
import bs4
from soupsieve.util import string

USERNAME = 'kouzui98'
USERPASSWORD = 'Windows10'
REQ_ID = '659'
REQ_TITLE = '法律数据库'
BASE_URL = 'http://520myfuture.com/db/goEntrance?'
CONN = RedisClient('account', 'pkulaw')

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '520myfuture.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

D_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    # 'Connection': 'keep-alive',
    'DNT': '1',
    # 'Host': 'www.mcnki.com',
    # 'Referer': 'http://www.mcnki.com/BDFB3/FBGWW.html',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

DATA = {
    'id': '',
    'title': ''
}

GETB_DATA = {
    'userName': '',
}


def dict_format(filepath, dict_1):
    try:
        with open(filepath, 'w', encoding = 'utf-8') as f1:
            for key, value in dict_1.items( ):
                f1.write(key + "=" + string(value) + "; ")
        f1.close( )
    except FileNotFoundError:
        print('file not exist')
        with open(filepath, 'w', encoding = 'utf-8') as f1:
            for key, value in dict_1.items( ):
                f1.write(key + "=" + string(value) + "; ")
        f1.close( )
    pass


def txt_reformat(filepath):
    try:
        with open(filepath, 'rb+') as f2:
            f2.seek(-2, os.SEEK_END)
            f2.truncate( )
        f2.close( )
    except FileNotFoundError:
        print('file not exist')
        with open(filepath, 'rb+') as f2:
            f2.seek(-2, os.SEEK_END)
            f2.truncate( )
        f2.close( )
    pass


def read_txt_header_update(filepath, headers):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f3:
            cookies = f3.readline( )
            print(cookies)
            headers.update(Cookie = cookies)
        f3.close( )
        return headers
    except FileNotFoundError:
        print('file not exist')
        with open(filepath, 'r', encoding = 'utf-8') as f3:
            cookies = f3.readline( )
            print(cookies)
            headers.update(Cookie = cookies)
        f3.close( )
        return None
    pass


def headers_json(filepath, headers):
    try:
        with open(filepath, 'w', encoding = 'utf-8') as f4:
            js = json.dumps(headers)
            f4.write(js)
        f4.close( )
        return None
    except FileNotFoundError:
        print('file not exist')
        with open(filepath, 'w', encoding = 'utf-8') as f4:
            js = json.dumps(headers)
            f4.write(js)
        f4.close( )
        return None
    pass


def test_req():
    res = requests.get('http://www.mcnki.com/BDFB3/FBGW1.html', D_HEADERS)
    content = decode_content(res.content)
    print(content)
    return content


def decode_content(html):
    encoding = chardet.detect(html)
    content = html.decode(encoding['encoding'], 'ignore')
    return content


def parse_index(content):
    doc = pq(content)
    url = doc('frame').attr('src')
    print(url)
    return url


def parse_content():
    global context
    content = test_req()
    # dom_tree = etree.HTML(content)
    # num2 = dom_tree.xpath('//div/p[3]/strong')
    # for i in num2:
    #     context = i.text
    # print(context)
    # num = re.findall('\d+.?\d', context, re.S)
    # print(num)
    doc = pq(content)
    info = doc('strong').text()
    num = re.findall('\d+.?\d', info, re.S)
    CONN.set(num[0], num[1])
    print(info)
    print(num)


def req_content(url):
    try:
        request = requests.Session( )
        response = request.get(url = url, headers = D_HEADERS, timeout = 10)
        if response.status_code == 200:
            content = response.content
            context = decode_content(content)
            print(context)
            return context
        else:
            print(response.status_code)
            print(response.history)
            print(response.url)
            return None
    except ConnectionError:
        pass


class MyFutureConnector(object):
    def __init__(self, username=USERNAME, userpassword=USERPASSWORD, req_id=REQ_ID, req_title=REQ_TITLE):
        self.username = username
        self.userpassword = userpassword
        self.rid = req_id
        self.title = req_title

    def first_log_cookie(self):
        login_url = 'http://520myfuture.com/account/login'

        try:
            request = requests.Session( )
            response = request.get(url = login_url, headers = HEADERS, timeout = 10)
            if response.status_code == 200:
                acookie = response.cookies.get_dict( )
                os.makedirs('./Cookies/', exist_ok = True)
                with open('./Cookies/first_log_cookie.txt', 'w', encoding = 'utf-8') as f1:
                    for key, value in acookie.items( ):
                        f1.write(key + "=" + string(value))
                f1.close( )
                with open('./Cookies/first_log_cookie.txt', 'r', encoding = 'utf-8') as f2:
                    acookie = f2.readline( )
                    HEADERS.update(Cookie = acookie, Referer = login_url)
                    dict_3 = {'X-Requested-With': 'XMLHttpRequest'}
                    HEADERS.update(dict_3)
                f2.close( )
                print(HEADERS)
                print(acookie)
                return HEADERS
            else:
                print(response.history)
        except ConnectionError:
            pass

    def req_account(self, headers):
        rid = self.rid
        title = self.title

        DATA.update(id = rid, title = title)

        url = BASE_URL + urlencode(DATA)

        try:
            request = requests.Session( )
            response = request.get(url = url, data = DATA, headers = headers, timeout = 10)
            if response.url == url:
                print('return html')
                html = response.content
                content = decode_content(html)
                d_url = parse_index(content)
                context = req_content(d_url)

                # print(content)
                # print(html)
                # print(context)
                return context
            else:
                headers = self.login( )
                print(headers)
                self.req_account(headers)
                return None
        except ConnectionError:
            pass

    def getcaptcha(self):
        username = self.username
        getb_url = 'http://520myfuture.com/ACCOUNT/GetCaptcha?'

        GETB_DATA.update(userName = username)
        getb_url = getb_url + urlencode(GETB_DATA)

        headers = self.first_log_cookie( )

        try:
            request = requests.Session( )
            response = request.get(url = getb_url, data = GETB_DATA, headers = headers, timeout = 10)
            if response.status_code == 200:
                print(response.url)
                print(response.history)
                headers.update(Origin = 'http://520myfuture.com')
                print(headers)
                return headers
            else:
                print(response.status_code)
                print(response.history)
                print(response.url)
                return None
        except ConnectionError:
            pass

    def login(self):
        username = self.username
        password = self.userpassword

        logindata = {
            'UsernameOrEmailAddress': username,
            'Password': password
        }

        headers = self.getcaptcha( )

        lurl = headers.get('Referer')
        print(lurl)

        try:
            request = requests.Session( )
            response = request.post(url = lurl, data = logindata, headers = headers, timeout = 10)
            if response.status_code == 200:
                cookies = response.cookies.get_dict( )
                print(cookies)
                dict_format('./Cookies/login_cookies.txt', cookies)
                txt_reformat('./Cookies/login_cookies.txt')
                headers = read_txt_header_update('./Cookies/login_cookies.txt', headers)
                headers_json('./Cookies/headers.txt', headers)
                return headers
            else:
                print(response.status_code)
                print(response.history)
                print(response.url)
                return None
        except ConnectionError:
            pass


def run():
    parse_content()
    # mc = MyFutureConnector( )
    # # mc.req_account()
    # try:
    #     with open('./Cookies/headers.txt', 'r', encoding = 'utf-8') as f:
    #         js = f.read( )
    #         headers = json.loads(js)
    #     f.close( )
    #     mc.req_account(headers)
    # except FileNotFoundError:
    #     print('file not exist')
    #     mc.req_account(HEADERS)


#
# # run( )
# # test_req()
run( )
