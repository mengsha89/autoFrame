# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获取答题结束后的数据
class TestGetSettlement(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_get_settlement(self, main_class_id, lesson_id, topic_id=1, topic_sub_id=-1, student_top=18, correct_answer="A"):
        url = datiqi_url + "/terminator/api/recipient/getSettlement"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id,
            "topicId": topic_id,
            "topicSubId": topic_sub_id,
            "studentTop": student_top,
            "correctAnswer": correct_answer
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")
        return req
