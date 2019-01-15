# coding=utf-8
# author:ss

#
# from config import *
# import subprocess
#
# subprocess.Popen(exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


import unittest
import time
from macaca import WebDriver
from macaca import WebElement
from config import *

desired_caps = {
    'platformName': 'desktop',
    'browserName': 'electron',
    'app': exe_path
}

server_url = 'http://127.0.0.1:3456/wd/hub'


class MacacaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver(desired_caps, server_url)
        cls.driver.init()

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.quit()

    def test_get_url(self):
        self.driver.set_window_size(1280, 800)
        self.driver.get("https://www.baidu.com")


if __name__ == '__main__':
    unittest.main()