FROM python:3.6

RUN mkdir /mailAlarm

WORKDIR /mailAlarm

COPY . /mailAlarm

RUN pip install --upgrade pip -i https://pypi.douban.com/simple\
    && pip install -r requirements.txt -i https://pypi.douban.com/simple \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python", "-u", "/mailAlarm/run.py"]
