# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json


# 主讲老师登录
class TestLogin(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_login(self):
        url = base_url + "/surrogates/user/passwordLogin"
        api = BaseApi(url)
        req = api.send_request("post", data=web_login)
        print json.dumps(req).decode("unicode-escape")

