import re
import ssl
from urllib import request

from bs4 import BeautifulSoup
from soupsieve.util import string

url = "F:\BDFB-spider\Sample\\test5.html"
# content = urlopen(url).read()
context = open(url, 'r', encoding = 'utf-8').read( )
print(type(context))
content = string(BeautifulSoup(context, 'html.parser'))
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
results = re.findall('<input.*?checkbox.*?checkbox.*?value="(a.*?)"/>', content, re.S)
print(results)
print(len(results))
# for result in results:
#     print(result[1])