import requests
from bs4 import BeautifulSoup
import urllib
from threading import Thread

def down_pic(link):
    filename =link.split('/')[-1]
    retries=0
    while retries<3:
        try:
            aa =requests.get('http:'+link)
            with open('pics2/'+filename,"wb") as f:
                f.write(aa.content)

            # urllib.urlretrieve('http:'+link,'pics2/'+filename)
        except Exception as e:
            retries+=1
            print e
            print filename,"faild"
        else:
            print filename,'succeed'
            break

url = 'https://www.qiushibaike.com/imgrank/'
for i in range(3):
    req =requests.get(url)
    html =req.text
    soup =BeautifulSoup(html,"lxml")
    result =soup.find_all('img',class_='illustration')

    for link in result:
        link =link.get('src')
        t=Thread(target=down_pic,args=(link,))
        t.start()


    current_page= soup.find_all('span',class_='page-numbers')
    current_page=current_page[0].text
    next_page =int(current_page)-1
    url = 'https://www.qiushibaike.com/imgrank/page/%d'%next_page





