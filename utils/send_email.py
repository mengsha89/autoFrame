# coding=utf-8
# author:ss

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import traceback
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SendEmail(object):
    def create_email(self, email_from, email_to, subject, text="", html="", attach_addr="", attach_name=""):
        """

        :param email_from:
        :param email_to:
        :param subject:
        :param text:
        :param attach_addr:
        :param attach_name:
        :return:
        """
        # 生成一个空的带附件的邮件实例
        message = MIMEMultipart()
        # 正文以text形式插入邮件
        # email_text = MIMEText(text, 'plain', 'utf-8')
        email_html = MIMEText(html, "html", "utf-8")
        # message.attach(email_text)
        message.attach(email_html)
        # 发件人姓名
        email_sender = Header(email_from, "utf-8")
        message["From"] = email_sender
        # 收件人姓名
        email_receiver = Header(email_to, "utf-8")
        message["To"] = email_receiver
        # 邮件主题
        email_subject = Header(subject, "utf-8")
        message["Subject"] = email_subject
        if attach_addr != "":
            # 附件
            attach = open(attach_addr, 'rb').read()
            text_att = MIMEText(attach, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            text_att["Content-Disposition"] = 'attachment; filename=' + attach_name
            # 将附件内容插入邮件中
            message.attach(text_att)
        return message

    def send_email(self, sender, pwd, msg, receiver):
        try:
            server = smtplib.SMTP("smtp.qq.com")
            # server.starttls()
            server.login(sender, pwd)
            server.sendmail(sender, receiver, msg.as_string())
            print u"邮件发送成功"
            server.close()
        except Exception:
            print traceback.print_exc()
            print u"邮件发送失败"


if __name__ == '__main__':
    report_name = "report_2019-01-15_22-01-03.html"
    filename = os.path.join('..\\', 'reports', report_name)
    # # 生成邮件报告内容
    # report_content(report_name)

    report = os.path.join('..\\', 'reports', 'report.html')
    #
    # path_wk = r'D:\Python27\wkhtmltox\bin\wkhtmltopdf.exe'  # 安装位置
    # config = pdfkit.configuration(wkhtmltopdf=path_wk)
    # with open(report) as f:
    #     pdfkit.from_file(f, 'out.pdf')

    f = open(report, "rb")
    mail_body = f.read()
    f.close()

    se = SendEmail()

    msg = se.create_email(u"莎莎", u"测试", u"【双师接口自动化测试报告】--自动发送,请勿回复,详情见附件", html=mail_body, attach_addr=filename, attach_name=report_name)
    se.send_email("961100678@qq.com", "ympthterpkccbfeh", msg,
                  ["dongshasha@gaosiedu.com", "majingna@gaosiedu.com", "qiyajing@gaosiedu.com",
               "cuimeng@gaosiedu.com", "liyuan0@gaosiedu.com", "panguoqing@gaosiedu.com",
               "outao@gaosiedu.com", "jiangzushuai@gaosiedu.com"])


    # se = SendEmail()
    #
    # msg = se.create_email(u"莎莎", u"测试", u"【双师接口自动化测试报告】--自动发送,请勿回复,详情见附件", html=mail_body, attach_addr=filename, attach_name=report_name)
    # se.send_email("dongshasha@gaosiedu.com", "ss940308", msg,
    #               ["961100678@qq.com"])


    # print "" or [] or None
    # print [] and "" and {}
    # print "a" and " " and [""]
    # print "a" or " " or []