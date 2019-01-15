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



