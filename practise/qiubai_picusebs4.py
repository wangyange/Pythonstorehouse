from bs4 import BeautifulSoup
import requests
import urllib
url ='https://www.qiushibaike.com/imgrank/'

for i in range(3):
    req = requests.get(url)
    html =req.text
    soup =BeautifulSoup(html,"lxml")
    result = soup.find_all('img',class_='illustration')
    for link in result:
        link =link.get('src')
        filename =link.split('/')[-1]
        retries = 0
        while retries<3:
            try:
                pic = requests.get("http:"+link)
                with open("pics/"+filename,'wb') as f:
                    f.write(pic.content)
            except requests.RequestException as e:
                print e
                retries+=1
                print filename+'faild'
            else:
               print filename+'succeed'
               break


            # urllib.urlretrieve("http:"+link,"pics/"+filename)


    current_page=soup.find_all('span',class_= 'page-numbers')
    current_page=current_page[0].text
    next_page =int(current_page)+1
    url = 'https://www.qiushibaike.com/imgrank/page/%d/'%next_page