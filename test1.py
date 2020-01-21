# coding = utf-8
# -*- coding:utf-8 -*-
import ast
import os
import re
import time
from urllib.parse import urlencode
from urllib.request import urlretrieve, urlopen
import chardet
import requests
from pyquery import PyQuery as pq
from redis import StrictRedis
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import redis
import json
from soupsieve.util import string


# r = redis.StrictRedis(host = 'localhost', port = 6379, db = 1, password = '')
pool = redis.ConnectionPool(host = 'localhost', port = 6379, db = 1, password = '')
r_pool = redis.StrictRedis(connection_pool = pool, charset = 'UTF-8', errors='strict', decode_responses=True, unix_socket_path=None)
r_pipe = r_pool.pipeline()
# ua = UserAgent( )
# redis = StrictRedis(host = 'localhost', port = 6379, db = 1, password = '')
# url="https://www.baidu.com"

# url = "https://www.pkulaw.com/case/search/RecordSearch"
# # url = "D:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html"
# # content = urlopen(url).read()
# # context = open(url, 'r', encoding = 'utf-8').read( )
# # content = string(BeautifulSoup(context, 'html.parser'))
# # content = urlopen("https://www.baidu.com").read()
# # context = ssl._create_unverified_context()
# # req = request.Request(url = "F:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html",)
# # res = request.urlopen(req,context=context)
# # content = res.read()
# # print(content)
#
# # res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
# # link = re.findall(res_url, content, re.I|re.S|re.M)
# # for url in link:
# #         print(url)
# # req_url = '^a6bdb3332ec0adc4.*bdfb$'<a.*?href="(.*?)">.*?</a>
# # results = re.findall('<input.*?checkbox.*?checkbox.*?value="(a.*?)"/>', content, re.S)
# # print(results)
# # print(len(results))
# # for result in results:
# #     print(result[1])
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/79.0.3945.88 Safari/537.36',
#     # 'User-Agent': ua.random,
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip,deflate,br',
#     'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
#     'Connection': 'keep-alive',
#     'Content-Length': '526',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Host': 'www.pkulaw.com',
#     # 'Sec-Fetch-Dest':'empty',
#     'X-Requested-With':'XMLHttpRequest',
#     # 'DNT': '1',
#     'Origin': 'https://www.pkulaw.com',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Referer': 'https://www.pkulaw.com/case/',
#     'Cookie': 'redSpot=false; pkulaw_v6_sessionid=tbzw3vtjm4tyhttgotxl35t0; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; xCloseNew=11'
#     # 'Cookie': 'xClose=7; pkulaw_v6_sessionid=yfc1vmuj1kpsuo3njyjscjqy; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578296317,1578296340,1578296341,1578376289; xCloseNew=8; redSpot=false; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578383719'
# }
#
# data = {
#     #'Menu': 'case',
#     # 'SearchKeywordType': 'DefaultSearch',
#     # 'MatchType': 'Exact',
#     # 'RangeType': 'Piece',
#     # 'Library': 'pfn1',
#     # 'ClassFlag': 'pfn1',
#     # 'QueryOnClick': 'False',
#     # 'AfterSearch': 'False',
#     # 'IsSynonymSearch': 'true',
#     # 'IsAdv': 'False',
#     # 'ClassCodeKey': ',,,,,,,,',
#     # 'GroupByIndex': '3',
#     # 'OrderByIndex': '0',
#     'ShowType': 'Default',
#     # 'RecordShowType': 'List',
#     'Pager.PageSize': '100',
#     # 'isEng': 'chinese',
#     'X-Requested-With': 'XMLHttpRequest',
# }


# class gid_data:
#
#     def __init__(self, name, gid, issue_type, court_name, issue_num, issue_date):
#         self.name = name
#         self.gid = gid
#         self.issue_type = issue_type
#         self.court_name = court_name
#         self.issue_num = issue_num
#         self.issue_date = issue_date

# def set_attr(self, name, gid, issue_type, court_name, issue_num, issue_date):
#     self.name = name
#     self.gid = gid
#     self.issue_type = issue_type
#     self.court_name = court_name
#     self.issue_num = issue_num
#     self.issue_date = issue_date


proxy_pool_url = 'http://127.0.0.1:5010/get'


def get_proxy():
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


def req_page(page):
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
    }

    data1 = {
        'SearchKeywordType': 'JournalId',
        'ShowType': 'Default',
        'Pager.PageSize': '100',
        'Menu': 'case',
        'Pager.PageIndex': page,
        'ClassCodeKey': ',,,,,001,,,',
    }

    url1 = 'https://www.pkulaw.com/case/search/RecordSearch'

    try:
        print("Requesting Pages...")
        ses = requests.Session( )
        res = ses.post(url = url1, data = data1, headers = headers1, timeout = 10)
        encoding = chardet.detect(res.content)
        html = res.content.decode(encoding['encoding'], 'ignore')
        print("return html....")
        # print(html)
        return html
    except ConnectionError:
        return req_page(page)


def parse_index(html):
    doc = pq(html)
    items = doc('.block').items()
    i = 0
    for item in items:
        gid = item('input').attr('value')
        name = item('h4 a').text().encode('UTF-8')
        related_info = item('.related-info').text()
        issue_type = related_info.split(' / ')[0]
        court_name = related_info.split(' / ')[1]
        issue_num = related_info.split(' / ')[2]
        issue_date = related_info.split(' / ')[-1]
        dg = dict(gid = gid, issue_type = issue_type, court_name = court_name, issue_num = issue_num,
                  issue_date = issue_date)
        en_json_dg = json.dumps(dg, ensure_ascii = False, indent = 4).encode('UTF-8')
        r_pipe.hset('crawldata', name, en_json_dg)
        r_pipe.hset('downloadreqdata', name, gid)
        r_pipe.execute()
        # print(name)
        # print(gid)
        # print(related_info)
        # print(issue_type)
        # print(court_name)
        # print(issue_num)
        # print(issue_date)
        # gids = gid_data(name = name, gid = gid, issue_type = issue_type, court_name = court_name, issue_num = issue_num, issue_date = issue_date)
        # r_pool.
        # gid_data.set_attr(name = name, gid = gid, issue_type = issue_type, court_name = court_name, issue_num = issue_num, issue_date = issue_date)
        i += 1
    print(i)

    # items = doc('.block .list-title h4 a').items()
    # for item in items:
    #     name = item.text()
    #     print(name)
    # doc = string(BeautifulSoup(html, 'html.parser'))
    # results = re.findall('<li.*?block.*?list-title,*?sortNum.*?flink.*?/pfnl/.*?_blank.*?>"(.*?)".*?', doc, re.S)
    # print(results)
    # print(len(results))
    # with open('./download/reqpage.html', 'w', encoding = 'utf-8') as f:
    #     f.write(doc)
    # f.close()
    # # print(doc)
    # # items = doc('.block .list-title h4 a')
    # # context = string(items)
    # with open('./download/reqpage.html', 'r', encoding = 'utf-8') as f1:
    #     content = string(f1.readline())
    #     names = re.findall('<li.*?block.*?sortNum.*?a.*?_blank.*?flink.*?/pfnl/.*?>"(.*?)"</a>', content, re.S)
    #     print(names)
    # f1.close()
    # print(len(names))
    # print(items)
    # print(type(items))
    # print(items)
    # lis = items.find('input')
    # values = yield items.attr('value')
    # for item in items:
    #     value = item.attr('value')
    #     print(value)
    # for item in items:
    #     value = item.attr('value')
    #     print(value)
    # with open('./download/gidreq.txt', 'w', encoding = 'utf-8') as f:
    #     f.write(value)
    # f.close()
    # print(items)
    # print(values)
    # print(type(lis))
    # print(lis)
    # print(doc('li .block input .recordList value'))
    # items = doc('.container .rightContent ul li .block input').items()
    # for item in items:
    #     yield item.attr('value')
# def req_index(page):
#     data = data1
#     req_pageindex = int(page)
#     data.update(Pager.PageIndex = req_pageindex)

# def getgid(url,data,headers):
#     # html = post_spider(url,data,headers)
#     content = string(BeautifulSoup(html,'html.parser'))
#     results = re.findall('<li.*?block.*?recordList.*?value="(a.*?)".*?>.*?</li>',content,re.S)
#     print(results)
#     print(len(results))
# getgid(url,data,headers)
# # post_spider(url,data,headers)
# # r = requests.post(url,data = data, headers = headers, timeout = 10)
# # print(r.status_code)
# # r= requests.post(url,headers,timeout=10)
# # print(r.status_code)
# # singeldownload()
#
# # def reqcookie():
# #     url3 = "https://www.pkulaw.cn/Case/"
# #     url2 = "https://www.pkulaw.cn/case/CheckLogin/Login"
# #     data2 = {
# #         'Usrlogtype': '1',
# #         'ExitLogin': '',
# #         'menu': 'case',
# #         'CookieId': '' ,
# #         'UserName': '16530569067',
# #         'PassWord': '16530569067',
# #         'jz_id': '0',
# #         'jz_pwd': '0',
# #         'auto_log': '0',
# #     }
# #     headers2 = {
# #         'Host': 'www.pkulaw.cn',
# #         'Connection': 'keep-alive',
# #         'Content-Length': '113',
# #         'Origin': 'https: // www.pkulaw.cn',
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
# #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# #         'Accept': '*/*',
# #         'X-Requested-With': 'XMLHttpRequest',
# #         'Referer': 'https://www.pkulaw.cn/Case/',
# #         'Accept-Encoding': 'gzip, deflate, br',
# #         'CheckIPDate': time.strftime('%y%y-%m-%d %H:%M:%S',time.localtime()),
# #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
# #     }
# #
# #     headers3 = {
# #         'Accept': '*/*',
# #         'Accept-Encoding': 'gzip, deflate, br',
# #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
# #         'Connection': 'keep-alive',
# #         'Content-Length': '113',
# #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# #         'Cookie': 'ASP.NET_SessionId=0psusmtincxmotx0qa5bfjj4; QINGCLOUDELB=59f1d6de987b0d2fd4ddf2274d09ac70921c45dcd3b30550838de7d33d1e4651; CookieId=0psusmtincxmotx0qa5bfjj4; CheckIPAuto=; CheckIPDate=2020-01-15 14:29:59',
# #         'DNT': '1',
# #         'Host': 'www.pkulaw.cn',
# #         'Origin': 'https://www.pkulaw.cn',
# #         'Referer': 'https://www.pkulaw.cn/Case/',
# #         'sec-ch-ua': '"Google Chrome 79"',
# #         'Sec-Fetch-Dest': 'empty',
# #         'Sec-Fetch-Mode': 'cors',
# #         'Sec-Fetch-Site': 'same-origin',
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
# #         'X-Requested-With': 'XMLHttpRequest',
# #     }
# #
# #     # response = requests.Session()
# #     # res = response.post(url = url2, headers = headers2, data = data2, timeout = 10,stream = True)
# #     # print(res.status_code)
# #     # cookie = res.cookies.get_dict()
# #     # t = res.request.headers.get('CheckIPDate')
# #     # # print(t)
# #     # # print(cookie)
# #     # # print(cookie.get('CookieId'))
# #     # os.makedirs('./Cookies/',exist_ok = True)
# #     # with open('./Cookies/req_Cookies.txt','w',encoding = 'utf-8') as f:
# #     #     for key,value in cookie.items():
# #     #         f.write(key+'='+string(value)+'; ')
# #     #     f.write('CheckIPAuto=; ')
# #     #     f.write('CheckIPDate='+t)
# #         # f.write('User_User=phone2020011214400673851')
# #         # 'Cookie': 'ASP.NET_SessionId=tigxfhukj3h1p5empnlhbvyb; QINGCLOUDELB=b1262d52db822794d00c3069ee5bd621ec61ed2f1b6f7d61f04556fafeaf0c45; CookieId=tigxfhukj3h1p5empnlhbvyb; CheckIPAuto=; CheckIPDate=2020-01-10 20:38:30; User_User=phone2020010610184515819; FWinCookie=1'
# #         # # 'Cookie': 'pkulaw_v6_sess
# #     # f.close()
# #
# #     time.sleep(5)
# #     with open('./Cookies/req_Cookies.txt', 'r', encoding = 'utf-8') as f1:
# #         cookie6 = f1.readline()
# #         print('he'headers3)
# #         print(cookie1)
# #         headers3.update(Cookie = string(cookie1))
# #         print(headers3)
# #         req = requests.Session()
# #         requ = req.post(url = url2, headers = headers3, data = data2, timeout = 10, stream = True)
# #         cookie2 = requ.cookies.get_dict()
# #         print(cookie2)
# #         os.makedirs('./Cookies/', exist_ok = True)
# #         with open('./Cookies/Check_expire_date.txt', 'w', encoding = 'utf-8') as f:
# #             for key, value in cookie2.items( ):
# #                 f.write(key + '=' + string(value) + '; ')
# #         f.close()
# #         print(requ.status_code)
#
#
# # def test_time():
# #     local_t = time.strftime('%y%y-%m-%d %H:%M:%S',time.localtime())
# #     print(local_t)
# def req_cookies():
#     headers1 = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'DNT': '1',
#         'Host': 'www.pkulaw.cn',
#         'If-Modified-Since': 'Wed, 15 Jan 2020 07:26:56 GMT',
#         'Referer': 'https://www.pkulaw.cn/',
#         'sec-ch-ua': 'Google Chrome 79',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Sec-Origin-Policy': '0',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
#     }
#
#     headers2 = {
#         'Accept': '*/*',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
#         'Connection': 'keep-alive',
#         'Cookie': 'QINGCLOUDELB=59f1d6de987b0d2fd4ddf2274d09ac70921c45dcd3b30550838de7d33d1e4651',
#         'DNT': '1',
#         'Host': 'www.pkulaw.cn',
#         'Referer': 'https://www.pkulaw.cn/Case/',
#         'sec-ch-ua': '"Google Chrome 79"',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
#         'X-Requested-With': 'XMLHttpRequest'
#     }
#
#     headers3 = {
#         'Accept': '*/*',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
#         'Connection': 'keep-alive',
#         'Content-Length': '113',
#         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'Cookie': 'ASP.NET_SessionId=0psusmtincxmotx0qa5bfjj4; QINGCLOUDELB=59f1d6de987b0d2fd4ddf2274d09ac70921c45dcd3b30550838de7d33d1e4651; CookieId=0psusmtincxmotx0qa5bfjj4; CheckIPAuto=; CheckIPDate=2020-01-15 14:29:59',
#         'DNT': '1',
#         'Host': 'www.pkulaw.cn',
#         'Origin': 'https://www.pkulaw.cn',
#         'Referer': 'https://www.pkulaw.cn/Case/',
#         'sec-ch-ua': '"Google Chrome 79"',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
#         'X-Requested-With': 'XMLHttpRequest',
#     }
#
#     data1 = {
#         'Usrlogtype': '3',
#         'ExitLogin': '',
#         'menu': 'case',
#         'UserName': '',
#         'PassWord': '',
#         'jz_id': '',
#         'jz_pwd': '',
#         'auto_log': ''
#     }
#
#     data2 = {
#         'Usrlogtype': '1',
#         'ExitLogin': '',
#         'menu': 'case',
#         'CookieId': '',
#         'UserName': '16566408577',
#         'PassWord': '16566408577',
#         'jz_id': '0',
#         'jz_pwd': '0',
#         'auto_log': '0',
#     }
#
#     url1 = 'https://www.pkulaw.cn/Case'
#     try:
#         req = requests.Session( )
#         response = req.get(url = url1, headers = headers1, timeout = 10)
#         cookie1 = response.cookies.get_dict( )
#         print('cookie1 = ' + string(cookie1))
#         os.makedirs('./Cookies/', exist_ok = True)
#         with open('./Cookies/get_QINGCLOUDLB.txt', 'w', encoding = 'utf-8') as f:
#             for key, value in cookie1.items( ):
#                 f.write(key + '=' + string(value))
#         f.close( )
#     except Exception as e:
#         print('error1: ' + string(e))
#         pass
#
#     url2 = 'https://www.pkulaw.cn/case/CheckLogin/Login?' + urlencode(data1)
#     with open('./Cookies/get_QINGCLOUDLB.txt', 'r', encoding = 'utf-8') as f1:
#         cookie2 = f1.readline( )
#         print('headers2 = ' + string(headers2))
#         print('cookie2 = ' + string(cookie2))
#         headers2.update(Cookie = string(cookie2))
#         print('headers2 = ' + string(headers2))
#     f1.close( )
#     try:
#         req = requests.Session( )
#         response = req.get(url = url2, headers = headers2, timeout = 10)
#         cookie3 = response.cookies.get_dict( )
#         cookie4 = {}
#         cookie5 = cookie1
#         cookie4.update(cookie3)
#         cookie4.update(cookie5)
#         print('cookie3 = ' + string(cookie3))
#         print('cookie4 = ' + string(cookie4))
#         os.makedirs('./Cookies/', exist_ok = True)
#         with open('./Cookies/req_Cookies.txt', 'w', encoding = 'utf-8') as f2:
#             for key, value in cookie4.items( ):
#                 f2.write(key + '=' + string(value) + '; ')
#             f2.write('FWinCookie=1; User_User=phone2020011214400673851')
#         f2.close( )
#     except Exception as e1:
#         print('error2: ' + string(e1))
#         pass
#
#         url3 = "https://www.pkulaw.cn/case/CheckLogin/Login"
#         with open('./Cookies/req_Cookies.txt', 'r', encoding = 'utf-8') as f4:
#             cookie4 = f2.readline( )
#             print('headers3 = ' + string(headers3))
#             print('cookie4 = ' + string(cookie4))
#             headers1.update(Cookie = string(cookie4))
#             print('headers3 = ' + string(headers3))
#         f4.close( )
#         try:
#             req = requests.Session( )
#             requ = req.post(url = url3, headers = headers3, data = data2, timeout = 10, stream = True)
#             cookie5 = requ.cookies.get_dict( )
#             print('requ.status_code: ' + requ.status_code)
#             print('cookie5 = ' + string(cookie5))
#         except Exception as e2:
#             print('error3: ' + string(e2))
#             pass


def singeldownload(cookie, name, gid):
    headers4 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': cookie,
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
    data1 = {
        'library': 'pfnl',
        'gid': gid,
        'type': 'txt',
        'jiamizi': ''
    }

    url1 = 'https://www.pkulaw.cn/case/FullText/DownloadFile?' + urlencode(data1)
    try:
        print("Requesting Pages...")
        print('headers4.getcookie: ' + string(headers4.get('Cookie')))
        ses = requests.Session()
        res = ses.get(url = url1, headers = headers4, data = data1, stream = True)
        print(res.status_code)
        if res.status_code == 200:
            with open('./download/'+name+'.txt', 'wb') as f4:
                for chunk in res.iter_content(chunk_size = 32):  # chunk_size #设置每次下载文件的大小
                    f4.write(chunk)  # 每一次循环存储一次下载下来的内容
            with open('./download/'+name+'.txt', 'r', encoding = 'GBK') as f5:
                lines = f5.readlines()
                first_line = lines[0]
                key = "尚未登录"
                if key in first_line:
                    print(first_line + "请先登录获取cookie")
                else:
                    print('您的账号已经登陆')
            f5.close()
            print("return html....")
        else:
            print("unable to download...")
    except Exception as e:
        print(e)
        pass
    # ses = requests.Session()
    # res = ses.get(url = url1, data = data1, headers = headers1, timeout = 10)
    # print(res.content)
    # if res.history:
    #     print("Request redirected")
    #     for ress in res.history:
    #         print(ress.status_code, ress.url)
    #         print("Final destination:")
    #         print(res.status_code, res.url)
    # else:
    #     print("Request was not redirected")
    # urlretrieve(,)
    # encoding = chardet.detect(res.content)
    # html = res.content.decode(encoding['encoding'], 'ignore')
    # print("return html....")
    # print(html)
    # return
    # response = requests.post(url =url1,data = data1, headers = headers1)

    # url1 = 'https://v6downloadservice.pkulaw.com/full/downloadfile?' + urlencode(data1)
    # print(url1)
    # os.makedirs('./download/', exist_ok = True)
    # try:
    #     urlretrieve(res.url, './download/test.txt')
    # except Exception as e:
    #     print(e)
    #     pass
    # response = requests.post(url1,headers1)


def first_login_reqck():
    global cookieID
    url1 = 'https://www.pkulaw.cn/case/CheckLogin/Login'

    data1 = {
        'Usrlogtype': '1',
        'ExitLogin': '',
        'menu': 'case',
        'CookieId': '',
        'UserName': '15045729324',
        'PassWord': '15045729324',
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


def crawl_data():
    for page in range(0, 2):
        html = req_page(page)
        if html:
            parse_index(html = html)


def download_data():
    cookie = first_login_reqck()
    names = r_pool.hkeys('downloadreqdata')
    for i in range(len(names)):
        names_list = {i: names[i].decode()}
        gid = r_pool.hget('downloadreqdata', names_list[i]).decode()
        singeldownload(cookie = cookie, name = names_list[i], gid = gid)
        print(names_list[i])
        print(gid)
        i += 1
        time.sleep(5)


if __name__ == '__main__':
    download_data()
    # crawl_data()