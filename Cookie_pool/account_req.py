import json
import os
import random
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor

import chardet
import requests
from pyquery import PyQuery as pq
from soupsieve.util import string

from Cookie_pool.account_saver import RedisClient

USERNAME = 'kouzui98'
USERPASSWORD = 'Windows10'
REQ_ID = '659'
REQ_TITLE = '法律数据库'
BASE_URL = 'http://520myfuture.com/db/goEntrance?'
CONN = RedisClient('account', 'pkulaw')
CONN1 = RedisClient('url_list', 'myfuture')

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


class account_req( ):

    def dict_format(self, filepath, dict_1):
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f1:
                for key, value in dict_1.items( ):
                    f1.write(key + "=" + string(value) + "; ")
            f1.close( )
        except FileNotFoundError:
            print('file not exist')
            os.mkdir(filepath)
            self.dict_format(filepath, dict_1)
            # with open(filepath, 'w', encoding = 'utf-8') as f1:
            #     for key, value in dict_1.items( ):
            #         f1.write(key + "=" + string(value) + "; ")
            # f1.close( )
        pass

    def txt_reformat(self, filepath):
        try:
            with open(filepath, 'rb+') as f2:
                f2.seek(-2, os.SEEK_END)
                f2.truncate( )
            f2.close( )
        except FileNotFoundError:
            print('file not exist')
            os.mkdir(filepath)
            self.txt_reformat(filepath)
            # with open(filepath, 'rb+') as f2:
            #     f2.seek(-2, os.SEEK_END)
            #     f2.truncate( )
            # f2.close( )
        pass

    def read_txt_header_update(self, filepath, headers):
        try:
            with open(filepath, 'r', encoding = 'utf-8') as f3:
                cookies = f3.readline( )
                print(cookies)
                headers.update(Cookie = cookies)
            f3.close( )
            return headers
        except FileNotFoundError:
            print('file not exist')
            os.mkdir(filepath)
            self.read_txt_header_update(filepath, headers)
            # with open(filepath, 'r', encoding = 'utf-8') as f3:
            #     cookies = f3.readline( )
            #     print(cookies)
            #     headers.update(Cookie = cookies)
            # f3.close( )
            return None
        pass

    def headers_json(self, filepath, headers):
        try:
            with open(filepath, 'w', encoding = 'utf-8') as f4:
                js = json.dumps(headers)
                f4.write(js)
            f4.close( )
            return None
        except FileNotFoundError:
            print('file not exist')
            os.mkdir(filepath)
            self.headers_json(filepath, headers)
            # with open(filepath, 'w', encoding = 'utf-8') as f4:
            #     js = json.dumps(headers)
            #     f4.write(js)
            # f4.close( )
            return None
        pass

    def test_req(self, url):
        try:
            # url = req_random_url( )
            res = requests.get(url)
            if res.status_code == 200:
                content = self.decode_content(res.content)
                self.parse_content(content)
            elif res.status_code == 404:
                print(404)
                # test_req(url)
                return None
        except Exception as e:
            print(e)
            pass

    def decode_content(self, html):
        encoding = chardet.detect(html)
        content = html.decode(encoding['encoding'], 'ignore')
        return content

    def parse_index(self, content):
        doc = pq(content)
        url = doc('frame').attr('src')
        print(url)
        return url

    def parse_content(self, content):
        global context
        # dom_tree = etree.HTML(content)
        # num2 = dom_tree.xpath('//div/p[3]/strong')
        # for i in num2:
        #     context = i.text
        # print(context)
        # num = re.findall('\d+.?\d', context, re.S)
        # print(num)
        doc = pq(content)
        info = doc('strong').text( )
        num = re.findall('\d+.?\d', info, re.S)
        CONN.set(num[0], num[1])
        print(info)
        print(num)

    def req_content(self, url):
        try:
            request = requests.Session( )
            response = request.get(url = url, headers = D_HEADERS, timeout = 10)
            if response.status_code == 200:
                content = response.content
                context = self.decode_content(content)
                print('content: ' + context)
                return context
            else:
                print(response.status_code)
                print(response.history)
                print(response.url)
                return None
        except ConnectionError:
            pass

    def parse_js(self, filepath):
        # with open(content,'r', encoding = 'utf-8') as f:
        #     doc = string(f.readlines())
        # print(doc)
        # info = json.loads(doc)
        # print(info)
        # url = info['dogo']['urls']
        doc = pq(filename = filepath, parser = 'html')
        items = doc('body script').text( )
        print(items)
        urls = re.findall('urls.*?=.*?"(.*?)";', items, re.S)
        print(urls)
        for i in range(len(urls)):
            CONN1.set('url[' + str(i) + ']', urls[i])
        url = random.choice(urls)
        print(url)
        return url

    def req_random_url(self):
        global url
        count = CONN1.scan( )
        i = random.randrange(count)
        url = CONN1.get('url[' + str(i) + ']')
        print(url)
        return url
        # try:
        #     request = requests.Session()
        #     response = request.get(url)
        #     if response.status_code == 200:
        #         html = decode_content(response.content)
        #         print(html)
        #         return html
        #     else:

    def job(self):
        start = time.time( )
        u_list = CONN1.get_alval( )
        with ThreadPoolExecutor(max_workers = 30) as executor:
            executor.map(self.test_req, u_list)
        # all_task = [executor.submit(test_req, (url)) for url in u_list]
        # for future in as_completed(all_task):
        #     data = future.result( )
        #     print("in main: get page {}s success".format(data))
        # for i in zip(u_list, executor.map(test_req, u_list)):
        #     print(i)
        # url = CONN1.get(i)
        # t = threading.Thread(target = test_req, args = (url,))
        # t.start()
        # t.join()
        # test_req(url)
        print('cost time: {}'.format(time.time( ) - start))
        # req_random_url()
        # url = 'F:\BDFB-spider_v5\Cookie_pool\\test.html'
        # parse_js(url)
        # # parse_content()
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


ar = account_req( )
ar.job( )

# class MyFutureConnector(object):
#     def __init__(self, username=USERNAME, userpassword=USERPASSWORD, req_id=REQ_ID, req_title=REQ_TITLE):
#         self.username = username
#         self.userpassword = userpassword
#         self.rid = req_id
#         self.title = req_title
#
#     def first_log_cookie(self):
#         login_url = 'http://520myfuture.com/account/login'
#
#         try:
#             request = requests.Session( )
#             response = request.get(url = login_url, headers = HEADERS, timeout = 10)
#             if response.status_code == 200:
#                 acookie = response.cookies.get_dict( )
#                 os.makedirs('./Cookies/', exist_ok = True)
#                 with open('./Cookies/first_log_cookie.txt', 'w', encoding = 'utf-8') as f1:
#                     for key, value in acookie.items( ):
#                         f1.write(key + "=" + string(value))
#                 f1.close( )
#                 with open('./Cookies/first_log_cookie.txt', 'r', encoding = 'utf-8') as f2:
#                     acookie = f2.readline( )
#                     HEADERS.update(Cookie = acookie, Referer = login_url)
#                     dict_3 = {'X-Requested-With': 'XMLHttpRequest'}
#                     HEADERS.update(dict_3)
#                 f2.close( )
#                 print(HEADERS)
#                 print(acookie)
#                 return HEADERS
#             else:
#                 print(response.history)
#         except ConnectionError:
#             pass
#
#     def req_account(self, headers):
#         rid = self.rid
#         title = self.title
#
#         DATA.update(id = rid, title = title)
#
#         url = BASE_URL + urlencode(DATA)
#
#         try:
#             request = requests.Session( )
#             response = request.get(url = url, data = DATA, headers = headers, timeout = 10)
#             if response.url == url:
#                 print('return html')
#                 html = response.content
#                 content = decode_content(html)
#                 d_url = parse_index(content)
#                 context = req_content(d_url)
#                 filepath = './Cookies/req.html'
#                 with open(filepath, 'w', encoding = 'utf-8') as f:
#                     f.write(context)
#                 f.close( )
#                 parse_js(filepath)
#                 return context
#             else:
#                 headers = self.login( )
#                 print(headers)
#                 self.req_account(headers)
#                 return None
#         except ConnectionError:
#             pass
#
#     def getcaptcha(self):
#         username = self.username
#         getb_url = 'http://520myfuture.com/ACCOUNT/GetCaptcha?'
#
#         GETB_DATA.update(userName = username)
#         getb_url = getb_url + urlencode(GETB_DATA)
#
#         headers = self.first_log_cookie( )
#
#         try:
#             request = requests.Session( )
#             response = request.get(url = getb_url, data = GETB_DATA, headers = headers, timeout = 10)
#             if response.status_code == 200:
#                 print(response.url)
#                 print(response.history)
#                 headers.update(Origin = 'http://520myfuture.com')
#                 print(headers)
#                 return headers
#             else:
#                 print(response.status_code)
#                 print(response.history)
#                 print(response.url)
#                 return None
#         except ConnectionError:
#             pass
#
#     def login(self):
#         username = self.username
#         password = self.userpassword
#
#         logindata = {
#             'UsernameOrEmailAddress': username,
#             'Password': password
#         }
#
#         headers = self.getcaptcha( )
#
#         lurl = headers.get('Referer')
#         print(lurl)
#
#         try:
#             request = requests.Session( )
#             response = request.post(url = lurl, data = logindata, headers = headers, timeout = 10)
#             if response.status_code == 200:
#                 cookies = response.cookies.get_dict( )
#                 print(cookies)
#                 dict_format('./Cookies/login_cookies.txt', cookies)
#                 txt_reformat('./Cookies/login_cookies.txt')
#                 headers = read_txt_header_update('./Cookies/login_cookies.txt', headers)
#                 headers_json('./Cookies/headers.txt', headers)
#                 return headers
#             else:
#                 print(response.status_code)
#                 print(response.history)
#                 print(response.url)
#                 return None
#         except ConnectionError:
#             pass
