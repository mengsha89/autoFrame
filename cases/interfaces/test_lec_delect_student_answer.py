# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 清空此次答题数据
class TestDelectStudentAnswer(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_delect_student_answer(self, main_class_id, lesson_id, type_=0, topic_id=1, topic_sub_id=-1, send_out=0):

        url = datiqi_url + "/terminator/api/sender/delectStudentAnswer"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id,
            "type": type_,
            "topicId": topic_id,
            "topicSubId": topic_sub_id,
            "sendOut": send_out
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")

