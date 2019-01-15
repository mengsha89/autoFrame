# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json


# 获取红包信息
class TestQueryRedEnvelopeInfo(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_query_red_envelope_info(self, user_id):

        url = datiqi_url + "/terminator/api/redenvelope/queryRedEnvelopeInfo.do"
        api = BaseApi(url)
        data = {
            "userId": user_id
        }
        req = api.send_request("get", data=data)
        print json.dumps(req).decode("unicode-escape")
