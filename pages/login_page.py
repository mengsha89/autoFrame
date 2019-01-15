# coding=utf-8
# author:ss

from core.base_page import Page
from common.slide_vali_code import *
from selenium.common.exceptions import NoSuchElementException


class LoginPage(Page):
    username_input = ('xpath', '//*[@id="loginForm"]/input[1]')
    pwd_input = ('xpath', '//*[@id="loginForm"]/input[2]')
    login_btn = ('xpath', '//*[@id="submit"]')

    def __init__(self, url='https://www.aixuexi.com/', browser_type='chrome'):
        super(LoginPage, self).__init__(browser_type=browser_type)
        self.wait = WebDriverWait(self.driver, 20)
        self.zoom = 1
        self.url = url

    def open_index(self):
        self.get(self.url)

    def type_text(self, username, password):
        self.type(self.username_input, username)
        self.type(self.pwd_input, password)

    def click_login(self):
        self.click(self.login_btn)

    def slide_validate_code(self):
        try:
            count = 6  # 最多识别6次
            while count > 0:
                target = 'target.jpg'
                template = 'template.png'
                zoom = get_pic(self.driver)
                distance = match_pic(target, template)
                tracks = get_tracks((distance + 7) * zoom)  # 对位移的缩放计算
                main_check_code(self.driver, tracks)
                time.sleep(2)
                try:
                    success_element = self.driver.find_element_by_xpath(
                        '//*[@id="captcha"]/input[@name="NECaptchaValidate"]')
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


lp = LoginPage()
lp.open_index()
lp.type_text("15912348888", "ss123456")
lp.slide_validate_code()
lp.click_login()