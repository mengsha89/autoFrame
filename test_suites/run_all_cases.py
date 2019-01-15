# coding=utf-8
# author:ss


# run_all_case

import unittest
import os
from utils.HTMLTestRunner import HTMLTestRunner
import time
from utils.simple_report import report_content


# 测试用例存放路径
test_dir = r"..\cases\multi_scenario_interface"
# test_dir = r"..\cases\test"
# 匹配规则
rule = 'test*.py'
discover = unittest.defaultTestLoader.discover(test_dir, rule)

# 获取测试报告：'report.html'路径
report_name = 'report_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.html'
filename = os.path.join('..\\', 'reports', report_name)
print filename

# 生成HTML格式的报告
fp = open(filename, 'wb')
runner = HTMLTestRunner(fp,
                        title='自动化测试报告',    # 报告标题
                        description='用例执行情况如下：',     # 报告的描述
                        verbosity=2,    # 将注释在测试用例中展示
                        )
runner.run(discover)
fp.close()
# 生成邮件报告内容
report_content(report_name)

report = os.path.join('..\\', 'reports', 'report.html')
f = open(report, "rb")
mail_body = f.read()
f.close()

# se = SendEmail()
#
# msg = se.create_email(u"莎莎", u"测试", u"【双师接口自动化测试报告】_自动发送，请勿回复", html=mail_body, attach_addr=filename, attach_name=report_name)
# se.send_email("961100678@qq.com", "znpcefmizdvsbahf", msg,
#               ["dongshasha@gaosiedu.com", "majingna@gaosiedu.com", "qiyajing@gaosiedu.com",
#                "wangshanshan@gaosiedu.com", "liyuan0@gaosiedu.com", "panguoqing@gaosiedu.com",
#                "outao@gaosiedu.com", "jiangzushuai@gaosiedu.com"])