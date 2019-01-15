# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 主讲获取签到人数
class TestgetMainSign(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_class_begin(self, main_class_id, lesson_id):
        url = datiqi_url + "/terminator/api/sender/getMainSign"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id
        }
        req = api.send_request("get", data)
        sign_num = req.get("body").get("mainClassSign")
        print json.dumps(req).decode("unicode-escape")
        print "签到人数为：%d" % sign_num
        return sign_num

