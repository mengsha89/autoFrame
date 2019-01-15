# coding=utf-8
# author:ss

from core.base import BaseApi
import config 
import json

import re
import os
import sys
import time
from utils.log import *
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

log = Logger()


def get_key():
    today_date = datetime.now().strftime("%Y%m%d")
    # print today_date
    file_name = today_date + ".log"
    file_path = os.path.join(config.file_dir, file_name)
    ex = r"key=(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})"
    obj = None
    file_size = 0
    while not os.path.exists(file_path):
        time.sleep(3)
    while file_size == 0:
        file_size = os.path.getsize(file_path)
    # print file_size
    while obj is None:
        with open(file_path, "r") as f:
            lines = f.readlines()
            text = lines[-4:][0]
            # print text
        obj = re.search(ex, text)
        # print obj
    key = obj.group(1)
    print key
    return key


def class_list(class_name):
    url = config.ghost_url + "/ghostrider/api/class/list.do"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    api = BaseApi(url, headers)
    # TODO 辅导教师id是固定值，需动态获取
    data = {
        "teaId": config.receive_teacher_id,
        "insId": config.insId,
        "pageSize": 10,
        "pageNum": 1
    }
    req = api.send_request("post", data=data)
    print json.dumps(req).decode("unicode-escape")
    class_list = req.get("body").get("list")
    for i in range(len(class_list)):
        # TODO 当前className判断仅适用于该课程，通用需使用注释的代码
        # if u"高斯数学高二培优班" in class_list[i]["name"]:
        # print class_list[i]["name"], class_name
        if class_name in class_list[i]["name"]:
            sub_class_id = class_list[i]["id"]
            print "小班ID：%s" % sub_class_id
            return sub_class_id


def ass_login(sub_class_id, lession_no, master_teacher_id, key):
    """
    助教扫码登录
    :param sub_class_id:
    :param lession_no:
    :param master_teacher_id:
    :param key: 二维码值
    :return:
    """
    url = config.datiqi_url + "/terminator/api/dataDocking/put.do"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    api = BaseApi(url, headers)
    data_docking_vo = {
        "classId": sub_class_id,
        "insId": config.insId,
        "lessonNo": lession_no,
        "masterTeacherId": master_teacher_id,
        "receiveTeacherId": str(config.receive_teacher_id),
        "saveType": "flush",
        "wageId": key
    }
    data = {
        "key": key,
        "dataDockingVo": json.dumps(data_docking_vo)
    }

    print data
    req = api.send_request("post", data=data)
    print json.dumps(req).decode("unicode-escape")


def get_students(key):
    """
    获取学生列表
    :param key:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/dataDocking/get.do"
    api = BaseApi(url)
    data = {
        "key": key
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")
    stus_dict = {}
    stus = []
    try:
        student_array = req.get("body").get("studentArray")
        stu_num = len(student_array)
        for i in range(stu_num):
            stu = student_array[i]
            stu_id = str(stu["studentId"])
            stu_name = stu["studentName"]
            # print type(stu_name)
            stus_dict[stu_id] = stu_name
            stus.append(stu_id)
        log.info("学生列表为：%s" % str(stus_dict).replace(r"u\'",r"\'").decode("unicode-escape"))
    except Exception, e:
        print e
        log.error(e)
    return stus, stus_dict


def sign(lession_no, main_class_id, sub_class_id, stu_num, stu_ids):
    """
    开始上课统计签到总人数
    :param lession_no:
    :param main_class_id:
    :param sub_class_id:
    :param stu_num:
    :param stu_ids:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/sender/smallClassSign.do"
    api = BaseApi(url)
    # stu_ids = ",".join(stus)
    # print stu_ids
    data = {
        "baseStationSN": "2017110631",
        "frequencyPoint": 48,
        "lessonId": lession_no,
        "mainClassId": main_class_id,
        "sign": stu_num,  # stu_num
        "signStuIds": stu_ids,
        "signedSpareNumber": 0,
        "smallClassId": sub_class_id
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")

# ---------------------------抢红包相关接口-----------------------------------------------


def vali_tingke_ter_status(user_id, lesson_id):
    """
    异常处理
    :param user_id:
    :param lesson_id:
    :return:
    """
    url = config.datiqi_url + "exception/valiTingkeTerStatus.do"
    api = BaseApi(url)
    data = {
        "userId": user_id,
        "currentStatus": 1,
        "currentBusinessId": "lessonId:%s" % lesson_id
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")


def query_red_envelope_info(user_id):
    """
    获取红包信息
    :param user_id:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/redenvelope/queryRedEnvelopeInfo.do"
    api = BaseApi(url)
    data = {
        "userId": user_id
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")
    red_enevs = req.get("body")
    red_num = len(red_enevs)
    red_infos = []
    for i in range(red_num):
        red_info = {}
        red_info["id"] = red_enevs[i]["id"]
        red_info["rewardNumber"] = int(red_enevs[i]["rewardNumber"])
        red_infos.append(red_info)
    return red_infos, red_num


def snatch_red_enve(user_id, red_id, stu_id):
    """
    抢红包
    :param user_id:
    :param red_id:
    :param stu_id:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/redenvelope/snatch.do"
    api = BaseApi(url)
    data = {
        "reId": red_id,
        "stuId": stu_id,
        "userId": user_id
    }
    req = api.send_request("get", data=data)
    # print json.dumps(req).decode("unicode-escape")
    return req.get("status")


def top_sub_class(size, user_id):
    """
    获取抢红包排行榜
    :return:
    """
    url = config.datiqi_url + "/terminator/api/redenvelope/topSubClass.do"
    api = BaseApi(url)
    data = {
        "size": size,
        "userId": user_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    rew_li = req.get("body")
    return rew_li

# -------------------------------------答题相关接口--------------------------------------


def save_answer_rides(correct_answer, main_class_id, lesson_id, sub_class_id, stu_id, answer="A", score=0, topic_id=-1, topic_sub_id=-1, topic_no=-1, topic_sub_no=-1, topic_version=-1, sort=-1, type_=0, answer_type=2):
    """
    点击答题器提交答题记录
    :param correct_answer:
    :param main_class_id:
    :param lesson_id:
    :param sub_class_id:
    :param stu_id:
    :param answer:
    :param score:
    :param topic_id:
    :param topic_sub_id:
    :param topic_no:
    :param topic_sub_no:
    :param topic_version:
    :param sort:
    :param type_:
    :param answer_type:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/sender/saveAnswerRides.do"
    api = BaseApi(url)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "score": score,
        "topicId": topic_id,
        "topicSubId": topic_sub_id,
        "topicNo": topic_no,
        "topicSubNo": topic_sub_no,
        "topicVersion": topic_version,
        "sort": sort,
        "type": type_,
        "studentId": stu_id,
        "answer": answer,
        "smallClassId": sub_class_id,
        "isCorrect": 1 if correct_answer == answer else 0,
        "topNumber": 12,
        "redisKey": 1234567891234,
        "mainInstitution": 1,
        "startTime": 1,
        "endTime": 1,
        "region": 1,
        "answerTime": 1,
        "mTime": 123456
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    if answer == correct_answer:
        config.top_stus_ids.append(stu_id)


def key_record(correct_answer, small_class_id, lesson_id, topic_id=1, topic_sub_id=-1, answer_type=2, student_id=123456, student_answer="A"):
    """
    写入学生答题按钮的过程
    :param correct_answer:
    :param small_class_id:
    :param lesson_id:
    :param topic_id:
    :param topic_sub_id:
    :param answer_type:
    :param student_id:
    :param student_answer:
    :return:
    """
    url = config.datiqi_url + "/terminator/api/studentAnswerLog/keyRecord.do"
    api = BaseApi(url)
    data = {
        "smallClassId": small_class_id,
        "lessonId": lesson_id,
        "rightKey": correct_answer,
        "topicId": topic_id,
        "topicSubId": topic_sub_id,
        "answerType": answer_type,
        "studentKeyLogListJson": json.dumps([{
            "studentId": student_id,
            "studentAnswer": student_answer,
            "isCorrect": 1 if correct_answer == student_answer else 0
        }])

    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")