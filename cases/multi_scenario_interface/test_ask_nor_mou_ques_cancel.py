# coding=utf-8
# author:ss

import unittest
from common.lecture import *
from common.assitant import *
import random
import subprocess
from config import *
from threading import Thread
import time
from utils.log import *


# 普通提问-随口提问
class TestDtAskNorMouQuesCancel(unittest.TestCase):
    """
    发起普通随口提问，取消后，再次发起普通提问流程
    """
    def setUp(self):
        # 主讲老师进入直播课
        login()
        enter_live()
        self.main_class_id, self.lesson_id, self.master_teacher_id, self.master_user_id, self.class_name = get_class_lesson()
        # 接口测试无需获取实际的key
        key = "1be9b4ef-3695-4324-86ab-90127f827e52"
        # 辅导老师扫码登录，进入直播课
        # key = get_key()
        self.sub_class_id = class_list(self.class_name)
        ass_login(self.sub_class_id, self.lesson_id, self.master_teacher_id, key)
        self.stus, self.stus_dict = get_students(key)
        print self.stus_dict
        stu_ids = ",".join(self.stus)
        stu_nums = len(self.stus)
        sign(self.lesson_id, self.main_class_id, self.sub_class_id, stu_nums, stu_ids)

    def tearDown(self):
        config.top_stus_ids = []
        logout()

    def test_cancel_answer_question(self, type_= 0):
        """
        发起普通随口提问后取消，之后再次提问
        """
        def alive():
            while True:
                keep_alive()
                time.sleep(10)

        t = Thread(target=alive)
        t.setDaemon(True)
        t.start()
        sign_num = 0
        while sign_num == 0:
            sign_num = get_main_sign(self.main_class_id, self.lesson_id)
            print "签到人数为：%s" % sign_num
            time.sleep(1)

        # 正确答案
        correct_answer = "A"
        score = random.randint(1, 5)
        delect_student_answer(self.main_class_id, self.lesson_id)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, type_=0, answer_type=1)
        topic_id, topic_no, topic_sub_id, topic_sub_no = return_current_question(self.main_class_id, self.lesson_id)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                        type_=0, answer_type=1)

        bus_id1 = "lessonId:%s" % self.lesson_id
        bus_id2 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, topic_id, topic_sub_id)
        bus_id3 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, int(topic_id) + 1, topic_sub_id)
        update_status_and_vali(1, 2, bus_id1, bus_id2)
        get_main_answer_info(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        print "第一次题目是：%s" % self.sub_class_id

        delect_student_answer(self.main_class_id, self.lesson_id, type_=0, topic_id=topic_id, topic_sub_id=topic_sub_id, send_out=1)
        update_status_and_vali(2, 1, bus_id2, bus_id1)

        print "结束答题后开始再一次答题"

        delect_student_answer(self.main_class_id, self.lesson_id, type_=0, topic_id=topic_id, topic_sub_id=topic_sub_id,
                              send_out=0)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no,
                     topic_sub_no,
                     type_=0, answer_type=1)
        update_status_and_vali(1, 2, bus_id1, bus_id2)
        get_main_answer_info(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        print "第二次题目是：%s" % self.sub_class_id
        threadpool = []
        stu_ans = {}
        for i in range(sign_num):
            answer = random.choice(["A", "B", "C", "D"])
            stu_id = self.stus[i]
            stu_ans[stu_id] = answer
            print "%s的回答是%s" % (stu_id, answer)
            ans_thread = Thread(target=save_answer_rides, args=(
            correct_answer, self.main_class_id, self.lesson_id, self.sub_class_id, stu_id, answer, score, topic_id,
            topic_sub_id, topic_no, topic_sub_no, -1, -1, 0, 1))
            # key_record(correct_answer, self.sub_class_id, self.lesson_id, topic_id, topic_sub_id, 1, stu_id, answer)
            threadpool.append(ans_thread)
        for th in threadpool:
            th.start()
            th.join()
        Logger().info("学生回答为：%s" % stu_ans)
        req = save_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no,
                          topic_sub_no,
                          type_=0, answer_type=1)
        return_current_question(self.main_class_id, self.lesson_id)
        # req = get_settlement(self.main_class_id, self.lesson_id, correct_answer=correct_answer)
        stu_top = json.dumps(req.get("body").get("studentName")).decode("unicode-escape")
        stus_top = []
        for stu in eval(stu_top):
            stu_name = stu.split("-")[1]
            for k, v in self.stus_dict.items():
                if v == stu_name:
                    stus_top.append(k)
        update_status_and_vali(2, 3, bus_id3, bus_id3)
        return_index(self.main_class_id, self.lesson_id)
        update_status_and_vali(3, 1, bus_id3, bus_id1)
        print "stu_top:%s" % stu_top
        self.assertEqual(sorted(stus_top), sorted(config.top_stus_ids), u"答题结果与实际答题情况不符")

