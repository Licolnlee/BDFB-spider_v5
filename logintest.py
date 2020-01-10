# coding = utf-8
import re
import ssl
import urllib
from urllib import request
from urllib.request import urlopen
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

from soupsieve.util import string

ua=UserAgent()

url = 'https://login.pkulaw.com/login?menu=&isAutoLogin=false&returnUrl=http://www.pkulaw.com/case/'
url1 = "https://www.pkulaw.com/case/"
data={
    'LoginName': '16564614616',
    'LoginPwd': '16564614616'
}

headers = {
    'Host': 'login.pkulaw.com',
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '42',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://login.pkulaw.com/?ReturnUrl=http%3a%2f%2fwww.pkulaw.com%2fcase%2f',
    'X-Requested-With': 'XMLHttpRequest',
}


def login_spider(url,data,headers):
    try:
        print("Requesting Pages...")
        ses=requests.Session()
        res = ses.post(url = url, data = data, headers = headers, timeout = 10)
        encoding = chardet.detect(res.content)
        cookies = res.cookies.get_dict()
        print(cookies)
        html = res.content.decode(encoding['encoding'],'ignore')
        print("return html....")
        print(res.status_code)
        return cookies
    except Exception as e:
        print(e)
        pass

def post_spider(url):
    headers1 = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/79.0.3945.88 Safari/537.36',
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '526',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.pkulaw.com',
        # 'Sec-Fetch-Dest':'empty',
        'X-Requested-With': 'XMLHttpRequest',
        # 'DNT': '1',
        'Origin': 'https://www.pkulaw.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.pkulaw.com/case/',
        # 'Cookie': string({'AccountMessage': 'LnLr6VXk9jcWHqqoFhvloNEYpbAnK9Xf0Wdoibz2TaSJsNbPi7ljpEqF93S7xxeVgqi3fYydAGWURvIJsWLubg==', 'IP_AUTO_LOGIN_UNABLE': '113.13.46.129', 'loginaccount': '{"SessionId":"gavzyglymbxn1nafh0mpwmii","UserLoginIp":"113.13.46.129","UserAccountId":"c59961a8-2830-ea11-b390-00155d3c0709","UserAccountMenuRight":[{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"journal","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"reference","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"law","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"journal","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"law","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"lawfirm","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"reference","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"case","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"case","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100},{"AccountId":"c59961a8-2830-ea11-b390-00155d3c0709","Menu":"lawfirm","IsTryUse":true,"StartDate":"\\/Date(1578240000000-0000)\\/","ExpireDate":"\\/Date(1578880978000-0000)\\/","OnlineCount":1,"ReadLimitCount":200,"ReadLimitCountToBuy":100}],"UserRole":"Personal","NickName":"885614","LinkManName":"885614","UserLoginName":"phone2020010610025840970","UserLoginPwd":"UQ/iclLQ4+Mq7iHnN3bKBg==","UserLoginPwd2":"16564614616","Email":"885614@qq.com","RegisterTime":"\\/Date(1578276178000-0000)\\/","WeChatUnionId":"","IsBindWeChatState":0,"UserLoginMode":""}', 'pkulaw_v6_sessionid': 'gavzyglymbxn1nafh0mpwmii'})
        'Cookie': 'xClose=7; pkulaw_v6_sessionid=tbzw3vtjm4tyhttgotxl35t0; xCloseNew=7; redSpot=false; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578296317,1578296340,1578296341,1578376289; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578380259'
    }

    data1 = {
        'Menu': 'case',
        'SearchKeywordType': 'DefaultSearch',
        'MatchType': 'Exact',
        'RangeType': 'Piece',
        'Library': 'pfn1',
        'ClassFlag': 'pfn1',
        # 'QueryOnClick': 'False',
        # 'AfterSearch': 'False',
        # 'IsSynonymSearch': 'true',
        # 'IsAdv': 'False',
        # 'ClassCodeKey': ',,,,,,,,',
        # 'GroupByIndex': '3',
        # 'OrderByIndex': '0',
        'ShowType': 'Default',
        'RecordShowType': 'List',
        'Pager.PageSize': '10',
        'isEng': 'chinese',
        'X-Requested-With': 'XMLHttpRequest',
    }

    try:
        print("Requesting Pages...")
        ses=requests.Session()
        res = ses.post(url = url1, data = data1, headers = headers1, timeout = 10)
        encoding = chardet.detect(res.content)
        html = res.content.decode(encoding['encoding'],'ignore')
        print("return html....")
        print(html)
        return html
    except Exception as e:
        print(e)
        pass


#
post_spider(url1)
# login_spider(url,data,headers)