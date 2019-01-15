# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json


# 助教扫码登录
class TestPut(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_put(self, sub_class_id, lession_no, master_teacher_id, key):
        url = datiqi_url + "/terminator/api/dataDocking/put.do"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        api = BaseApi(url, headers)
        data_docking_vo = {
            "classId": sub_class_id,
            "insId": "1591",
            "lessonNo": lession_no,
            "masterTeacherId": master_teacher_id,
            "receiveTeacherId": "50808",
            "saveType": "flush",
            "wageId": key
        }
        data = {
            "key": key,
            "dataDockingVo": json.dumps(data_docking_vo)
        }

        print data
        req = api.send_request("post", data=data)
        print json.dumps(req).decode("unicode-escape")
