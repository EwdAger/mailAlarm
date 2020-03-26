# coding=utf-8
"""
Created on 2020/3/25 17:11

@author: EwdAger
"""
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time as ptime

from apscheduler.schedulers.blocking import BlockingScheduler

from mail_pigeon.parse_html import format_html, format_body
from mail_pigeon.settings import members, sender, getter, job_defaults, executors, jobstores
from crawler.daily_spider import DailySpider


class Pigeon:
    def __init__(self):
        self.scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.spider = DailySpider()

    def add_jobs(self):
        self.scheduler.add_job(self.tell_alive, trigger='cron', minute="*/5")

        self.scheduler.add_job(self.check_update, trigger='cron', args=[0], day_of_week='mon-fri', hour=17, minute=30)
        self.scheduler.add_job(self.check_update, trigger='cron', args=[1], day_of_week='mon-fri', hour=17, minute=45)
        self.scheduler.add_job(self.check_update, trigger='cron', args=[2], day_of_week='mon-fri', hour=18, minute=00)
        self.scheduler.add_job(self.check_update, trigger='cron', args=[3], day_of_week='mon-fri', hour=18, minute=15)
        self.scheduler.add_job(self.check_update, trigger='cron', args=[4], day_of_week='mon-fri', hour=18, minute=30)

        self.scheduler.add_job(self.send_daily, trigger='cron', hour=19, minute=00)
        print(f"添加任务成功! -- {datetime.now().strftime('%Y-%m-%d %H:%M')} --")

    def check_update(self, time):
        user_dict = self.spider.do_crawl(only_check_update=True)
        for name, is_update in user_dict.items():
            if not is_update:
                print(f"{name} 还没有写日报，已提醒{time + 1}次")
                self._send_alert(time, name)
                ptime.sleep(1)

    @staticmethod
    def tell_alive():
        print(f"I'm alive!!! Time is: -- {datetime.now().strftime('%Y-%m-%d %H:%M')} --")

    @staticmethod
    def _send_alert(time, user):
        word_dict = {
            0: "还",
            1: "又",
            2: "双",
            3: "叒",
            4: "叕"
        }

        mail_msg = '你今天'
        ceil = (time*100) + 1
        for i in range(ceil):
            mail_msg += word_dict[time]
        mail_msg += "没有写日报哦~ \n\n若一直没写日报，本条信息将从17:30至19:00每间隔15min，提醒一次~\n\n若至19:00还未写日报，将留空您今天的日报"

        ret = True
        try:
            msg = MIMEText(mail_msg, 'plain', 'utf-8')
            msg['From'] = sender['email']
            msg['To'] = formataddr((user, getter['user'][user]))
            msg['Subject'] = "你今天{}没有写日报哦~".format(word_dict[time])
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            server.login(sender['email'], sender['password'])
            server.sendmail(sender['email'], [getter['user'][user], ], msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            ret = False
        return ret

    def start(self):
        self.scheduler.start()

    @staticmethod
    def parse(daily_dict):
        date_now = datetime.now().strftime("%Y-%m-%d %H:%S")
        str_members = ", ".join(members)
        body = format_body(daily_dict)

        html = format_html(date_now, str_members, body)
        return html

    def send_daily(self):
        daily_dict = self.spider.do_crawl()

        all_none = True
        for daily in daily_dict.values():
            if daily:
                all_none = False
        if all_none:
            print("今天大家都没有写日报，应该是节假日")
            return False

        mail_msg = self.parse(daily_dict)

        ret = True
        try:
            email_list = [i for i in getter['user'].values()]

            msg = MIMEText(mail_msg, 'html', 'utf-8')
            msg['From'] = formataddr(("宁文杰", sender['email']))
            msg['To'] = ', '.join(email_list)
            msg['Cc'] = ', '.join(getter['copy'])
            msg['Subject'] = "数据智能组日报{}".format(datetime.now().strftime("%Y/%m/%d"))

            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            server.login(sender['email'], sender['password'])
            server.sendmail(sender['email'], email_list+getter['copy'], msg.as_string())
            server.quit()
            print(f'{datetime.now().strftime("%Y/%m/%d")} 日报发送成功！')
        except Exception as e:
            print(e)
            ret = False
        return ret


if __name__ == "__main__":
    p = Pigeon()
    p.send_daily()
