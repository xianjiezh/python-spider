#!/usr/bin/python
# -*- coding: UTF-8 -*-


import requests
from bs4 import BeautifulSoup
import os
import time
import random

request_headers = {
    "Host": "www.tianqihoubao.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}

data_path = os.path.dirname(__file__)  # 获取当前python文件所在目录的完整路径
data_path = os.path.join(data_path, "tempdata")  # 获取的数据保存在temp目录中

if not os.path.exists(data_path):
    os.mkdir(data_path)  # 如果tempdata目录不存在，则创建该目录
ses = requests.Session()  # 创建Session进行请求，这样可以在后续爬取数据时传递cookie

ses.get("http://www.tianqihoubao.com/aqi/dongguang.html", headers=request_headers)



f = open(os.path.join(data_path, 'data.txt'), 'w', encoding='UTF-8', errors='ignore')  # 打开文件用于写入数据

f.write('日期      质量等级      AQI\n')

year = 2015
month = 1

year_str = ''
month_str = ''


while (year <= 2018 and month <= 12):
    year_str = str(year)
    if month < 10:
        month_str = '0' + str(month)
    else:
        month_str = str(month)
    
    url = 'http://www.tianqihoubao.com/aqi/dongguang-' + year_str + month_str +  '.html'
    print('url', url)
    r = ses.get(url)  # 通过Session对象请求网页数据，可以将前面获取的cookie传递给服务器
    month += 1
    if (month > 12):
        month = 1
        year += 1
    
    r.encoding = "gb2312"
    if r.status_code != 200:
        print("error code", r.status_code)


    bf = BeautifulSoup(r.text, features="html.parser")

    table = bf.table
    tr_items = table.find_all('tr')
    index = 0
    for item in tr_items:
        if index == 0: 
            pass
        else:
            date = item.select('td')[0].get_text(strip=True)
            quality = item.select('td')[1].get_text(strip=True)
            aqi = item.select('td')[2].get_text(strip=True)
            print(date + '   '+ quality + '     ' + aqi)
            f.write(date + '   '+ quality + '     ' + aqi + '\n')
        index += 1
    time.sleep(2.5 * random.random() + 2)


f.close()