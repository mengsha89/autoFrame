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
