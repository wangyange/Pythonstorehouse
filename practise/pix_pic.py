import urllib
import requests
from bs4 import BeautifulSoup
from lxml import etree as etree

url ='https://pixabay.com/'
req =requests.get(url)
html =req.text
tree = etree.HTML(html)
result=tree.xpath("//div[@class='item']/a/img/@src")

def down(pic,filename):
    retries = 0
    while retries<3:
        try:
            with open("pics3/"+filename,'wb') as f:
                f.write(pic.content)
        except Exception as e:
            retries+=1
            print e
            print filename,"faild"
        else:
            print filename,'succeed'
            break

for link in range(len(result)):
    if result[link]!=result[link-1]:
        if 'jpg' in str(result[link]):
            filename = result[link].split('/')[-1]
            pic = requests.get(result[link],timeout=2)
            down(pic,filename)
        elif 'gif' in result[link]:

            result =tree.xpath("//div[@class='item']/a/img/@data-lazy")
            for link in range(len(result)):
                pic = requests.get(result[link],timeout=2)
                filename=result[link].split('/')[-1]
                down(pic,filename)
            else:
                break
    # retries = 0
    # while retries<3:
    #     try:
    #         with open("pics3/"+filename,'wb') as f:
    #             f.write(pic.content)
    #     except Exception as e:
    #         retries+=1
    #         print e
    #         print filename,"faild"
    #     else:
    #         print filename,'succeed'
    #         break





