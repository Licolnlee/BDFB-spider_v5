import random
import time
from telnetlib import EC

import chardet
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import cv2 as cv
import numpy as np
import math


#
#
# def ease_out_quad(x):
#     return 1 - (1 - x) * (1 - x)
#
#
# def ease_out_quart(x):
#     return 1 - pow(1 - x, 4)
#
#
# def ease_out_expo(x):
#     if x == 1:
#         return 1
#     else:
#         return 1 - pow(2, -10 * x)
#
#
# def get_tracks(distance, seconds, ease_func):
#     tracks = [0]
#     offsets = [0]
#     for t in np.arange(0.0, seconds, 0.1):
#         ease = globals( )[ease_func]
#         offset = round(ease(t / seconds) * distance)
#         tracks.append(offset - offsets[-1])
#         offsets.append(offset)
#     return offsets, tracks
#
# def drag_and_drop(browser, offset):
#     knob = browser.find_element_by_class_name("gt_slider_knob")
#     offsets, tracks = easing.get_tracks(offset, 12, 'ease_out_expo')
#     ActionChains(browser).click_and_hold(knob).perform()
#     for x in tracks:
#         ActionChains(browser).move_by_offset(x, 0).perform()
#     ActionChains(browser).pause(0.5).release().perform()


class crack_slide( ):
    def __init__(self):
        self.driver = webdriver.Chrome( )
        self.driver.maximize_window( )
        self.wait = WebDriverWait(self.driver, 5)
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

    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0.1
        r = [1.1, 1.2, 1.3, 1.4, 1.5]
        p = [2, 2.5, 2.8, 3, 3.5, 3.6]
        q = 5.0
        i = 0
        while current < distance:
            if current < mid:
                a = 2
                q = q * 0.9
            else:
                q = 1.0
                a = -3
            v0 = v
            v = v0 + a * t
            r1 = random.choice(r)
            p1 = random.choice(p)
            move = r1 * v0 * t + 1 / p1 * a * t * t * q
            if i == 2:
                currentdis = (distance - current) / random.choice([3.5, 4.0, 4.5, 5.0])
            elif i == 4:
                currentdis = (distance - current) / random.choice([4.0, 5.0, 6.0, 7.0])
                current += currentdis
                track.append(round(currentdis))
            else:
                current += move
                track.append(round(move))
                # 加入轨迹
            i = i + 1
            return track

    def get_slide(self, browser):
        slide = None
        while True:
            try:
                slide = self.driver.find_element(by = 'xpath', value = '//*[@id="drag"]/div[3]')
                break
            except:
                break
        return slide

    def move_to_gap(self, browser, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(browser).click_and_hold(slider).perform( )
        time.sleep(0.5)
        while track:
            x = random.choice(track)
            y = 0
            ActionChains(browser).move_by_offset(xoffset = x, yoffset = y).perform( )
            track.remove(x)
            t = random.choice([0.002, 0.003, 0.004, 0.005, 0.006])
            time.sleep(t)
        time.sleep(1)
        ActionChains(browser).release(on_element = slider).perform( )

    def crack(self):
        self.driver.get(self.url)
        self.driver.find_element(by = 'id', value = 'recordgroup').click( )
        time.sleep(3)
        self.driver.find_element(by = 'xpath', value = '//*[@id="recordgroup"]/a[2]').click( )
        time.sleep(3)
        self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/h4/a').click( )
        time.sleep(5)
        self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]').click( )
        time.sleep(5)
        self.driver.find_element(by = 'xpath',
                                 value = '//*[@id="rightContent"]/div[2]/div/div[1]/div/div[2]/div/dl/dd[4]').click( )
        # time.sleep(7)
        # self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[3]/a').click()
        time.sleep(7)
        self.driver.find_element(by = 'xpath', value = '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[4]/a').click( )
        time.sleep(5)
        img = self.driver.find_element(by = 'xpath', value = '//*[@id="bgImg"]').screenshot('./download/sc.png')
        time.sleep(1)
        div = self.driver.find_element(by = 'xpath', value = '//*[@id="drag"]/div[3]')
        ActionChains(self.driver).click_and_hold(div).perform( )
        time.sleep(1)
        img = self.driver.find_element(by = 'xpath', value = '//*[@id="xy_img"]').screenshot('./download/nc.png')

        bg = cv.imread('./download/sc.png')
        front = cv.imread('./download/nc.png')

        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)

        result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
        np.argmax(result)
        x, y = np.unravel_index(np.argmax(result), result.shape)

        # track = self.get_track(y)
        # slide = self.get_slide(self.driver)


        ActionChains(self.driver).drag_and_drop_by_offset(div, xoffset = y, yoffset = 0).perform( )
        ActionChains(self.driver).release(div).perform( )
        # self.move_to_gap(self.driver, slide, track)


        # ActionChains(self.driver).drag_and_drop_by_offset(div, xoffset = y, yoffset = 0).perform( )


cs = crack_slide( )
cs.crack( )
