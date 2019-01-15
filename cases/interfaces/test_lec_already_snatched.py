# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 已抢到红包的学生
class TestAlreadySnatched(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_already_snatched(self):
        url = datiqi_url + "/terminator/api/redenvelope/alreadySnatched"
        api = BaseApi(url, headers)
        req = api.send_request("get")
        print json.dumps(req).decode("unicode-escape")

