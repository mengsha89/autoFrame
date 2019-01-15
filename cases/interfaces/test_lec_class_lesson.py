# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获取班级列表、讲次列表
class TestClassLesson(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_class_lesson(self):
        url = datiqi_url + "/terminator/api/base/classLesson"
        api = BaseApi(url, headers)
        req = api.send_request("get")
        print json.dumps(req).decode("unicode-escape")
        class_list = req.get("body")
        class_lists = {}
        lesson_lists = []
        for i in range(len(class_list)):
            class_li = class_list[i]
            class_id = class_li["classId"]
            lesson_list = class_li.get("lessonList")
            for j in range(len(lesson_list)):
                lesson_id = lesson_list[j]["lessonId"]
                lesson_lists.append(lesson_id)
            class_lists[class_id] = lesson_lists
        print class_lists

