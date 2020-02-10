import json
import random
import shutil
import time

import chardet
import cv2 as cv
import numpy as np
import redis
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
from Cookie_pool.account_saver import RedisClient

pool = redis.ConnectionPool(host = 'localhost', port = 6379, db = 1, password = '')
r_pool = redis.StrictRedis(connection_pool = pool, charset = 'UTF-8', errors = 'strict', decode_responses = True,
                           unix_socket_path = None)
r_pipe = r_pool.pipeline()

CONN = RedisClient('account', 'pkulaw')
FLAG = True


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


def get_path(distance):
    result = []
    current = 0
    mid = distance * 7 / 8
    t = 0.2
    v = 0
    while current < (distance - 10):
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * t * t
        current += s
        result.append(round(s))
    return result


def parse_page(html):
    print('processing...')
    try:
        doc = pq(html, parser = 'html')
        items = doc('.block').items( )
        i = 0
        for item in items:
            gid = item('input').attr('value')
            # print(gid)
            name = item('h4 a').text( )
            # print(name)
            related_info = item('.related-info').text( )
            issue_type = related_info.split(' / ')[0]
            # print(issue_type)
            court_name = related_info.split(' / ')[1]
            # print(court_name)
            issue_num = related_info.split(' / ')[2]
            # print(issue_num)
            issue_date = related_info.split(' / ')[-1]
            # print(issue_date)
            dg = dict(gid = gid, issue_type = issue_type, court_name = court_name, issue_num = issue_num,
                      issue_date = issue_date)
            en_json_dg = json.dumps(dg, ensure_ascii = False, indent = 4).encode('UTF-8')
            r_pipe.hset('crawldata', name, en_json_dg)
            r_pipe.hset('downloadreqdata', name, gid)
            r_pipe.execute( )
            i += 1
        print('completed...')
    except Exception as e:
        print(e)
        pass


class crack_slide( ):
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.proxy = get_proxy()
        desired_capabilities = self.option.to_capabilities()
        desired_capabilities['proxy'] = {
            "httpProxy": self.proxy,
            "ftpProxy": None,
            "sslProxy": None,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # self.option.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options = self.option, desired_capabilities = desired_capabilities)
        self.driver.maximize_window()
        self.wait = WebDriverWait(driver = self.driver, timeout = 10)
        self.driver.implicitly_wait(10)
        self.url = 'https://www.pkulaw.com/case/'
        self.COUNT = 0

    # chrome_options = webdriver.ChromeOptions( )
    # chrome_options.add_argument("--start-maximized")
    # driver = webdriver.Chrome(chrome_options = chrome_options)

    # 鼠标悬停
    def hover(self, by, value):
        element = self.findElement(by, value)
        ActionChains(self.driver).move_to_element(element).perform( )

    # 通过不同的方式查找界面元素
    def findElement(self, by, value):
        if by == "id":
            element = self.driver.find_element_by_id(value)
            return element
        elif by == "name":
            element = self.driver.find_element_by_name(value)
            return element
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
            return element
        elif by == "classname":
            element = self.driver.find_element_by_class_name(value)
            return element
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
            return element
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
            return element
        else:
            print("无对应方法，请检查")
            return None

    def process(self):
        bg = cv.imread('./download/sc.png')
        front = cv.imread('./download/nc.png')

        print(bg.shape)
        print(front.shape)
        for i in range(bg.shape[0]):
            for j in range(bg.shape[1]):
                if bg[i][j][0] >= 157 and bg[i][j][1] >= 157 and bg[i][j][2] >= 157:
                    bg[i][j] = (0, 0, 0)
        front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        bg = cv.GaussianBlur(bg, (1, 1), -10)
        result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(np.argmax(result), result.shape)
        print(x, y)
        return x, y

    #
    # # def get_track(self, distance):
    # #     track = []
    # #     current = 0
    # #     mid = distance * 4 / 5
    # #     t = 0.2
    # #     v = 0.1
    # #     r = [1.1, 1.2, 1.3, 1.4, 1.5]
    # #     p = [2, 2.5, 2.8, 3, 3.5, 3.6]
    # #     q = 5.0
    # #     i = 0
    # #     while current < distance:
    # #         if current < mid:
    # #             a = 2
    # #             q = q * 0.9
    # #         else:
    # #             q = 1.0
    # #             a = -3
    # #         v0 = v
    # #         v = v0 + a * t
    # #         r1 = random.choice(r)
    # #         p1 = random.choice(p)
    # #         move = r1 * v0 * t + 1 / p1 * a * t * t * q
    # #         if i == 2:
    # #             currentdis = (distance - current) / random.choice([3.5, 4.0, 4.5, 5.0])
    # #         elif i == 4:
    # #             currentdis = (distance - current) / random.choice([4.0, 5.0, 6.0, 7.0])
    # #             current += currentdis
    # #             track.append(round(currentdis))
    # #         else:
    # #             current += move
    # #             track.append(round(move))
    # #             # 加入轨迹
    # #         i = i + 1
    # #         return track
    #
    # def get_track(self, distance):
    #     """
    #     模拟轨迹 假装是人在操作
    #     :param distance:
    #     :return:
    #     """
    #     # 初速度
    #     v = 0
    #     # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    #     t = 0.2
    #     # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    #     tracks = []
    #     # 当前的位移
    #     current = 0
    #     # 到达mid值开始减速
    #     mid = distance * 7 / 8
    #
    #     distance += 10  # 先滑过一点，最后再反着滑动回来
    #     # a = random.randint(1,3)
    #     while current < distance:
    #         if current < mid:
    #             # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
    #             a = random.randint(2, 4)  # 加速运动
    #         else:
    #             a = -random.randint(3, 5)  # 减速运动
    #
    #         # 初速度
    #         v0 = v  # 0.2秒时间内的位移
    #         s = v0 * t + 0.5 * a * (t ** 2)
    #         # 当前的位置
    #         current += s  # 添加到轨迹列表
    #         tracks.append(round(s))
    #
    #         # 速度已经达到v,该速度作为下次的初速度
    #         v = v0 + a * t  # 反着滑动到大概准确位置
    #     for i in range(4):
    #         tracks.append(-random.randint(2, 3))
    #     for i in range(4):
    #         tracks.append(-random.randint(1, 3))
    #     return tracks

    # def get_slide(self, browser):
    #     slide = None
    #     while True:
    #         try:
    #             slide = self.driver.find_element(by = 'xpath', value = '//*[@id="drag"]/div[3]')
    #             break
    #         except:
    #             break
    #     return slide

    # def move_to_gap(self, browser, slider, track):
    #     """
    #     拖动滑块到缺口处
    #     :param slider: 滑块
    #     :param track: 轨迹
    #     :return:
    #     """
    #     ActionChains(browser).click_and_hold(slider).perform( )
    #     time.sleep(0.5)
    #     while track:
    #         x = random.choice(track)
    #         y = 0
    #         ActionChains(browser).move_by_offset(xoffset = x, yoffset = y).perform( )
    #         track.remove(x)
    #         t = random.choice([0.002, 0.003, 0.004, 0.005, 0.006])
    #         time.sleep(t)
    #     time.sleep(1)
    #     ActionChains(browser).release(on_element = slider).perform( )

    def locator(self, method, path):
        locator = (method, path)
        return locator

    def image_capture(self):
        time.sleep(1)
        bk_block = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="bgImg"]')))
        img = bk_block.screenshot('./download/sc.png')
        # web_image_width = bk_block.size
        # web_image_width = web_image_width['width']
        # bk_block_x = bk_block.location['x']
        # img = self.driver.find_element(by = 'xpath', value = '//*[@id="bgImg"]').screenshot('./download/sc.png')
        time.sleep(1)
        slide_ing = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/div[3]')))
        # div = self.driver.find_element(by = 'xpath', value = '//*[@id="drag"]/div[3]')
        ActionChains(self.driver).click_and_hold(slide_ing).perform( )
        time.sleep(1)
        slide_block = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="xy_img"]')))
        # slide_block_x = slide_block.location['x']
        img1 = slide_block.screenshot('./download/nc.png')
        # img_bkblock = Image.open('./image/bkBlock.png')
        # real_width = img_bkblock.size[0]
        # width_scale = float(real_width) / float(web_image_width)

        # img = self.driver.find_element(by = 'xpath', value = '//*[@id="xy_img"]').screenshot('./download/nc.png')

        # real_position = position[1] / width_scale
        # real_position = real_position - (slide_block_x - bk_block_x)
        # track_list = self.get_track(real_position + 4)
        return slide_ing

    def req_page(self):
        try:
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="recordgroup"]/a[1]'))).click( )
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="recordgroup"]/a[2]'))).click( )
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a'))).click( )
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]'))).click( )
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]'))).click( )
            time.sleep(2)
            self.autopass( )
            time.sleep(2)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[2]/ul/li[1]/a'))).click( )
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[7]/ul/li[1]/a'))).click( )
            # time.sleep(1)
            # self.wait.until(Ec.presence_of_element_located(
            #     self.locator(By.XPATH, '//*[@id="rightContent"]/div[3]/div/div[1]/div/div[2]/div/dl/dd[4]'))).click( )
            # time.sleep(1)
            # self.wait.until(Ec.presence_of_element_located(
            #     self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/h4/a[1]'))).click( )
            time.sleep(3)

        except Exception as e:
            print(e)
        # self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[2]/ul/li[1]/a'))).click( )
        # # self.wait.until(Ec.presence_of_element_located(self.locator(By.ID, "recordgroup"))).click( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(
        #     self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[7]/h4/a[1]'))).click( )
        # # self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="recordgroup"]/a[2]'))).click( )
        # # self.driver.find_element(by = 'id', value = 'recordgroup').click( )
        # # time.sleep(3)
        # # self.driver.find_element(by = 'xpath', value = '//*[@id="recordgroup"]/a[2]').click( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[7]/ul/li[1]/a'))).click( )
        # # self.wait.until(Ec.presence_of_element_located(
        # #     self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a'))).click( )
        # # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a').click( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(
        #     self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/h4/a[1]'))).click( )
        # # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]').click( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(
        #     self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]'))).click( )
        # self.driver.find_element(by = 'xpath',
        # value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]').click( )
        # time.sleep(7)
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[3]/a').click()

    def autoTraversal_f(self, num):
        print('autoTraversaling...')
        try:
            time.sleep(3)
            province_button = self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/ul/li[' + str(num) + ']/a')))
            # value = province_button.get_attribute("cluster_code")
            # print(value)
            # print(num)
            # # n_str = str(num)
            # # n_z = n_str.zfill(2)
            # # print(n_z)
            # self.driver.execute_script("return arguments[0].setAttribute('cluster_code',"+str(num)+");", province_button)
            # value = province_button.get_attribute("cluster_code")
            # print(value)
            time.sleep(3)
            province_button.click( )
        except Exception as e:
            print(e)
            print('unclickable...')

    def autoTraversal_p(self, num):
        print('autoTraversaling...')
        try:
            time.sleep(3)
            province_button = self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/ul/li[2]/a')))
            value = province_button.get_attribute("cluster_code")
            print(value)
            print(num)
            # n_str = str(num)
            # n_z = n_str.zfill(2)
            # print(n_z)
            self.driver.execute_script("return arguments[0].setAttribute('cluster_code'," + str(num) + ");",
                                       province_button)
            value = province_button.get_attribute("cluster_code")
            print(value)
            time.sleep(3)
            province_button.click( )
        except Exception as e:
            print(e)
            print('unclickable...')
        # self.wait.until(Ec.presence_of_element_located(
        #     self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[' + str(num) + ']/a'))).click( )
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[4]/a').click( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="bgImg"]'))).screenshot(
        #     './download/sc.png')
        # # img = self.driver.find_element(by = 'xpath', value = '//*[@id="bgImg"]').screenshot('./download/sc.png')
        # time.sleep(1)
        # div = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/div[3]')))
        # # div = self.driver.find_element(by = 'xpath', value = '//*[@id="drag"]/div[3]')
        # ActionChains(self.driver).click_and_hold(div).perform( )
        # time.sleep(1)
        # self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="xy_img"]'))).screenshot(
        #     './download/nc.png')
        # # img = self.driver.find_element(by = 'xpath', value = '//*[@id="xy_img"]').screenshot('./download/nc.png')

        # track = self.get_track(y)
        # slide = self.get_slide(self.driver)

    def autoreturn(self):
        print('autoreturning...')
        try:
            time.sleep(5)
            self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/h4/a[3]'))).click( )
            time.sleep(2)
        except Exception as e:
            print(e)

    def autopage(self, num):
        print('paging...')
        try:
            time.sleep(5)
            n_page = self.wait.until(Ec.presence_of_element_located(
                self.locator(By.XPATH, '//*[@id="rightContent"]/div[3]/div/div[3]/ul/li[2]/a')))
            value = n_page.get_attribute("pageindex")
            print(n_page)
            print(value)
            self.driver.execute_script("arguments[0].setAttribute('pageindex'," + str(num) + ");", n_page)
            value = n_page.get_attribute("pageindex")
            print(n_page)
            print(value)
            time.sleep(1)
            n_page.click( )
        except Exception as e:
            print(e)

    def login(self):
        try:
            account = CONN.random_key( )
            aps = account
            time.sleep(1)
            self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="newloginbtn"]'))).click( )
            time.sleep(1)
            username = self.wait.until(
                Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="inputUserName"]')))
            username.click( )
            username.clear( )
            username.send_keys(account)
            time.sleep(1)
            userpassword = self.wait.until(
                Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="inputPwd"]')))
            userpassword.click( )
            userpassword.clear( )
            userpassword.send_keys(aps)
            time.sleep(1)
            self.wait.until(
                Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="loginByUserName"]'))).click( )
            time.sleep(1)
        except Exception as e:
            print(e)

    def autocheck(self):
        try:
            print('autochecking...')
            time.sleep(1)
            if self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/div[3]'))):
                print('Trying ' + str(self.COUNT) + ' times...')
                shutil.copyfile('./download/sc.png', './error/error_sc' + str(self.COUNT) + '.png')
                shutil.copyfile('./download/nc.png', './error/error_nc' + str(self.COUNT) + '.png')
                time.sleep(1)
                self.wait.until(
                    Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/a/div'))).click( )
                print('Refreshing...')
                self.COUNT += 1
                return True
        except Exception as e:
            print(e)
            print('Verification success...')
            return False

    def vpass(self):
        print('verification passing...')
        try:
            time.sleep(1)
            slide_ing = self.image_capture( )
            x, y = self.process( )
            rs = get_path(y + 8.94)
            for r in rs:
                ActionChains(self.driver).move_by_offset(xoffset = r, yoffset = 0).perform( )
            time.sleep(0.002)
            time.sleep(1)
            ActionChains(self.driver).release(slide_ing).perform( )
            time.sleep(1)
        except Exception as e:
            print(e)

    def autopage_f(self):
        try:
            time.sleep(2)
            sc = self.driver.page_source
            parse_page(sc)
            time.sleep(5)
            self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="rightContent"]/div[3]/div/div[3]/ul/li[3]/a'))).click()
            time.sleep(2)
        except Exception as e:
            print(e)

    def autopage_p(self, num):
        try:
            sc = self.driver.page_source
            parse_page(sc)
            time.sleep(5)
            self.autopage(num)
            self.vpass( )
            while self.autocheck( ):
                self.vpass( )
            time.sleep(2)
        except Exception as e:
            print(e)

    def autopass(self):
        try:
            print('autopassing first time...')
            time.sleep(3)
            p_icon = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[5]/h4/a[1]')))
            value = p_icon.get_attribute("isno")
            print(p_icon)
            print(value)
            self.driver.execute_script("arguments[0].setAttribute('isno', 'false');", p_icon)
            value = p_icon.get_attribute("isno")
            print(p_icon)
            print(value)
            time.sleep(1)
            print('autopassing second time...')
            time.sleep(3)
            i_icon = self.wait.until(
                Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="leftContent"]/div[1]/div[7]/h4/a[1]')))
            value = i_icon.get_attribute("isno")
            print(i_icon)
            print(value)
            self.driver.execute_script("arguments[0].setAttribute('isno', 'false');", i_icon)
            value = i_icon.get_attribute("isno")
            print(i_icon)
            print(value)
            time.sleep(1)
        except Exception as e:
            print(e)

    def crack(self, fnum, lnum):
        self.driver.get(self.url)
        # self.login( )
        self.req_page( )

        try:
            for p_num in range(2, 32):
                if p_num < 10:
                    self.autoTraversal_f(p_num)
                    for num in range(fnum, lnum):
                        if num < 3:
                            self.autopage_f()
                        else:
                            self.autopage_p(num)
                    self.autoreturn( )
                else:
                    self.autoTraversal_p(p_num)
                    for num in range(fnum, lnum):
                        if num < 3:
                            self.autopage_f()
                        else:
                            self.autopage_p(num)
        except Exception as e:
            print(e)
            pass
        print('Completed...waiting....')
        time.sleep(100)
        print('closing...')
        self.driver.close( )


cs = crack_slide()
cs.crack(2, 4)
