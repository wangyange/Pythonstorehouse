#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import pymongo
import time
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

headers = {
 'Cookie': 'appver=1.5.0.75771',
 'Referer':'http://music.163.com/'
}
url = "http://music.163.com/api/search/pc"
data ={"s":"love","offset":1,"limit":1,"type":1000}
req = requests.post(url,data=data,headers=headers)
html =req.json()

client =pymongo.MongoClient()
db =client.wangyiyun
lyrics =db.lyrics


# try:
for result in html['result']['playlists']:
    print str(result['id'])
    url_1 = 'http://music.163.com/api/playlist/detail?id='+str(result['id'])+'&updateTime=-1'
    song_req = requests.get(url_1,headers=headers)
    songs = song_req.json()

    for id in songs['result']['tracks']:
        print 'start',str(id['id'])
        url_2 ='http://music.163.com/api/song/lyric?os=pc&id='+str(id['id'])+'&lv=-1&kv=-1&tv=-1'
        lyric_req = requests.get(url_2,headers=headers)
        try:
            lyric =lyric_req.json()
            lyrics.update_one({'id':id},{'$set':lyric},upsert=True)
            print 'done',str(id['id'])
            time.sleep(3)
        except Exception as e :
            print e
            continue



# except Exception as e :
#     print e,str(id['id'])






