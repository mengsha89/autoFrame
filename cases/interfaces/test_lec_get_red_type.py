# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获取红包类型
class TestGetRedType(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_get_red_type(self):
        url = datiqi_url + "/terminator/api/redenvelope/getRedType"
        api = BaseApi(url, headers)
        req = api.send_request("get")
        types = req.get("body")
        print json.dumps(types).decode("unicode-escape")
        return types
