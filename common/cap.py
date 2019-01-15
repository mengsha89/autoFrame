# coding=utf-8
# author:ss

from __future__ import division
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # 等待元素加载的
from selenium.webdriver.common.action_chains import ActionChains  # 拖拽
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import time
import random
from io import BytesIO
import numpy as np
import cv2


class CrackSlider(object):
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1

    def open(self):
        self.driver.get(self.url)

    def get_pic(self):
        time.sleep(2)
        tem = '//*[@id="captcha"]/div/div[1]/div/div[1]/img[@class="yidun_jigsaw"]'
        tar = '//*[@id="captcha"]/div/div[1]/div/div[1]/img[@class="yidun_bg-img"]'
        #
        # user = '//*[@id="captcha"]/div/div[2]/div[2]'
        # btn = self.driver.find_element_by_xpath(user)
        #
        # ActionChains(self.driver).move_to_element(btn).perform()
        refresh = '//*[@id="captcha"]/div/div[1]/div/div[3]'
        tip = '//*[@id="captcha"]/div/div[2]/div[3]/span[2]'

        code = '//*[@id="captcha"]/div/div[2]'
        code_input = self.driver.find_element_by_xpath(code)
        refresh_btn = self.driver.find_element_by_xpath(refresh)
        tip_text = self.driver.find_element_by_xpath(tip).text
        while tip_text == u"加载失败":
            refresh_btn.click()
        target = self.driver.find_element_by_xpath(tar)
        template = self.driver.find_element_by_xpath(tem)
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        tar_pic = requests.get(target_link).content
        tem_pic = requests.get(template_link).content
        target_img = Image.open(BytesIO(tar_pic))
        template_img = Image.open(BytesIO(tem_pic))
        target_img.save('target.jpg')
        template_img.save('template.png')
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        pic_size = int(size_loc[0])
        self.zoom = 232 / pic_size
        print "图片大小：%s" % pic_size
        print "232 / int(size_loc[0]):%s" % (232 / pic_size)
        print "阈值为：%s" % self.zoom

    def match(self, target, template):
        # 读取图片: cv2.imread(路径,num) 其中num=0，为灰度图像；num=1为彩图
        img_rgb = cv2.imread(target)
        # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        # 记录图像模板的尺寸
        w, h = template.shape[::-1]
        print(w, h)
        # 使用matchTemplate对原始灰度图像和图像模板进行匹配
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            print("threshold:%s" % threshold)
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            # print("res为%s，x坐标为%s:" % (res, len(loc[1])))
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                # # 使用灰度图像中的坐标对原始RGB图像进行标记
                # for pt in zip(*loc[::-1]):
                #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
                # cv2.imshow('Detected', img_rgb)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                break
            elif len(loc[1]) < 1:
                R -= (R - L) / 2
        return loc[1][0]

    def get_tracks(self, distance):
        """
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+(1/2)at²
        ③v²-v0²=2as

        :param distance: 需要移动的距离
        :return: 存放每0.2秒移动的距离
        """
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 7/8

        distance += 10  # 先滑过一点，最后再反着滑动回来
        # a = random.randint(1,3)
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(2, 4)  # 加速运动
            else:
                a = -random.randint(3, 5)  # 减速运动

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0*t+0.5*a*(t**2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0+a*t

        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    def main_check_code(self, track_list):
        """
        拖动识别验证码
        :param track_list:
        :return:
        """
        print('第一步,点击滑动按钮')
        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="captcha"]/div/div[2]/div[2]')))
        ActionChains(self.driver).click_and_hold(slider).perform()  # 点击鼠标左键，按住不放
        time.sleep(1)
        print('第二步,拖动元素')
        for track in track_list:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            time.sleep(0.002)

        ActionChains(self.driver).move_by_offset(xoffset=-random.randint(2, 5), yoffset=0).perform()
        time.sleep(1)
        print('第三步,释放鼠标')
        ActionChains(self.driver).release().perform()
        time.sleep(5)


if __name__ == '__main__':
    url = "https://www.aixuexi.com/"
    cs = CrackSlider(url)
    try:
        count = 6  # 最多识别6次
        cs.open()
        while count > 0:
            target = 'target.jpg'
            template = 'template.png'
            cs.get_pic()
            distance = cs.match(target, template)
            tracks = cs.get_tracks((distance + 7) * cs.zoom)  # 对位移的缩放计算
            cs.main_check_code(tracks)
            time.sleep(2)
            try:
                success_element = cs.driver.find_element_by_xpath('//*[@id="captcha"]/input[@name="NECaptchaValidate"]')
                validate = success_element.get_attribute("value")
                if validate:
                    print('成功识别！！！！！！')
                    count = 0
                    break
            except NoSuchElementException as e:
                print('识别错误，继续')
                count -= 1
                time.sleep(2)
        else:
            print('too many attempt check code ')
            exit('退出程序')
    finally:
        pass
        # cs.driver.close()

