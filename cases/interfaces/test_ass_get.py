# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json


# 获取学生列表
class TestGet(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_get(self, key):
        url = datiqi_url + "/terminator/api/dataDocking/get.do"
        api = BaseApi(url)
        data = {
            "key": key
        }
        req = api.send_request("get", data=data)
        print json.dumps(req).decode("unicode-escape")
        student_array = req.get("body").get("studentArray")
        stu_num = len(student_array)
        stus = []
        for i in range(stu_num):
            stus.append(str(student_array[i]["studentId"]))
        return stus