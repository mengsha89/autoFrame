# coding=utf-8
# author:ss

import unittest
from common.lecture import *
from common.assitant import *
import random
import subprocess
import config
from threading import Thread
import time
from utils.log import *
from ddt import ddt, data, unpack
from data import get


# 普通提问-随口提问
@ddt
class TestDtRedAskNorMouQues(unittest.TestCase):
    """
    发放3次红包后，发起普通提问
    """
    dt = get("red")

    @classmethod
    def setUpClass(cls):
        # subprocess.Popen(exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
        # TODO 签到仍需手工
        # sign(self.lesson_id, self.main_class_id, self.sub_class_id, 0, "657122")

    def setUp(self):
        pass

    def tearDown(self):
        config.top_stus_ids = []

    @classmethod
    def tearDownClass(cls):
        logout()

    @data(*dt)
    @unpack
    def test_001_snatch_red_envelope(self, i):
        """
        发放普通红包
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

        changci = hand_out()
        print u"红包场次为:%s" % changci
        bus_id1 = "lessonId:%s" % self.lesson_id
        bus_id2 = "lessonId:%s_changci:%s" % (self.lesson_id, changci)
        update_status_and_vali(1, 12, bus_id1, bus_id2)

        # 辅导老师端抢红包
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
        # reward_li = poll_all_snatch_dynamic()
        time.sleep(3)
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

    def test_002_answer_question(self, type_= 0):
        """
        普通提问流程
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
        print "题目是：%s" % self.sub_class_id
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
        req = save_answer(self.main_class_id, self.lesson_id, correct_answer, score, topic_id, topic_sub_id, topic_no, topic_sub_no,
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


if __name__ == '__main__':
    unittest.main()