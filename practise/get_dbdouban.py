import pymongo
import requests
import time

client  = pymongo.MongoClient()
db =client.douban
col_casts =db.casts
collections = db.movies
proxies ={
    "https":"https://125.210.121.113:3128"
}
def get_cast(id):
    if not id:
        return
    print 'fetching',id
    try:
        url ='https://api.douban.com/v2/movie/celebrity/'+str(id)
        req =requests.get(url,proxies=proxies)
        data =req.json()
        print 'update',id
        col_casts.update_one({'id':id},{'$set':data},upsert=True)
        print 'done',id
    except Exception as e:
        print e,id




for movie in collections.find():
    casts =movie['casts']
    for cast in casts:
        print cast['name'],cast['id']
        get_cast(cast['id'])
        time.sleep(1.5)

