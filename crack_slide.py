import random
import time

import chardet
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from Cookie_pool.account_saver import RedisClient
from image_process import image_process
import cv2 as cv
import numpy as np
import math

CONN = RedisClient('account', 'pkulaw')


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


class crack_slide( ):
    def __init__(self):
        self.driver = webdriver.Chrome( )
        self.driver.maximize_window( )
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://www.pkulaw.com/case/'

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

        bg = cv.GaussianBlur(bg, (1, 1), -10)
        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
        # bg = cv.Canny(bg, 100, 200)
        result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(np.argmax(result), result.shape)
        print(x, y)

        # w, h = front.shape
        # cv.rectangle(bg, (y, x), (y + w, x + h), (7, 249, 151), 2)
        # cv.imwrite("gray.jpg", bg)
        # self.show(bg)

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
        self.wait.until(Ec.presence_of_element_located(self.locator(By.ID, "recordgroup"))).click( )
        time.sleep(1)
        self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="recordgroup"]/a[2]'))).click( )
        # self.driver.find_element(by = 'id', value = 'recordgroup').click( )
        # time.sleep(3)
        # self.driver.find_element(by = 'xpath', value = '//*[@id="recordgroup"]/a[2]').click( )
        time.sleep(1)
        self.wait.until(Ec.presence_of_element_located(
            self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a'))).click( )
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a').click( )
        time.sleep(1)
        self.wait.until(Ec.presence_of_element_located(
            self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]'))).click( )
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]').click( )
        time.sleep(1)
        self.wait.until(Ec.presence_of_element_located(
            self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]'))).click( )
        # self.driver.find_element(by = 'xpath',
        # value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]').click( )
        # time.sleep(7)
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[3]/a').click()

    def autopage(self, num):
        time.sleep(2)
        self.wait.until(Ec.presence_of_element_located(
            self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[' + str(num) + ']/a'))).click( )
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

    def login(self):
        account = CONN.random_key( )
        aps = account
        self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="newloginbtn"]'))).click( )
        time.sleep(1)
        username = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="inputUserName"]')))
        username.click( )
        username.clear( )
        username.send_keys(account)
        userpassword = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="inputPwd"]')))
        userpassword.click( )
        userpassword.clear( )
        userpassword.send_keys(aps)
        time.sleep(1)
        self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="loginByUserName"]'))).click( )
        time.sleep(1)

    def crack(self):
        self.driver.get(self.url)
        # time.sleep(1)
        # self.login()
        # time.sleep(1)
        self.req_page()
        time.sleep(1)
        for num in range(4, 10):
            try:
                self.autopage(num)
            except Exception as e:
                pass
            slide_ing = self.image_capture( )
            x, y = self.process( )
            rs = get_path(y + 9)
            for r in rs:
                ActionChains(self.driver).move_by_offset(xoffset = r, yoffset = 0).perform( )
            time.sleep(0.002)
            time.sleep(1)
            ActionChains(self.driver).release(slide_ing).perform( )
            time.sleep(10)
            sc = self.driver.page_source
            print(sc)
        time.sleep(100)
        self.driver.close( )
        # self.move_to_gap(self.driver, slide, track)

        # ActionChains(self.driver).drag_and_drop_by_offset(div, xoffset = y, yoffset = 0).perform( )


cs = crack_slide( )
cs.crack( )
