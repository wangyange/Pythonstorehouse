import requests
import pymongo
client = pymongo.MongoClient()
db = client.douban
collections =db.movies

for start in range(0,250,20):
    url ='https://api.douban.com/v2/movie/top250?start='+str(start)
    req =requests.get(url)
    html =req.json()
    print('insert',start)
    collections.insert_many(html['subjects'])
    print('done',start)
