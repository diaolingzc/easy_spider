# coding:utf-8
from email.mime.text import MIMEText
import smtplib

from SMTP.config import *


def build_mail():
    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR
    msg['Subject'] = '来自SMTP的问候。。。'
    return msg


def send_mail():
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
        server.set_debuglevel(1)
        server.login(FROM_ADDR, PASSWORD)
        server.sendmail(FROM_ADDR, [TO_ADDR], build_mail().as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print('发送邮箱失败', e.args)


if __name__ == '__main__':
    send_mail()