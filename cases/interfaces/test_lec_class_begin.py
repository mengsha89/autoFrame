# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 主讲开始上课
class TestClassBegin(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_class_begin(self):
        url = datiqi_url + "/terminator/api/dataDocking/classesBegin"
        api = BaseApi(url, headers)
        req = api.send_request("get", data=live_class_begin)
        print json.dumps(req).decode("unicode-escape")

