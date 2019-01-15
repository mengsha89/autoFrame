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


# 抢红包
class TestSnatchOrdinaryRedEnve(unittest.TestCase):
    """
    提前停止抢红包
    """
    def setUp(self):
        # subprocess.Popen(exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # 主讲老师进入直播课
        login()
        enter_live()
        self.main_class_id, self.lesson_id, self.master_teacher_id, self.master_user_id, self.class_name = get_class_lesson()
        # 接口测试无需获取实际的key
        key = "8b20cef3-b529-41ac-9d8a-bccfaab50081"
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

    def test_snatch_red_envelope(self):
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
        time.sleep(10)

        # 辅导老师端抢红包

        red_infos, red_num = query_red_envelope_info(user_id)

        red_rew_li = {}
        # 发放5个红包后，提前结束红包发放
        for i in range(5):
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

        # 主讲端提前结束抢红包，并获取抢红包队列
        redenvelope_interrupt()
        # reward_li = poll_all_snatch_dynamic()
        reward_li = top_main_class(sign_num)
        update_status_and_vali(12, 13, bus_id2, bus_id2)
        time.sleep(10)
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

