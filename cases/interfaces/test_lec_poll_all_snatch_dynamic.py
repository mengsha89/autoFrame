# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 发放红包
class TestPollAllSnatchDynamic(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_poll_all_snatch_dynamic(self):
        url = datiqi_url + "/terminator/api/redenvelope/pollAllSnatchDynamic"
        api = BaseApi(url, headers)
        req = api.send_request("get")
        print json.dumps(req).decode("unicode-escape")
        rew_li = req.get("body")
        return rew_li

