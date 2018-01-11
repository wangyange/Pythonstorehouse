#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import csv
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

url_1 ='https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time='
url_2 ='&max_behot_time_tmp=1515628836&tadrequire=true&as=A1C5BAB5060C1C3&cp=5A564CA1BC439E1&_signature=V3WKwwAADSSrDGC.nr9T-1d1it'

headers={
    'Cookie':'uuid="w:18845548685742289937f6c8dd6d86b2"; UM_distinctid=160dec004e48a-02b7095a7057bf-454f032b-1fa400-160dec004e57f4; tt_webid=6509304748125373966; _ga=GA1.2.1127840692.1515565615; _gid=GA1.2.750937425.1515565615; tt_webid=6509304748125373966; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=pw9si34s81515635133770; CNZZDATA1259612802=622648049-1515562235-null%7C1515632472',
'Host':'www.toutiao.com',
'Referer':'https://www.toutiao.com/ch/news_sports/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
max_behot_time =[1515628836]
print type(max_behot_time)
def get_toutiao(max_behot_time):
    global toutiao
    url =url_1+str(max_behot_time)+url_2
    req= requests.get(url=url,headers=headers)
    html =req.json()
    toutiao=[]
    time_temp.append(html['next']['max_behot_time'])
    for data in html['data']:
        toutiao.append([data['title'],data['abstract'],data['source']])
        # toutiao.append(data['abstract'])
        # toutiao.append(data['source'])
    return toutiao

time_temp=[1515628836]
for i in range(3):
    max_behot_time=time_temp.pop()
    print max_behot_time
    # time_temp.append(max_behot_time)
    get_toutiao(max_behot_time)

with open("toutiao.csv","w") as csvfile:
    writer =csv.writer(csvfile)
    writer.writerow(["标题","概述","作者"])
    for  data in toutiao:
        writer.writerow(data)



