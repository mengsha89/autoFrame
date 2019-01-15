# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获取PK答题的班级数据
class TestGetMainClassPK(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_get_main_class_pk(self, main_class_id, lesson_id, topic_id, topic_sub_id):
        url = datiqi_url + "/terminator/api/answerPK/getMainClassPK"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id,
            "topicId": topic_id,
            "topicSubId": topic_sub_id
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")

