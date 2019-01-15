# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获取抢红包排行榜
class TestTopMainClass(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_top_main_class(self):
        url = datiqi_url + "/terminator/api/redenvelope/topMainClass"
        api = BaseApi(url, headers)
        data = {
            "size": 7
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")

