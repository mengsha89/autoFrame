# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 正常结束发红包
class TestEnd(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_end(self):
        url = datiqi_url + "/terminator/api/redenvelope/end"
        api = BaseApi(url, headers)
        req = api.send_request("get")
        print json.dumps(req).decode("unicode-escape")

