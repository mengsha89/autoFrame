# coding=utf-8
# author:ss


from selenium import webdriver
from config import *
import os
from common.assitant import *
import time


options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.binary_location = exe_path
options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument(
#     "user-agent:5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#     "doubleteacher/1.0.9.1 Chrome/56.0.2924.87 Electron/1.6.10 Safari/537.36")
# options.add_experimental_option("useAutomationExtension", False)
# desired_caps = options.to_capabilities()
desired_caps = {
    "browserName": "electron",
    'platformName': 'desktop',
    "binary": exe_path
}
# options.add_experimental_option("")
# desired_caps.update(caps)
# print desired_caps
chromedriver_path = os.path.join(driver_path, "chromedriver_2.42.exe")

driver = webdriver.Chrome(options=options, desired_capabilities=desired_caps)
# time.sleep(5)
# sound_confirm_btn = '/html/body/div[4]/div/div[3]/button[2]'
# students_list = '/html/body/div[1]/div[2]/div[2]/div'
# browser.find_element_by_xpath(sound_confirm_btn).click()
# time.sleep(10)
# # 辅导老师扫码登录，进入直播课
# key = get_key()
# sub_class_id = class_list(u"高思数学初一思维突破")
# ass_login(sub_class_id, "1127418868", 72374, key)
#
#
# stus = browser.find_element_by_xpath(students_list)
# for i in range(len(stus)):
#     stu_xpath = students_list + "[%d]" % i
#     stu_id = browser.find_element_by_xpath(stu_xpath).get_attribute("id")
#     js = 'var q=document.getElementById(%s);q.setAttribute("model", "true");' % stu_id
#     js_change_color = 'var q=document.getElementById(%s).children[0];q.setAttribute("class", "yellow");' % stu_id
#     browser.execute_script(js)
#     browser.execute_script(js_change_color)

executor_url = driver.command_executor._url
session_id = driver.session_id
driver.get("http://www.spiderpy.cn/")

print(session_id)
print(executor_url)