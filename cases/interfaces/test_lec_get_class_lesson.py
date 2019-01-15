# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 获得当前班级讲次
class TestGetClassLesson(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_get_class_lesson(self):
        url = datiqi_url + "/terminator/api/dataDocking/getClassLesson"
        api = BaseApi(url, headers)
        try:
            req = api.send_request("get")
            print json.dumps(req).decode("unicode-escape")
            main_class_id = req.get("body").get("mainClassId")
            lesson_id = req.get("body").get("lessonId")
            class_name = req.get("body").get("className")
            master_teacher = eval(req.get("body").get("teacherList"))
            master_teacher_id = master_teacher[0]["id"]
            master_user_id = master_teacher[0]["userId"]
            # print main_class_id, lesson_id, master_teacher_id, master_user_id, class_name
            return main_class_id, lesson_id, master_teacher_id, master_user_id, class_name
        except Exception, e:
            print e.message
