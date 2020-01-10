# coding = utf-8
import re
import ssl
import urllib
from urllib import request
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import requests
import psycopg2
import datetime
import time
from fake_useragent import UserAgent
import chardet
from lxml import etree
import hashlib
import csv
import os

ua = UserAgent( )

# url="https://www.baidu.com"
from soupsieve.util import string

url = "https://www.pkulaw.com/case/search/RecordSearch"

#
# def readgid:
#     content = post_spider(url,data,headers)
# url = "D:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html"
# content = urlopen(url).read()
# context = open(url, 'r', encoding = 'utf-8').read( )
# content = string(BeautifulSoup(context, 'html.parser'))
# content = urlopen("https://www.baidu.com").read()
# context = ssl._create_unverified_context()
# req = request.Request(url = "F:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html",)
# res = request.urlopen(req,context=context)
# content = res.read()
# print(content)

# res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
# link = re.findall(res_url, content, re.I|re.S|re.M)
# for url in link:
#         print(url)
# req_url = '^a6bdb3332ec0adc4.*bdfb$'<a.*?href="(.*?)">.*?</a>
# results = re.findall('<input.*?checkbox.*?checkbox.*?value="(a.*?)"/>', content, re.S)
# print(results)
# print(len(results))
# for result in results:
#     print(result[1])

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    # 'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '526',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.pkulaw.com',
    'Sec-Fetch-Dest': 'empty',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Origin': 'https://www.pkulaw.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'sec-ch-ua': '"Google Chrome 79"',
    'Referer': 'https://www.pkulaw.com/case/',
    # 'Cookie': 'pkulaw_v6_sessionid=cz3d5tysubxaduz4g04scgdw; redSpot=false; xCloseNew=8',
    # 'Cookie': 'xClose=7; pkulaw_v6_sessionid=yfc1vmuj1kpsuo3njyjscjqy; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578296317,1578296340,1578296341,1578376289; xCloseNew=8; redSpot=false; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578383719'
}

data = {
    # 'Menu': 'case',
    # 'SearchKeywordType': 'DefaultSearch',
    # 'MatchType': 'Exact',
    # 'RangeType': 'Piece',
    # 'Library': 'pfn1',
    # 'ClassFlag': 'pfn1',
    # 'QueryOnClick': 'False',
    # 'AfterSearch': 'False',
    # 'IsSynonymSearch': 'true',
    # 'IsAdv': 'False',
    # 'ClassCodeKey': ',,,,,,,,',
    # 'GroupByIndex': '3',
    # 'OrderByIndex': '0',
    'ShowType': 'Default',
    # 'Pager.PageIndex': '0',
    # 'RecordShowType': 'List',
    'Pager.PageSize': '100',
    # 'isEng': 'chinese',
    # 'X-Requested-With': 'XMLHttpRequest',
}


def post_spider(url, data, headers):
    try:
        print("Requesting Pages...")
        # ses=requests.Session()
        res = requests.post(url = url, data = data, headers = headers, timeout = 10)
        encoding = chardet.detect(res.content)
        html = res.content.decode(encoding['encoding'], 'ignore')
        print("return html....")
        # print(html)
        return html
    except Exception as e:
        print(e)
        pass


# post_spider(url,data,headers)
# r = requests.post(url,data = data, headers = headers, timeout = 10)
# print(r.status_code)
# r= requests.post(url,headers,timeout=10)
# print(r.status_code)
def readgid(url, data, headers):
    content = post_spider(url, data, headers)
    # contenta = open(content, 'r', encoding = 'utf-8').read()
    contenta = string(content.encode('utf-8'))
    print(type(contenta))
    context = string(BeautifulSoup(contenta, 'html.parser'))
    # print(context)
    # results = re.findall('<input.*?name.*?recordList.*?value="(a.*?b)"/>', context, re.S)
    results = re.findall('<li.*?block.*?recordList.*?value=.*?"(a.*?)".*?>.*?</li>', context, re.S)
    print(results)
    print(len(results))
    return results
    # for result in results:
    #     print(result.strip())


# url = "D:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html"
# content = urlopen(url).read()
# context = open(url, 'r', encoding = 'utf-8').read( )
# content = string(BeautifulSoup(context, 'html.parser'))
# content = urlopen("https://www.baidu.com").read()
# context = ssl._create_unverified_context()
# req = request.Request(url = "F:\BDFB-spider\Sample\案例与裁判文书_裁判文书_裁判文书公开_法院判决书_法院裁定书_司法审判书-北大法宝V6官网.html",)
# res = request.urlopen(req,context=context)
# content = res.read()
# print(content)
#
# readgid(url,data,headers)

def multidownload(url, data, headers):
    # gidlist=readgid(url,data,headers)
    headers1 = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '632',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'pkulaw_v6_sessionid=cz3d5tysubxaduz4g04scgdw; redSpot=false; xCloseNew=8',
        'DNT': '1',
        'Host': 'www.pkulaw.com',
        'Origin': 'https://www.pkulaw.com',
        'Referer': 'https://www.pkulaw.com/case/',
        'sec-ch-ua': '"Google Chrome 79"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data1 = {
        'downloadType': 'BatchDownloadFullText',
        'library': 'pfnl',
        'gids': string(readgid(url, data, headers)),
        'curLib[]': 'pfnl',
        'isDetect': 'true',
    }

    url1 = 'https://www.pkulaw.com/Tool/CheckDownloadLimit'

    try:
        os.makedirs('./download/', exist_ok = True)
        print("Requesting Pages...")
        # ses=requests.Session()
        res = requests.post(url = url1, data = data1, headers = headers1, timeout = 10)

        print("downloading with urllib")
        urlretrieve(rurl, "./download/download.zip")
        # r = requests.get(res.url,stream=True)
        # with open('./download/download.zip', 'wb') as f:
        #     for chunk in r.iter_content(chunk_size=32):
        #         f.write(chunk)
        # encoding = chardet.detect(res.content)
        # html = res.content.decode(encoding['encoding'],'ignore')
        print("download complete....")
        # # print(html)
        # return html
    except Exception as e:
        print(e)
        pass



multidownload(url,data,headers)