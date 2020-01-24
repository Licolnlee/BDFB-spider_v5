from telnetlib import EC

import chardet
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait



browser = webdriver.Chrome()
# try:
url1 = 'https://www.pkulaw.com/case/'
browser.get(url1)
input1 = browser.find_element_by_id('recordgroup')
input1.click()
input2 = browser.find_elements_by_xpath('//*[@id="recordgroup"]/a[2]')
# for i in brwser.find_elements_by_xpath('//*[@id="recordgroup"]/a[2]'):
#     i.click()
#     WebDriverWait(browser, 40)
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)
# finally:
#     browser.close()
