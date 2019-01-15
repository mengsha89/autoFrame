# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json


# 抢红包
class TestSnatch(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_snatch(self, user_id, red_id, stu_id):
        url = datiqi_url + "/terminator/api/redenvelope/snatch.do"
        api = BaseApi(url)
        data = {
            "reId": red_id,
            "stuId": stu_id,
            "userId": user_id
        }
        req = api.send_request("get", data=data)