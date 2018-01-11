#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
render = web.template.render('templates/')
urls = (
    '/', 'index',
    '/movie/(.*)', 'movie',
    '/cast/(.*)', 'cast',
    '/director/(.*)', 'director',
)

db = web.database(dbn='sqlite',db='E:\sqlite\MovieSite.db')
class index:
    def GET(self):
        movies = db.select('movie')
        count = db.query('SELECT COUNT(*) AS COUNT FROM movie')[0]['COUNT']
        return render.index(movies,count,None)

    def POST(self):
        data = web.input()
        condition = r'TITLE LIKE"%' + data.title + r'%"'
        movies = db.select('movie',where=condition)
        count = db.query('SELECT COUNT(*) AS COUNT FROM movie WHERE ' +  condition)[0]['COUNT']

        return render.index(movies,count,data.title)


class movie:
    def GET(self,movie_id):
        movie_id=int(movie_id)
        movie=db.select('movie',where='id=$movie_id',vars=locals())[0]
        return render.movie(movie)

class cast:
    def GET(self,cast_name):
        condition = r'casts like "%' + cast_name + r'%"'
        movies = db.select('movie',where =condition)
        return render.index(movies)







if __name__=='__main__':
    app = web.application(urls,globals())
    app.run()


