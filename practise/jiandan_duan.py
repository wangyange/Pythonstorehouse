#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import re
import requests
import lxml.etree as etree

url = 'http://jandan.net/duan/'
data_all=''
for page in range(3):

    req = requests.get(url,headers={'user-agent':'chrome'})
    html =req.text
    tree = etree.HTML(html)

    result =tree.xpath('//li//div[@class="text"]')

    for div in result:
        author = div.xpath('../div[@class="author"]/strong/text()')
        print author
        data_all+= (author[0] + ":\n")
        content = div.xpath('p/text()')
        for p in content:
            data_all+=p
            data_all+="\n\n"

    current_page =tree.xpath('//span[@class="current-comment-page"]/text()')
    next_page = int(current_page[0].strip('[]'))-1
    url = 'http://jandan.net/duan/page-%d#comments'%next_page
    # print next_page,url

# with open('duan.text','w') as f:
#     f.write(data_all.encode(encoding='utf_8'))

