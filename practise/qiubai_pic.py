import requests
import urllib
import lxml.etree as etree
from bs4 import BeautifulSoup
url = 'https://www.qiushibaike.com/imgrank/'
req = requests.get(url)
html =req.text

tree =etree.HTML(html)

result = tree.xpath('//div[@class="thumb"]/a/img[@class="illustration"]/@src')

print result

for link in result:
    print type(link)
    # filename = link.split('/')[-1]
    # print filename
    # urllib.urlretrieve('http:'+link,'pics/'+filename)



