# coding=utf-8
# author:ss


import time
import os
from selenium import webdriver
from config import driver_path, screenshot_path

# 可根据需要自行扩展
CHROMEDRIVER_PATH = driver_path + '\chromedriver.exe'
IEDRIVER_PATH = driver_path + '\IEDriverServer.exe'
PHANTOMJSDRIVER_PATH = driver_path + '\phantomjs.exe'

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie, 'phantomjs': webdriver.PhantomJS}
EXECUTABLE_PATH = {'firefox': 'wires', 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH, 'phantomjs': PHANTOMJSDRIVER_PATH}


class UnSupportBrowserTypeError(Exception):
    pass


class Browser(object):
    def __init__(self, browser_type='chrome', remoteAddress=None):
        """
        remote consle：
        dr = Browser('Chrome','127.0.0.1:8080')
        """
        self._type = browser_type
        t1 = time.time()
        dc = {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': True}
        dr = None
        if remoteAddress is None:
            if self._type == "firefox" or self._type == "ff":
                dr = webdriver.Firefox()
            elif self._type == "chrome" or self._type == "Chrome":
                dr = webdriver.Chrome()
            elif self._type == "internet explorer" or self._type == "ie":
                dr = webdriver.Ie()
            elif self._type == "opera":
                dr = webdriver.Opera()
            elif self._type == "phantomjs":
                dr = webdriver.PhantomJS()
            elif self._type == "edge":
                dr = webdriver.Edge()
        else:
            if self._type == "RChrome":
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif self._type == "RIE":
                dc['browserName'] = 'internet explorer'
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
            elif self._type == "RFirefox":
                dc['browserName'] = 'firefox'
                dc['marionette'] = False
                dr = webdriver.Remote(command_executor='http://' + remoteAddress + '/wd/hub',
                                      desired_capabilities=dc)
        self.driver = dr

    def get(self, url, maximize_window=True, implicitly_wait=30):
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self

    @property
    def current_window(self):
        return self.driver.current_window_handle

    @property
    def title(self):
        return self.driver.title

    @property
    def current_url(self):
        return self.driver.current_url

    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_dir = screenshot_path + '\screenshot_%s' % day
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(screenshot_path + '\\%s_%s.png' % (name, tm))
        return screenshot

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def F5(self):
        self.driver.refresh()


if __name__ == '__main__':
    b = Browser('33').get('http://www.baidu.com')
    b.save_screen_shot('test_baidu')
    time.sleep(3)
    b.quit()
