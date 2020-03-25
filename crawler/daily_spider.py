# coding=utf-8
"""
Created on 2020/3/24 16:39

@author: EwdAger
"""
from datetime import datetime

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

from crawler.settings import login_dict, parse_dict

ua = UserAgent()


class DailySpider:

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({"user-agent": ua.random})
        self.is_login = False

    def login(self):
        self.session.post(login_dict['login_url'], data={
            "os_username": login_dict['username'],
            "os_password": login_dict['password'],
            "os_cookie": "true",
            "login": "登录"
        })
        self.is_login = True

    def do_crawl(self):
        if not self.is_login:
            self.login()

        daily_dict = {}
        for page_id, name in parse_dict['team_dict'].items():
            res = self.session.get(f"{parse_dict['daily_url']}?pageId={page_id}")
            daily_dict[name] = self._parse(res)

        return daily_dict

    def _parse(self, res):
        daily = ''
        soup = BeautifulSoup(res.text, 'html.parser')

        # 获取最后一条日报记录
        last_comment = soup.findAll("li", attrs={"class": "comment-thread"})[-1]
        # 获取编写时间
        update_time = last_comment.find('li', attrs={"class": "comment-date"})('a')[0].attrs['title']
        update_time = self._format_time(update_time)

        if update_time.date() < datetime.now().date():
            pass
        else:
            # 只发更新过的日报
            contents = last_comment.findAll('tr')

            for content in contents:
                daily += content.text + '<br>'

        return daily

    @staticmethod
    def _format_time(date):
        digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}

        if date[0] == '十' and date[2] == '月':
            to_digit = str(digit[date[0:2]]) + date[3:]
        else:
            to_digit = str(digit[date[0]]) + date[2:]
        return datetime.strptime(to_digit, '%m %d, %Y %H:%S')


if __name__ == "__main__":
    a = DailySpider()
    daily = a.do_crawl()
    from mail_pigeon.pigeon import send_daily
    send_daily(daily)
