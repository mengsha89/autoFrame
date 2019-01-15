# coding=utf-8
# author:ss


# run_all_case

import unittest
import os
from utils.HTMLTestRunner import HTMLTestRunner
import time
from utils.simple_report import report_content


# 测试用例存放路径
test_dir = r"..\cases\test"
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
