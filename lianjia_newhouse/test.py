# -- coding: utf-8 --
"""
    author:michael

    project:lianjia_newhouse

    date:2020/2/21

"""
from urllib import request
from bs4 import BeautifulSoup
import datetime


a = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print(a)
print(type(a))