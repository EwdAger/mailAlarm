# coding=utf-8
"""
Created on 2020/3/25 17:11

@author: EwdAger
"""
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from mail_pigeon.parse_html import format_html, format_body
from mail_pigeon.settings import members, sender, getter


def parse(daily_dict):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%S")
    str_members = ", ".join(members)
    body = format_body(daily_dict)

    html = format_html(date_now, str_members, body)
    return html


def send_daily(daily_dict):
    mail_msg = parse(daily_dict)

    ret = True
    try:
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = sender['email']
        # msg['To'] = ', '.join(getter['user'])
        msg['To'] = "413657833@qq.com"
        msg['Subject'] = "数据智能组日报{}".format(datetime.now().strftime("%Y/%m/%d"))

        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.login(sender['email'], sender['password'])
        server.sendmail(sender['email'], ['413657833@qq.com', ], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
        ret = False
    return ret