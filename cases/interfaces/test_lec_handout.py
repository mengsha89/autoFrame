# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 发放红包
class TestHandout(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_handout(self):
        url = datiqi_url + "/terminator/api/redenvelope/handout"
        api = BaseApi(url, headers)
        data = {
            "redType": "Red_Ordinary"
        }
        req = api.send_request("get", data=data)
        print json.dumps(req).decode("unicode-escape")
        changci = req.get("body").get("currentChangci")
        return changci

