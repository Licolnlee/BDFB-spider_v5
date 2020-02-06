import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class get_img( ):

    def __init__(self):
        self.driver = webdriver.Chrome( )
        self.driver.maximize_window( )
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://www.pkulaw.com/case/'

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
        time.sleep(3)
        self.wait.until(Ec.presence_of_element_located(
            self.locator(By.XPATH, '//*[@id="rightContent"]/div[2]/div/div[3]/ul/li[' + str(num) + ']/a'))).click( )

    def locator(self, method, path):
        locator = (method, path)
        return locator

    def image_capture(self, i):
        time.sleep(1)
        bk_block = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="bgImg"]')))
        img = bk_block.screenshot('./download/sc'+str(i)+'.jpg')
        time.sleep(1)
        slide_ing = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/div[3]')))
        ActionChains(self.driver).click_and_hold(slide_ing).perform( )
        time.sleep(1)
        slide_block = self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="xy_img"]')))
        img1 = slide_block.screenshot('./download/nc'+str(i)+'.jpg')
        self.wait.until(Ec.presence_of_element_located(self.locator(By.XPATH, '//*[@id="drag"]/a/div'))).click()
        time.sleep(1)
        print('refreshing...')

    def crack(self):
        self.driver.get(self.url)
        self.req_page( )
        time.sleep(10)
        num = 4
        self.autopage(num)
        while True:
            for i in range(0, 120):
                self.image_capture(i)


gi = get_img()
gi.crack()