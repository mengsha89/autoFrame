# coding=utf-8
# author:ss

from pywinauto import application
from config import *
from common.assitant import *
import time

from selenium import webdriver
from pywinusb import hid
import serial

filter = hid.HidDeviceFilter()
all_devices = filter.get_devices()
for device in all_devices:
    if device.vendor_id == 0x04f3:
        print device  # vID=0x04f3, pID=0x0000, v=0x0005
        device.open()
        # device.set_raw_data_handler([hex(item).upper() for item in data[1:]])
        time.sleep(5)
        print device.find_input_reports()
        device.close()
# print all_devices
print len(all_devices)

import serial.tools.list_ports

plist = list(serial.tools.list_ports.comports())
print plist



# import pyautogui
#
# time.sleep(5)
#
# screenWidth, screenHeight = pyautogui.size()
# currentMouseX, currentMouseY = pyautogui.position()  # 1169 607
#
# print screenWidth, screenHeight, currentMouseX, currentMouseY



# driver = webdriver.Chrome()
# win_hans = driver.windows_handles
# print win_hans

# app = application.Application().start(exe_path)
#
# time.sleep(10)
# # 辅导老师扫码登录，进入直播课
# key = get_key()
# ass_login("4840058", "1127362672", "72374", key)
#
#
#
#
