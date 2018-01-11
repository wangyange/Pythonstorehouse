import web
import urllib
import time
db = web.database(dbn='sqlite',db='E:\sqlite\MovieSite.db')
def GetPosters(id,url):
    pic = urllib.urlopen(url).read()
    file_name = 'static/poster/%d.jpg'%id
    f= file(file_name,'wb')
    f.write(pic)
    f.close()

movies = db.select('movie')
count = 0
for movie in movies:
    GetPosters(movie.id,movie.image)
    count+=1
    print count,movie.title
    time.sleep(2)
