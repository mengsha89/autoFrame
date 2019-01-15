# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 下课调研-统计答案
class TestStatisticsClassProblem(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_statistics_class_problem(self, main_class_id, lesson_id):
        url = datiqi_url + "/terminator/api/studentSurvey/statisticsClassProblem"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")
