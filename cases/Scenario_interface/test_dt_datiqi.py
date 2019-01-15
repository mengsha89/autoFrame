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
import sys


class TestDtDatiqi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 主讲老师进入直播课
        login()
        enter_live()
        cls.main_class_id, cls.lesson_id, cls.master_teacher_id, cls.master_user_id, cls.class_name = get_class_lesson()
        # 接口测试无需获取实际的key
        key = "1be9b4ef-3695-4324-86ab-90127f827e52"
        # 辅导老师扫码登录，进入直播课
        # key = get_key()
        cls.sub_class_id = class_list(cls.class_name)
        ass_login(cls.sub_class_id, cls.lesson_id, cls.master_teacher_id, key)
        cls.stus, cls.stus_dict = get_students(key)
        print cls.stus_dict
        stu_ids = ",".join(cls.stus)
        cls.stu_nums = len(cls.stus)
        sign(cls.lesson_id, cls.main_class_id, cls.sub_class_id, cls.stu_nums, stu_ids)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def answer_question(self, type_= 0):
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
        print "题目是：%s" % self.sub_class_id
        top_stus_ids = []
        stu_ans = {}

        for i in range(sign_num):
            answer = random.choice(["A", "B", "C", "D"])
            stu_id = self.stus[i]
            if answer == correct_answer:
                top_stus_ids.append(stu_id)
            stu_ans[stu_id] = answer
            print "%s的回答是%s" % (stu_id, answer)
            save_answer_rides(correct_answer, self.main_class_id, self.lesson_id, self.sub_class_id, stu_id, answer, score, topic_id,
                                  topic_sub_id, topic_no, topic_sub_no, type_=0, answer_type=1)
            key_record(correct_answer, self.sub_class_id, self.lesson_id, topic_id, topic_sub_id, 1, stu_id, answer)
            time.sleep(1)
        Logger().info("学生回答为：%s" % stu_ans)
        time.sleep(1)
        req = save_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                       type_=0, answer_type=1)
        return_current_question(self.main_class_id, self.lesson_id)
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
        self.assertEqual(stus_top, top_stus_ids, u"答题结果与实际答题情况不符")

    def snatch_red_envelope(self):
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

        changci = hand_out()
        print u"红包场次为:%s" % changci
        bus_id1 = "lessonId:%s" % self.lesson_id
        bus_id2 = "lessonId:%s_changci:%s" % (self.lesson_id, changci)
        update_status_and_vali(1, 12, bus_id1, bus_id2)

        # 抢红包
        red_infos, red_num = query_red_envelope_info(user_id)
        red_rew_li = {}
        for i in range(red_num):
            stu_red = int(random.choice(self.stus))
            print stu_red
            time.sleep(1)
            red_id = red_infos[i]["id"]
            red_rew = red_infos[i]["rewardNumber"]
            status = snatch_red_enve(user_id, red_id, stu_red)
            if status == 1:
                if stu_red in red_rew_li:
                    red_rew_li[stu_red] += red_rew
                else:
                    red_rew_li[stu_red] = red_rew

        # 主讲端正常结束抢红包，并获取抢红包队列
        redenvelope_end()
        reward_li = top_main_class(sign_num)
        update_status_and_vali(12, 13, bus_id2, bus_id2)
        return_index(self.main_class_id, self.lesson_id)
        update_status_and_vali(13, 1, bus_id2, bus_id1)
        # 当前仅一个小班
        result = {}
        for i in reward_li:
            stu_id = int(i["studentId"])
            stu_rew = i["rewardNumber"]
            result[stu_id] = stu_rew
        logger.info("抢红包排行榜为：%s" % result)
        self.assertEqual(red_rew_li, result, u"主讲端红包排行榜与实际抢红包情况不符")
        sub_rew_li = top_sub_class(sign_num, user_id)
        sub_rew = {}
        for j in sub_rew_li:
            stu_id = int(j["studentId"])
            stu_rew = j["rewardNumber"]
            sub_rew[stu_id] = stu_rew
        self.assertEqual(red_rew_li, sub_rew, u"听课端红包排行榜与实际抢红包情况不符")

    def pk_answer(self):
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
        start_answer(self.main_class_id, self.lesson_id, correct_answer, type_=0, answer_type=2)
        topic_id, topic_no, topic_sub_id, topic_sub_no = return_current_question(self.main_class_id, self.lesson_id)
        start_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                        type_=0, answer_type=2)

        bus_id1 = "lessonId:%s" % self.lesson_id
        bus_id2 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, topic_id, topic_sub_id)
        bus_id3 = "lessonId:%s_topicId:%s_topicSubId:%s" % (self.lesson_id, int(topic_id) + 1, topic_sub_id)
        update_status_and_vali(1, 22, bus_id1, bus_id2)
        get_main_answer_info(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        print "题目是：%s" % self.sub_class_id
        top_stus_ids = []
        stu_ans = {}

        for i in range(sign_num):
            answer = random.choice(["A", "B", "C", "D"])
            stu_id = self.stus[i]
            if answer == correct_answer:
                top_stus_ids.append(stu_id)
            stu_ans[stu_id] = answer
            print "%s的回答是%s" % (stu_id, answer)
            save_answer_rides(correct_answer, self.main_class_id, self.lesson_id, self.sub_class_id, stu_id, answer, score, topic_id,
                                  topic_sub_id, topic_no, topic_sub_no, type_=0, answer_type=2)
            key_record(correct_answer, self.sub_class_id, self.lesson_id, topic_id, topic_sub_id, 1, stu_id, answer)
            res = get_main_class_pk(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
            correct_rate = res.get("body").get("answerPKsmallVoList")[0].get("correctRate")
            corr_rate = round(float(len(top_stus_ids)) / float(i+1), 4)
            cor_rete = int(abs(correct_rate - corr_rate)*10000)
            print
            if cor_rete <= 1:
                logger.info("答题人数为：%d,答对人数为：%d,计算的正确率为：%.4f,实际为：%.4f" % (i+1, len(top_stus_ids), corr_rate, correct_rate))
            else:
                logger.error("答题人数为：%d,答对人数为：%d,计算的正确率为：%.4f,实际为：%.4f" % (i+1, len(top_stus_ids), corr_rate, correct_rate))
            self.assertLessEqual(round(abs(correct_rate-corr_rate), 4), 0.0001, "答题正确率与实际不符")
            time.sleep(1)

        req = save_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
                       type_=0, answer_type=2)

        update_status_and_vali(22, 23, bus_id3, bus_id3)
        res = get_main_pk_data(self.main_class_id, self.lesson_id, topic_id, topic_sub_id)
        correct_rate_end = res.get("body").get("answerPKsmallVoList")[0].get("correctRate")
        corr_rate_end = round(float(len(top_stus_ids))/float(self.stu_nums), 4)
        return_index(self.main_class_id, self.lesson_id)
        update_status_and_vali(23, 1, bus_id3, bus_id1)
        self.assertLessEqual(round(abs(correct_rate_end-corr_rate_end), 4), 0.0001, "答题正确率与实际不符")

    @staticmethod
    def getTestFunc():
        def func(self):
            self.answer_question()
            self.snatch_red_envelope()
            self.pk_answer()
        return func


def __generateTestCases():
    arg_lists = [(1,), (2,), (3,)]
    for args in arg_lists:
        setattr(TestDtDatiqi, "test_%s_%s" % (args[0], TestDtDatiqi.getTestFunc().__name__), TestDtDatiqi.getTestFunc())


# __generateTestCases()