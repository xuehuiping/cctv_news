# -*- coding: utf-8 -*-
# @Time   : 2023/2/16 上午11:28
# @Author : xuehuiping

'''
获取每日新闻联播内容
'''
import os
import requests
import schedule
from lxml import etree
import datetime
import time
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4651.0 Safari/537.36'
}
data_dir = 'cctv_news'


# 获取新闻
def get_hanlder(url):
    try:
        rsp = requests.get(url, headers=headers, timeout=5)
        rsp.raise_for_status()
        rsp.encoding = rsp.apparent_encoding
        return rsp.text
    except requests.RequestException as error:
        print(error)
        exit()


def get_news(url):
    rsp = get_hanlder(url)
    etr = etree.HTML(rsp)
    titles = etr.xpath("//li/a/text()")
    hrefs = etr.xpath("//li/a/@href")

    for title, href in zip(titles, hrefs):
        if '《新闻联播》' in title:
            # 获取新闻概要
            title_rsp = get_hanlder(href)

            data_tree = etree.HTML(title_rsp)
            summary = data_tree.xpath("//*[@class = \"video_brief\"]//text()")[0]
            return summary

    return ''


def run_one_day(strTime):
    tgt_file_name = os.path.join(data_dir, strTime + '.txt')
    if os.path.exists(tgt_file_name):
        return
    url = f'https://tv.cctv.com/lm/xwlb/day/{strTime}.shtml'
    news_text = get_news(url)
    with open(tgt_file_name, 'w')as f:
        f.write(news_text)


def run_some_day():
    for i in range(-30, -1):
        print(i)
        # 获取日期，处理是天，要更改为当天推送更改 -1 为 0
        strTime = (datetime.date.today() + datetime.timedelta(i)).strftime("%Y%m%d")
        print(strTime)
        run_one_day(strTime)
        time.sleep(3)


def run_many_day():
    dates = pd.date_range(end='20220803', periods=5, freq='D')
    for date in dates:
        strTime = date.strftime("%Y%m%d")
        print(strTime)
        run_one_day(strTime)
        time.sleep(5)

def run_yestoday():
    runDay = (datetime.date.today() + datetime.timedelta(-1)).strftime("%Y%m%d")
    run_one_day(runDay)

if __name__ == '__main__':
    run_yestoday()
