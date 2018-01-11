#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import time
import web
import json

# Top250（/v2/movie/top250），获取豆瓣电影排行榜前 250 部电影列表；
# 电影条目信息（/v2/movie/subject/:id），获取一部电影的详细信息。

db = web.database(dbn='sqlite',db='E:\sqlite\MovieSite.db')
movie_ids=[]
for index in range(0,250,50):
    response = urllib.urlopen('http://api.douban.com/v2/movie/top250?start=%d&count=50' % index)
    data = response.read()
    data_json = json.loads(data)
    movie250 = data_json['subjects']
    for movie in movie250:
        movie_ids.append(movie['id'])
    time.sleep(3)
print len(movie_ids)

def add_movie(data):
    movie = json.loads(data)
    #print movie['title']
    db.insert('movie',
        id=int(movie['id']),
        title=movie['title'],
        origin=movie['original_title'],
        url=movie['alt'],
        rating=movie['rating']['average'],
        image=movie['images']['large'],
        directors=','.join([d['name'] for d in movie['directors']]),
        casts=','.join([c['name'] for c in movie['casts']]),
        year=movie['year'],
        genres=','.join(movie['genres']),
        countries=','.join(movie['countries']),
        summary=movie['summary']
              )

count =0
for mid in movie_ids:
    print mid,count
    try:
        response=urllib.urlopen('http://api.douban.com/v2/movie/subject/%s'%mid)
        data= response.read()
        add_movie(data)
        count+=1
        time.sleep(3)
    except:
        print 'not found this movie'

