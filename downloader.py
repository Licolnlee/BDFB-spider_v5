import os
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import urlencode

import chardet
import redis
import requests
from soupsieve.util import string

from Cookie_pool.account_saver import RedisClient

CONN = RedisClient('account', 'pkulaw_v5')
NUM = 16

pool = redis.ConnectionPool(host = 'localhost', port = 6379, db = 1, password = '')
r_pool = redis.StrictRedis(connection_pool = pool, charset = 'UTF-8', errors = 'strict', decode_responses = True,
                           unix_socket_path = None)
r_pipe = r_pool.pipeline( )

proxy_pool_url = 'http://127.0.0.1:5010/get'


class downloader( ):
    def __init__(self):
        self.names = r_pool.hkeys('downloadreqdata')
        self.names_list = None
        self.username = None
        self.userpassword = None
        self.gid = None
        self.cookieId = None
        self.cookie = None

        self.data1 = {
            'Usrlogtype': '1',
            'ExitLogin': '',
            'menu': 'case',
            'CookieId': '',
            'UserName': self.username,
            'PassWord': self.userpassword,
            'jz_id': '0',
            'jz_pwd': '0',
            'auto_log': '0'
        }

        self.data2 = {
            'Usrlogtype': '1',
            'ExitLogin': '',
            'menu': 'case',
            'CookieId': self.cookieId,
            'UserName': '',
            'PassWord': '',
            'jz_id': '',
            'jz_pwd': '',
            'auto_log': ''
        }

        self.headers1 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '113',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'DNT': '1',
            'Host': 'www.pkulaw.cn',
            'Origin': 'https://www.pkulaw.cn',
            'Referer': 'https://www.pkulaw.cn/Case/',
            # 'sec-ch-ua': '"Google Chrome 79"',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.headers2 = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '112',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            # 'DNT': '1',
            'Host': 'www.pkulaw.cn',
            'Origin': 'https://www.pkulaw.cn',
            'Referer': 'https://www.pkulaw.cn/Case/',
            # 'sec-ch-ua': '"Google Chrome 79"',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.headers3 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Host': 'www.pkulaw.cn',
            'Referer': 'https://www.pkulaw.cn/case/pfnl_a6bdb3332ec0adc4bf6da0b52d04589a8445f45b7079568dbdfb.html?match=Exact',
            # 'sec-ch-ua': 'Google Chrome 79',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-User': '?1',
            # 'Sec-Origin-Policy': '0',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }

        self.data3 = {
            'library': 'pfnl',
            'gid': self.gid,
            'type': 'txt',
            'jiamizi': ''
        }

        self.url1 = 'https://www.pkulaw.cn/case/CheckLogin/Login'
        self.url2 = 'https://www.pkulaw.cn/case/FullText/DownloadFile?' + urlencode(self.data3)

    def get_proxy(self):
        try:
            response = requests.get(proxy_pool_url)
            if response.status_code == 200:
                proxy_url_content = response.content
                encoding = chardet.detect(proxy_url_content)
                proxy_url_context = proxy_url_content.decode(encoding['encoding'], 'ignore')
                proxy_url_context1 = eval(proxy_url_context)
                proxy_url = proxy_url_context1.get('proxy')
                print(proxy_url)
                return proxy_url
        except ConnectionError:
            return None

    def singeldownload(self, name):
        global proxy

        try:
            print("Requesting Pages...")
            self.headers3.update(Cookie = self.cookie)
            print('headers3.getcookie: ' + string(self.headers3.get('Cookie')))
            self.data3.update(gid = self.gid)
            proxy = self.get_proxy( )
            proxies = {
                'http': 'http://' + proxy
            }
            ses = requests.Session( )
            r = ses.head(self.url2)
            total = int(r.headers['Content-Length'])
            print(total)
            # print(r.status_code)
            while r.status_code != 500:
                # with ThreadPoolExecutor(max_workers = 30) as executor:
                #     executor.map(self.download, )
                thread_list = []
                # 一个数字,用来标记打印每个线程
                n = 0
                for ran in self.get_range(total):
                    start, end = ran
                    # 打印信息
                    print('thread %d start:%s,end:%s' % (n, start, end))
                    n += 1
                    # 创建线程 传参,处理函数为download
                    thread = threading.Thread(
                        target = self.download(name, start, end, self.headers3, ses, self.url2, self.data3, proxies),
                        args = (start, end))
                    # 启动
                    thread.start( )
                    thread_list.append(thread)
                for i in thread_list:
                    # 设置等待
                    i.join( )
                print('download %s load success' % name)
                # with open('./download/' + name + '.txt', 'wb') as f4:
                #     for ran in get_range(total):
                #         headers4['Range'] = 'Bytes=%s-%s' % ran
                #         r = ses.get(url = url1, headers = headers4, data = data1, stream = True, proxies = proxies)
                #         f4.seek(ran[0])
                #         f4.write(r.content)
                #     f4.close( )
                # res = ses.get(url = url1, headers = headers4, data = data1, stream = True, proxies = proxies)
                #
                # print('Using proxy : ' + proxy)
                # print(res.status_code)
                # while res.status_code == 200:
                #     with open('./download/'+name+'.txt', 'wb') as f4:
                #         for chunk in res.iter_content(chunk_size = 32):  # chunk_size #设置每次下载文件的大小
                #             f4.write(chunk)  # 每一次循环存储一次下载下来的内容
                with open('./download/' + name + '.txt', 'r', encoding = 'GBK') as f5:
                    lines = f5.readlines( )
                    first_line = lines[0]
                    key = "尚未登录"
                    if key in first_line:
                        print(first_line + "请先登录获取cookie")
                        return False
                    else:
                        print('您的账号已经登陆')
                        return True
            else:
                print("unable to download...")
                return False
        except Exception as e:
            print(e)
            return False

    def download(self, name, start, end, headers, ses, url, data, proxies):
        with open('./download/' + name + '.txt', 'wb') as f4:
            headers['Range'] = 'Bytes=%s-%s' % (start, end)
            r = ses.get(url = url, headers = headers, data = data, stream = True, proxies = proxies)
            f4.seek(start)
            f4.write(r.content)
        f4.close( )

    def get_range(self, total):
        ranges = []
        offset = int(total / NUM)
        for i in range(NUM):
            if i == NUM - 1:
                ranges.append((i * offset, ''))
            else:
                ranges.append((i * offset, (i + 1) * offset))
        return ranges

    def first_login_reqck(self):
        try:
            response = requests.Session( )
            self.data1.update(UserName = self.username, PassWord = self.userpassword)
            res = response.post(url = self.url1, data = self.data1, headers = self.headers1, timeout = 10)
            cookies1 = res.cookies.get_dict( )
            self.cookieId = cookies1.get('CookieId')
            print('CookieId: ' + string(self.cookieId))
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
            self.cookieupdate( )
            self.headers2.update(Cookie = self.cookie)
            self.data2.update(CookieId = self.cookieId)
            response1 = requests.Session( )
            res1 = response1.post(url = self.url1, data = self.data2, headers = self.headers2, timeout = 10)
        except Exception as e2:
            print("error2: " + string(e2))
            pass

    def account_update(self):
        self.username = CONN.random_key( )
        self.userpassword = self.username

    def autocookiecheck(self):
        try:
            print(self.cookie)
            if self.cookie is None or self.cookie is '':
                print('cookie is None')
                return False
            else:
                print('cookie exists')
                return True
        except Exception as e:
            print(e)
            pass
        return False

    def cookieupdate(self):
        try:
            with open('./Cookies/firstlogCookie.txt', 'r', encoding = 'utf-8') as f2:
                self.cookie = f2.readline( )
                print("cookie: " + string(self.cookie))
            f2.close( )
        except Exception as e:
            print(e)
            pass

    def download_data(self):
        global FLAG
        self.cookieupdate( )
        FLAG = self.autocookiecheck( )
        print(FLAG)
        try:
            for i in range(len(self.names)):
                while FLAG:
                    self.names_list = {i: self.names[i].decode( )}
                    self.gid = r_pool.hget('downloadreqdata', self.names_list[i]).decode( )
                    print(self.names_list[i])
                    print(self.gid)
                    # self.cookieupdate( )
                    FLAG = self.singeldownload(name = self.names_list[i])
                    i += 1
                    time.sleep(5)
                    break
                else:
                    print('cookie expired')
                    self.account_update( )
                    self.first_login_reqck( )
                    self.cookieupdate( )
                    self.names_list = {i: self.names[i].decode( )}
                    self.gid = r_pool.hget('downloadreqdata', self.names_list[i]).decode( )
                    print(self.names_list[i])
                    print(self.gid)
                    FLAG = self.singeldownload(name = self.names_list[i])
                    i += 1
                    time.sleep(5)
                    continue
        except Exception as e:
            print(e)
            pass


dl = downloader( )
dl.download_data( )
