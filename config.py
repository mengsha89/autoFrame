# coding=utf-8
# author:ss

import os
import logging
error = True  # 调试信息打开或关闭
debug = True  # 调试信息打开或关闭
info = True  # 执行信息开关（主要用于log打印；）
env = "online"  # env表示脚本执行环境：test-测试，online-线上

# 控制台输出最低日志级别
clevel = logging.DEBUG
# 日志文件输出最低日志级别
flevel = logging.INFO
base_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
# 日志文件保存地址
log_file_dir = os.path.join(base_dir, "logs")
# 浏览器驱动目录
driver_path = os.path.join(base_dir, "drivers")
# 截图目录
screenshot_path = os.path.join(base_dir, "screenshot")

# 地址
base_url = "https://www.aixuexi.com"
datiqi_url = "http://datiqi.aixuexi.com"
ghost_url = "http://ghostrider.aixuexi.com"
bk_url = "https://ke.aixuexi.com"


# 主讲端请求头
headers = {
    "token": "6e32596f59ef50f7faf153f005e4cbf9,3sqq2,0"
}
# 听课端应用程序路径
path = ""

# 不同环境，参数不同
if env == "test":
    path = base_dir + r"apps\test\doubleteacher-win32-x64-1.1.1"

    # 主讲老师登录
    web_login = {
        "username": "15912348888",
        "password": "ss123456",
        "validate": ""
    }

    live_class_begin = {
        "mainClassId": "4657118",
        "lessonId": "1127333243",
        "lessonNo": "1",
        "meetingNo": "915201569320",
        "liveRoomCode": "lx2019",
        "tiddlerDeviceSN": "9Z278878C22556",
        "tiddlerDeviceNo": "60545830"
    }
    # 助教ID
    receive_teacher_id = 50808
    # 助教机构ID
    insId = "1591"
    user_id = "23077"


elif env == "online":
    path = base_dir + r"apps\online\doubleteacher-win32-x64-1.1.1"

    # 主讲老师登录
    web_login = {
        "username": "15912348888",
        "password": "ss123456",
        # "validate": ""
    }

    # live_class_begin = {
    #     "mainClassId": "4840057",
    #     "lessonId": "1127362672",
    #     "lessonNo": "1",
    #     "meetingNo": "915201569320",
    #     "liveRoomCode": "JS001",  # JS002 亚静直播间2
    #     "tiddlerDeviceSN": "102",
    #     "tiddlerDeviceNo": "102"
    # }

    live_class_begin = {
        "mainClassId": "4860385",
        "lessonId": "1127418868",
        "lessonNo": "1",
        "meetingNo": "915201569321",
        "liveRoomCode": "JS001",  # JS002 亚静直播间2
        "tiddlerDeviceSN": "101",
        "tiddlerDeviceNo": "101"
    }

    receive_teacher_id = 72375
    # 助教机构ID
    insId = "1591"
    master_teacher_id = 72374
    user_id = 1531039


exe_path = os.path.join(path, "doubleteacher.exe")
print exe_path
# 听课端应用日志文件路径
file_dir = os.path.join(path, "electron\logs")

# 答对学生列表
top_stus_ids = []


