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


# PK提问-习题练习题
class TestDtAskPkExecQues(unittest.TestCase):
    def setUp(self):
        # subprocess.Popen(exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
        self.stu_nums = len(self.stus)
        sign(self.lesson_id, self.main_class_id, self.sub_class_id, self.stu_nums, stu_ids)
        # TODO 签到仍需手工
        # sign(self.lesson_id, self.main_class_id, self.sub_class_id, 0, "657122")

    def tearDown(self):
        logout()

    def test_001_pk_answer(self):
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
            time.sleep(1)

        # 正确答案
        correct_answer = "A"
        score = random.randint(1, 5)
        delect_student_answer(self.main_class_id, self.lesson_id)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, type_=1, answer_type=2)
        topic_id, topic_no, topic_sub_id, topic_sub_no = return_current_question(self.main_class_id, self.lesson_id)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                        type_=1, answer_type=2)

        bus_id1 = "lessonId:%s" % self.lesson_id
        bus_id2 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, topic_id, topic_sub_id)
        bus_id3 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, int(topic_id) + 1, topic_sub_id)
        update_status_and_vali(1, 22, bus_id1, bus_id2)
        get_main_answer_info(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        stu_li = [657122, 657124, 775732, 775734, 783181]
        print "题目是：%s" % self.sub_class_id
        for i in range(sign_num):
            answer = random.choice(["A", "B", "C", "D"])
            print "%s的回答是%s" % (stu_li[i], answer)
            save_answer_rides(correct_answer, self.main_class_id, self.lesson_id, self.sub_class_id, stu_li[i], answer, score, topic_id,
                                  topic_sub_id, topic_no, topic_sub_no, type_=1, answer_type=2)
            key_record(correct_answer, self.sub_class_id, self.lesson_id, topic_id, topic_sub_id, 1, stu_li[i], answer)
            get_main_class_pk(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
            time.sleep(1)

        save_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                       type_=1, answer_type=2)
        update_status_and_vali(22, 23, bus_id3, bus_id3)
        get_main_pk_data(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        return_index(self.main_class_id, self.lesson_id)
        update_status_and_vali(23, 1, bus_id3, bus_id1)
