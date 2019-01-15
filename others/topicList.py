# coding=utf-8
# author:ss


from core.base import BaseApi
import json
import unittest
from ddt import ddt, data, unpack
from data import get


@ddt
class Test1(unittest.TestCase):
    dt = get("topicList")

    @data(*dt)
    @unpack
    def test_topicList(self, main_class_id, lesson_id):
        url = "http://datiqi.aixuexi.com/terminator/api/topic/topicList.do"
        api = BaseApi(url)
        dd = {
            "mainClassId": main_class_id,
            "lessonId": lesson_id
        }
        req = api.send_request("get", dd)
        topic_list = req.get("body").get("topicList")
        print json.dumps(topic_list).decode("unicode-escape")
        if len(topic_list) == 0:
            with open("fail_data.txt", "a") as f:
                d = str(main_class_id)+","+str(lesson_id)
                f.write(d+"\n")
        self.assertNotEqual(len(topic_list), 0, str(main_class_id)+"----"+str(lesson_id))
