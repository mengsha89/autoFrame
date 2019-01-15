# coding=utf-8
# author:ss

from core.base import BaseApi
from config import *
import json
from cap import *


def get_validate():
    url = "https://www.aixuexi.com/"
    cs = CrackSlider(url)
    validate = ""
    try:
        count = 6  # 最多识别6次
        cs.open()
        while count > 0:
            target = 'target.jpg'
            template = 'template.png'
            cs.get_pic()
            distance = cs.match(target, template)
            tracks = cs.get_tracks((distance + 7) * cs.zoom)  # 对位移的缩放计算
            cs.main_check_code(tracks)
            time.sleep(2)
            try:
                success_element = cs.driver.find_element_by_xpath('//*[@id="captcha"]/input[@name="NECaptchaValidate"]')
                validate = success_element.get_attribute("value")
                if validate:
                    print('成功识别！！！！！！')
                    count = 0
                    break
            except NoSuchElementException as e:
                print('识别错误，继续')
                count -= 1
                time.sleep(2)
        else:
            print('too many attempt check code ')
            exit('退出程序')
    finally:
        print validate
        return validate


def login():
    """
    主讲老师登录
    :return:
    """
    url = base_url + "/surrogates/user/passwordLogin"
    api = BaseApi(url)
    login_json = web_login.copy()
    try:
        # if env == "online":
        #     login_json["validate"] = get_validate()
        #     print "++++++++++++++++++++%s" % login_json
        req = api.send_request("post", data=login_json)
        print login_json
        token = req.get("body").get("token")
        headers["token"] = token
        # print req
        # return token
    except Exception, e:
        print e.message


def logout():
    """
    退出登录
    :return:
    """
    url = base_url + "/logout"
    api = BaseApi(url)
    api.send_request("get")


def class_lesson():
    """
    获取班级列表、讲次列表
    :return:
    """
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


def enter_live():
    """
    主讲开始上课
    :return:
    """
    url = datiqi_url + "/terminator/api/dataDocking/classesBegin"
    api = BaseApi(url, headers)
    req = api.send_request("get", data=live_class_begin)
    print json.dumps(req).decode("unicode-escape")


def get_main_sign(main_class_id, lesson_id):
    """
    获取签到人数
    :param main_class_id: 大班ID
    :param lesson_id: 讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/sender/getMainSign"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    sign_num = req.get("body").get("mainClassSign")
    print json.dumps(req).decode("unicode-escape")
    # print "签到人数为：%d" % sign_num
    return sign_num


def get_class_lesson():
    """
    获得当前班级讲次
    :return:
    """
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


def return_index(main_class_id, lesson_id):
    """
    返回答题页面
    :param main_class_id: 大班ID
    :param lesson_id: 讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/recipient/returnIndex.do"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def start_class_problem(main_class_id, lesson_id):
    """
    下课调研-开始提问
    :param main_class_id:大班ID
    :param lesson_id:讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/studentSurveySoket/startClassProblem"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def revoke_class_problem(main_class_id, lesson_id):
    """
    下课调研-撤销提问
    :param main_class_id:大班ID
    :param lesson_id:讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/studentSurveySoket/revokeClassProblem"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def stat_class_problem(main_class_id, lesson_id):
    """
    下课调研-统计答案
    :param main_class_id: 大班ID
    :param lesson_id: 讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/studentSurvey/statisticsClassProblem"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def stop_class_problem(main_class_id, lesson_id):
    """
    下课调研-结束提问
    :param main_class_id:大班ID
    :param lesson_id:讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/studentSurveySoket/stopClassProblem"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def reset_status():
    url = datiqi_url + "/terminator/api/exception/resetStatus"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def keep_alive():
    """
    更新在线状态
    :return:
    """
    url = datiqi_url + "/terminator/api/online/keepAlive"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def update_status_and_vali(current_status, target_tatus, current_businessId, target_business_id):
    """
    验证以及更新状态
    :param current_status:
    :param target_tatus:
    :param current_businessId:
    :param target_business_id:
    :return:
    """
    url = datiqi_url + "/terminator/api/exception/updateStatusAndVali"
    api = BaseApi(url, headers)
    data = {
        "currentStatus": current_status,
        "targetStatus": target_tatus,
        "currentBusinessId": current_businessId,  # "lessonId:%s" % lesson_id
        "targetBusinessId": target_business_id  # "lessonId:%s_changci:%s" % (lesson_id, changci)
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")

# -------------------------------------发红包相关接口--------------------------------------


def get_red_type():
    """
    获取红包类型
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/getRedType"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    types = req.get("body")
    print json.dumps(types).decode("unicode-escape")
    return types


def hand_out(red_type="Red_Ordinary"):
    """
    发放红包
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/handout"
    api = BaseApi(url, headers)
    data = {
        "redType": red_type
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")
    changci = req.get("body").get("currentChangci")
    return changci


def poll_all_snatch_dynamic():
    """
    抢到红包的人数
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/pollAllSnatchDynamic"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")
    rew_li = req.get("body")
    return rew_li


def already_snatched():
    """
    已抢到红包的学生
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/alreadySnatched"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def redenvelope_end():
    """
    正常结束发红包
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/end"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def redenvelope_interrupt():
    """
    提前结束发红包
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/interrupt"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def redenvelope_revoke():
    """
    撤销发红包
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/revoke"
    api = BaseApi(url, headers)
    req = api.send_request("get")
    print json.dumps(req).decode("unicode-escape")


def top_main_class(size):
    """
    获取抢红包排行榜
    :return:
    """
    url = datiqi_url + "/terminator/api/redenvelope/topMainClass"
    api = BaseApi(url, headers)
    data = {
        "size": size
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    rew_li = req.get("body")
    return rew_li

# ---------------------------------------上课提问相关接口-------------------------------------------------


def start_answer(main_class_id, lesson_id, correct_answer="A", score=0, topic_id=-1, topic_sub_id=-1, topic_no=-1, topic_sub_no=-1, topic_version=-1, sort=-1, type_=0, answer_type=2):
    """
    开始提问
    :param main_class_id:
    :param lesson_id:
    :param correct_answer:正确答案
    :param score:金币数
    :param topic_id:
    :param topic_sub_id:
    :param topic_no: 例题1.3，topic_no为1，topic_sub_no为3
    :param topic_sub_no:
    :param topic_version:
    :param sort:问题序号
    :param type_:0-随口提问，1-例题，2-练习题
    :param answer_type:1-普通提问，2-pk提问
    :return:
    """
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


def save_answer(main_class_id, lesson_id, correct_answer="A", score=0, topic_id=1, topic_sub_id=-1, topic_no=-1, topic_sub_no=-1, topic_version=-1, sort=-1, type_=0, answer_type=2, stus_top=18):
    """
    结束答题 并 获取答题结果
    :param main_class_id:
    :param lesson_id:
    :param correct_answer:
    :param score:
    :param topic_id:
    :param topic_sub_id:
    :param topic_no:
    :param topic_sub_no:
    :param topic_version:
    :param sort:
    :param type_:
    :param answer_type:
    :param stus_top:
    :return:
    """
    url = datiqi_url + "/terminator/api/recipient/saveAnswer"
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
        "answerType": answer_type,
        "studentTop": stus_top
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    return req


def topic_list(main_class_id, lesson_id):
    """
    获取 例题 和 练习题 列表
    :param main_class_id:大班ID
    :param lesson_id:讲次ID
    :return:
    """
    url = datiqi_url + "/terminator/api/topic/topicList.do"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def delect_student_answer(main_class_id, lesson_id, type_=0, topic_id=1, topic_sub_id=-1, send_out=0):
    """
    清空此次答题数据
    :param main_class_id:
    :param lesson_id:
    :param type_:
    :param topic_id:
    :param topic_sub_id:
    :param send_out:
    :return:
    """
    url = datiqi_url + "/terminator/api/sender/delectStudentAnswer"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "type": type_,
        "topicId": topic_id,
        "topicSubId": topic_sub_id,
        "sendOut": send_out
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def return_current_question(main_class_id, lesson_id):
    """
    异常时，跳转到正在答题页面所需要的参数数据
    :param main_class_id:
    :param lesson_id:
    :return:
    """
    url = datiqi_url + "/terminator/api/recipient/returnCurrentQuestion"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id
    }
    req = api.send_request("get", data)
    # print json.dumps(req).decode("unicode-escape")
    topic_id = req.get("body").get("topicId")
    topic_no = req.get("body").get("topicNo")
    topic_sub_id = req.get("body").get("topicSubId")
    topic_sub_no = req.get("body").get("topicSubNo")
    print"当前topicId：%s" % topic_id
    return topic_id, topic_no, topic_sub_id, topic_sub_no


def get_settlement(main_class_id, lesson_id, topic_id=1, topic_sub_id=-1, student_top=18, correct_answer="A"):
    """
    获取答题结束后的数据
    :param main_class_id:
    :param lesson_id:
    :param topic_id:
    :param topic_sub_id:
    :param student_top:
    :param correct_answer:
    :return:
    """
    url = datiqi_url + "/terminator/api/recipient/getSettlement"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "topicId": topic_id,
        "topicSubId": topic_sub_id,
        "studentTop": student_top,
        "correctAnswer": correct_answer
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    return req


def get_main_answer_info( main_class_id, lesson_id, topic_id, topic_sub_id):
    """
    主动获取正在答题的数据
    :param main_class_id:
    :param lesson_id:
    :param topic_id:
    :param topic_sub_id:
    :return:
    """
    url = datiqi_url + "/terminator/api/sender/getMainAnswerInformation"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "topicId": topic_id,
        "topicSubId": topic_sub_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def get_main_class_pk(main_class_id, lesson_id, topic_id, topic_sub_id):
    """
    获取PK答题的班级数据
    :param main_class_id:
    :param lesson_id:
    :param topic_id:
    :param topic_sub_id:
    :return:
    """
    url = datiqi_url + "/terminator/api/answerPK/getMainClassPK"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "topicId": topic_id,
        "topicSubId": topic_sub_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    return req


def get_main_pk_data(main_class_id, lesson_id, topic_id, topic_sub_id):
    """
    获取PK答题的数据
    :param main_class_id:
    :param lesson_id:
    :param topic_id:
    :param topic_sub_id:
    :return:
    """
    url = datiqi_url + "/terminator/api/answerPK/getMainPKData"
    api = BaseApi(url, headers)
    data = {
        "mainClassId": main_class_id,
        "lessonId": lesson_id,
        "topicId": topic_id,
        "topicSubId": topic_sub_id
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")
    return req


# ---------------------------------------授课页例题改造提问相关接口-------------------------------------------------


def start_answer_do(main_class_id, lesson_id, correct_answer="A", score=2, topic_id=533093, topic_sub_id=594422, topic_no=11, topic_sub_no=11, topic_version=27, sort=17, type_=1, answer_type=1):
    """
    开始提问
    :param main_class_id:
    :param lesson_id:
    :param correct_answer:正确答案
    :param score:金币数
    :param topic_id:
    :param topic_sub_id:
    :param topic_no: 例题1.3，topic_no为1，topic_sub_no为3
    :param topic_sub_no:
    :param topic_version:
    :param sort:问题序号
    :param type_:0-随口提问，1-例题，2-练习题
    :param answer_type:1-普通提问，2-pk提问
    :return:
    """
    url = bk_url + "/terminator/api/recipient/startAnswer.do"
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
        "answerType": answer_type,
        "institution": 2867
    }
    req = api.send_request("get", data)
    print json.dumps(req).decode("unicode-escape")


def update_status_and_vali_do(current_status, target_tatus, current_businessId, target_business_id):
    """
    验证以及更新状态
    :param current_status:
    :param target_tatus:
    :param current_businessId:
    :param target_business_id:
    :return:
    """
    url = bk_url + "/terminator/api/exception/updateStatusAndVali.do"
    api = BaseApi(url, headers)
    data = {
        "currentStatus": current_status,
        "targetStatus": target_tatus,
        "currentBusinessId": current_businessId,  # "lessonId:%s" % lesson_id
        "targetBusinessId": target_business_id  # "lessonId:%s_topicId:%s_topicSubId:%s" % (lesson_id, topic_id, topic_sub_id)
    }
    req = api.send_request("get", data=data)
    print json.dumps(req).decode("unicode-escape")


if __name__ == '__main__':
    # get_validate()
    login()
    logout()