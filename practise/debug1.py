import requests

url='https://www.zhihu.com/topic'
req =requests.get(url)
print req
data =req.text