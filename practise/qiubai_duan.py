#!/usr/bin/python
# -*- coding: UTF-8 -*-

import lxml.etree as etree
import  requests
import urllib

url = 'https://www.qiushibaike.com/'
req = requests.get(url)
html =req.text
tree =etree.HTML(html)
xpath_div=tree.xpath('//div[@class="article block untagged mb15 typs_hot"]')
data =''
for i in range(3):
    for div in xpath_div:
        author = div.xpath('.//div[@class="author clearfix"]/a/h2/text()')
        content = div.xpath('.//div[@class="content"]/span/text()')
        good_laugh = div.xpath('.//div/span[@class="stats-vote"]/i[@class="number"]/text()')
        comment = div.xpath('.//div/span[@class="stats-comments"]/a/i[@class="number"]/text()')
        data+="\n作者:"+author[0].encode(encoding="utf_8")+"\t段子："+content[0].encode(encoding="utf_8")+"\t好笑："+good_laugh[0].encode(encoding="utf_8")+"\t评论："+comment[0].encode(encoding="utf_8")





    current_page=tree.xpath('.//li/a/span[@class="page-numbers"]/text()')
    next_page =int(current_page[0])-1
    url = 'https://www.qiushibaike.com/8hr/page/%d/'%next_page

with open('qiubai.txt','w') as f:
    f.write(data)





