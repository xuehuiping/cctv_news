# -*- coding: utf-8 -*-
# @Time   : 2023/2/16 下午4:10
# @Author : xuehuiping

import os
from flask import Flask
from flask import render_template, send_file
from flask import request
from flask_bootstrap import Bootstrap
import pandas as pd
import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
bootstrap = Bootstrap(app)

data_dir = './cctv_news/'

from x3 import run_one_day


@app.route('/')
def index():
    # runDay = datetime.datetime.now().strftime("%Y%m%d")
    runDay = (datetime.date.today() + datetime.timedelta(-1)).strftime("%Y%m%d")
    file_name = os.path.join(data_dir, runDay) + '.txt'
    if not os.path.exists(file_name):
        run_one_day(runDay)
    lines = open(file_name, encoding='utf-8').readlines()
    text = '《新闻联播》' + runDay + '<br>'
    for line in lines:
        text = text + line
        text = text + '<br>'
    return text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
