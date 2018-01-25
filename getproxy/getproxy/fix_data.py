# -*- coding: utf-8 -*-
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import requests
from collections import Counter

url ='http://localhost:28017/getxici/proxies/'
req =requests.get(url)
html =req.json()
print type(html),html['rows']
dict=[]
for data in html['rows']:
    for port in data['port']:
        dict.append(port)
print dict

most_port =Counter(dict).most_common(10)
a=[]
b=[]
for item in most_port:
    a.append(str(item[0]))
    b.append(int(item[1]))
print a,b



