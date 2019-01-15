# coding=utf-8
# author:ss


import unittest
from config import *
from core.base import *
from common.lecture import login
import json


# 开始提问
class TestStartAnswer(unittest.TestCase):
    def setUp(self):
        login()

    def tearDown(self):
        pass

    def test_001_start_answer(self, main_class_id, lesson_id, correct_answer="A", score=0, topic_id=-1, topic_sub_id=-1, topic_no=-1, topic_sub_no=-1, topic_version=-1, sort=-1, type_=0, answer_type=2):
        url = datiqi_url + "/terminator/api/recipient/startAnswer"
        api = BaseApi(url, headers)
        data = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id,
            "correctAnswer": correct_answer,
            "score": score,
            "topicId": topic_id,
            "topicSubId": topic_sub_id,
            "topicNo": topic_no,
            "topicSubNo": topic_sub_no,
            "topicVersion": topic_version,
            "sort": sort,
            "type": type_,
            "answerType": answer_type
        }
        req = api.send_request("get", data)
        print json.dumps(req).decode("unicode-escape")

