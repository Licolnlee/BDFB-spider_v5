# coding = utf-8
import os
import re
import time
from urllib.parse import urlencode
from urllib.request import urlretrieve
import chardet
import requests
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent

# ua = UserAgent( )

# url="https://www.baidu.com"
from soupsieve.util import string

url = "https://www.pkulaw.com/case/search/RecordSearch"
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36',
    # 'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '526',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.pkulaw.com',
    # 'Sec-Fetch-Dest':'empty',
    'X-Requested-With':'XMLHttpRequest',
    # 'DNT': '1',
    'Origin': 'https://www.pkulaw.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.pkulaw.com/case/',
    'Cookie': 'redSpot=false; pkulaw_v6_sessionid=tbzw3vtjm4tyhttgotxl35t0; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; xCloseNew=11'
    # 'Cookie': 'xClose=7; pkulaw_v6_sessionid=yfc1vmuj1kpsuo3njyjscjqy; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578296317,1578296340,1578296341,1578376289; xCloseNew=8; redSpot=false; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578383719'
}

data = {
    #'Menu': 'case',
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
    # 'RecordShowType': 'List',
    'Pager.PageSize': '100',
    # 'isEng': 'chinese',
    'X-Requested-With': 'XMLHttpRequest',
}


def post_spider(url,data,headers):
    try:
        print("Requesting Pages...")
        ses=requests.Session()
        res = ses.post(url = url, data = data, headers = headers, timeout = 10)
        encoding = chardet.detect(res.content)
        html = res.content.decode(encoding['encoding'],'ignore')
        print("return html....")
        # print(html)
        return html
    except Exception as e:
        print(e)
        pass


def getgid(url,data,headers):
    html = post_spider(url,data,headers)
    content = string(BeautifulSoup(html,'html.parser'))
    results = re.findall('<li.*?block.*?recordList.*?value="(a.*?)".*?>.*?</li>',content,re.S)
    print(results)
    print(len(results))


def singeldownload():
    headers1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId: kdcox0fubhob3r4mwobyajsq; QINGCLOUDELB: 59f1d6de987b0d2fd4ddf2274d09ac70921c45dcd3b30550838de7d33d1e4651; CookieId: kdcox0fubhob3r4mwobyajsq; CheckIPAuto=; CheckIPDate: 2020-01-13 16:58:50; User_User=phone2020010610184515819; FWinCookie=1',
        # 'Cookie': 'ASP.NET_SessionId=xsx3ratnhiqvobn1qxlvgff2; QINGCLOUDELB=59f1d6de987b0d2fd4ddf2274d09ac70921c45dcd3b30550838de7d33d1e4651; CookieId=xsx3ratnhiqvobn1qxlvgff2; CheckIPAuto=; CheckIPDate=2020-01-10 20:38:30; User_User=phone2020010610184515819; FWinCookie=1',
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
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/79.0.3945.88 Safari/537.36',
        # # 'User-Agent': ua.random,
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,
        #         # # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         # 'Host': 'www.pkulaw.com',
        #         # # 'Sec-Fetch-Dest':'empty',
        #         # # 'X-Requested-With': 'XMLHttpRequest',
        #         # 'DNT': '1',
        #         # # 'Origin': 'https://www.pkulaw.com',
        #         # 'Sec-Fetch-Site': 'same-origin',
        #         # 'sec-ch-ua': 'Google Chrome 79',
        #         # 'Sec-Fetch-Dest': 'document',application/signed-exchange;v=b3;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        # 'Connection': 'keep-alive',
        # # 'Content-Length': '526',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-User': '?1',
        # 'Sec-Origin-Policy': '0',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Referer': 'https://www.pkulaw.cn/case/pfnl_a6bdb3332ec0adc4bf6da0b52d04589a8445f45b7079568dbdfb.html?match=Exact',
        # # 'Cookie': 'redSpot=false; pkulaw_v6_sessionid=tbzw3vtjm4tyhttgotxl35t0; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; xCloseNew=11'
        # # 'Cookie': 'Catalog_Search=; ASP.NET_SessionId=spcqaqc2s4o0wo44wqmpq3ff; QINGCLOUDELB=b1262d52db822794d00c3069ee5bd621ec61ed2f1b6f7d61f04556fafeaf0c45; CookieId=nxms1otryaob51eiuakv3gdc; CheckIPAuto=; CheckIPDate=2020-01-10 18:23:11; User_User=phone2020010610184515819; bdyh_record=1970324901429167%2C1970324901429169%2C1970324904312067%2C1970324905695111%2C1970324848373893%2C1970324905695537%2C1970324901429168%2C1970324848373860%2C1970324923942454%2C1970324848266918%2C1970324904617424%2C1970324846989066%2C1970324847175278%2C1970324904617425%2C1970324904312066%2C1970324846989064%2C1970324904617426%2C1970324904312068%2C1970324904617423%2C1970324923942453%2C'
        # 'Cookie': 'ASP.NET_SessionId=tigxfhukj3h1p5empnlhbvyb; QINGCLOUDELB=b1262d52db822794d00c3069ee5bd621ec61ed2f1b6f7d61f04556fafeaf0c45; CookieId=tigxfhukj3h1p5empnlhbvyb; CheckIPAuto=; CheckIPDate=2020-01-10 20:38:30; User_User=phone2020010610184515819; FWinCookie=1'
        # # 'Cookie': 'pkulaw_v6_sessionid=tbzw3vtjm4tyhttgotxl35t0; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1578636966; xCloseNew=11'
    }
    data1 = {
        'library': 'pfnl',
        'gid': 'a6bdb3332ec0adc47f1db9bdb22905b97700c455564b7ea3bdfb',
        'type': 'txt',
        'jiamizi': ''
    }
    # url1 = 'https://www.pkulaw.com/Tool/CheckDownloadLimit'
    # url1 = 'https://v6downloadservice.pkulaw.com/full/downloadfile'
    url1 = 'https://www.pkulaw.cn/case/FullText/DownloadFile?'+urlencode(data1)
    try:
        reqcookie()
        with open('./Cookies/req_Cookies.txt','r',encoding = 'utf-8') as f1:
            headers1.update('Cookie')
        print("Requesting Pages...")
        print(headers1.get('Cookie'))
        # ses = requests.Session()
        res = requests.get(url = url1, headers = headers1, data = data1, stream = True)
        print(res.status_code)
        if res.status_code == 200:
            # urlretrieve(res.url, './download/test2.txt')
            with open('./download/test3.txt', 'wb') as f:
                for chunk in res.iter_content(chunk_size = 32):  # chunk_size #设置每次下载文件的大小
                    f.write(chunk)  # 每一次循环存储一次下载下来的内容
            with open('./download/test3.txt', 'r', encoding = 'GBK') as f:
                lines = f.readlines()
                first_line = lines[0]
                # print(first_line)
                key = "尚未登录"
                if key in first_line:
                    print(first_line+"请先登录获取cookie")
                else:
                    print('您的账号已经登陆')
            f.close()
            print("return html....")
        else:
            print("unable to download...")
        # print(html)
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

# getgid(url,data,headers)
# post_spider(url,data,headers)
# r = requests.post(url,data = data, headers = headers, timeout = 10)
# print(r.status_code)
# r= requests.post(url,headers,timeout=10)
# print(r.status_code)
# singeldownload()

def reqcookie():
    url2 = "https://www.pkulaw.cn/case/CheckLogin/Login"
    data2 = {
        'menu': 'case',
        'UserName': '16567408533',
        'PassWord': '16567408533',
    }
    headers2 = {
        'Host': 'www.pkulaw.cn',
        'Connection': 'keep-alive',
        'Content-Length': '114',
        'Origin': 'https: // www.pkulaw.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.pkulaw.cn/Case/',
        'Accept-Encoding': 'gzip, deflate, br',
        'CheckIPDate': time.strftime('%y%y-%m-%d %H:%M:%S',time.localtime()),
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    response = requests.Session()
    res = response.post(url = url2, data = data2, headers = headers2, timeout = 10)
    cookie = res.cookies.get_dict()
    t = res.request.headers.get('CheckIPDate')
    # print(t)
    # print(cookie)
    # print(cookie.get('CookieId'))
    os.makedirs('./Cookies/',exist_ok = True)
    with open('./Cookies/req_Cookies.txt','w',encoding = 'utf-8') as f:
        for key,value in cookie.items():
            f.write(key+': '+string(value)+'; ')
        f.write('CheckIPAuto=; ')
        f.write('CheckIPDate: '+t+'; ')
        f.write('User_User=phone2020010610184515819; FWinCookie=1')
        # 'Cookie': 'ASP.NET_SessionId=tigxfhukj3h1p5empnlhbvyb; QINGCLOUDELB=b1262d52db822794d00c3069ee5bd621ec61ed2f1b6f7d61f04556fafeaf0c45; CookieId=tigxfhukj3h1p5empnlhbvyb; CheckIPAuto=; CheckIPDate=2020-01-10 20:38:30; User_User=phone2020010610184515819; FWinCookie=1'
        # # 'Cookie': 'pkulaw_v6_sess
    f.close()


# reqcookie()
singeldownload()


def test_time():
    local_t = time.strftime('%y%y-%m-%d %H:%M:%S',time.localtime())
    print(local_t)


# test_time()