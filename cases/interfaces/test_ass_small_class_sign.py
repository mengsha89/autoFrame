# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
import json
from common.assitant import get_students, ass_login
from ddt import ddt, data, unpack
from data import get


# 开始上课统计签到总人数
@ddt
class TestSmallClassSign(unittest.TestCase):
    dt = get("small_sign")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*dt)
    @unpack
    def test_001_small_class_sign(self, lession_no, main_class_id, sub_class_id):
        ass_login(sub_class_id, lession_no, master_teacher_id, "da025b78-9833-4d72-a45a-45a3a5f2a600")
        stus = get_students("da025b78-9833-4d72-a45a-45a3a5f2a600")
        stu_ids = ",".join(stus)
        stu_num = len(stu_ids)
        url = datiqi_url + "/terminator/api/sender/smallClassSign.do"
        api = BaseApi(url)
        data = {
            "baseStationSN": "2017110631",
            "frequencyPoint": 48,
            "lessonId": lession_no,
            "mainClassId": main_class_id,
            "sign": stu_num,
            "signStuIds": stu_ids,
            "signedSpareNumber": 0,
            "smallClassId": sub_class_id
        }
        req = api.send_request("get", data=data)
        print json.dumps(req).decode("unicode-escape")
        sign_num = req.get("body").get("mainClassSign")
        self.assertGreater(sign_num, 0, u"签到失败")