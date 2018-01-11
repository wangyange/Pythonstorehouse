import requests

url_1 = 'https://www.zhihu.com/api/v4/members/'
url_2 = '/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'

headers ={'Cookie':'aliyungf_tc=AQAAAEL3s1C8aQIAysbsdMhEuv6UYihT; d_c0="AGCCvO7W5gyPTlCUWYtf_VXdAN5AuTvMt7k=|1514429812"; _xsrf=dce7cb2c-1fe3-476a-bd0f-d91d2b045ec4; q_c1=1459e34341074eda8bbdef0a6866353a|1514429812000|1514429812000; _zap=cea312c0-5d09-496a-86db-61e5436719db; l_cap_id="YThmY2Y3NDFlODliNGY4Mzk3OTdkODhkNWVkYWJjYzU=|1514953015|ded31d8424625231b70fd893d6451429824ad8c7"; r_cap_id="MjgyNzM5OGZlMmE4NDdkOWE3NGYzYzFmNDg5MWM1ODM=|1514953015|db970134db9f3b4a8751e6b7fbc16bfb77de159f"; cap_id="YjU1M2UzOGMyOTM5NDFlMDg5NjM3ZmNlYzIxMTdmMDA=|1514953015|f8379d3473480ce10fab17c22bb3876f0dedab16"; capsion_ticket="2|1:0|10:1515393285|14:capsion_ticket|44:ZjJjODcyZmI2NjA0NDI2ODhhODRiYTE5Y2ZjMTY1YWQ=|3723300fd4f12c8ce6c4ca25e7961cf96b8c5d8d99c70c990cf9186f23fcd65f"; z_c0="2|1:0|10:1515393294|4:z_c0|92:Mi4xRl9vcEFnQUFBQUFBWUlLODd0Ym1EQ1lBQUFCZ0FsVk5EbDlBV3dCS2R5QkM5TjFqOURKWGNPUGxaZWliZmRXX1FR|65bc628a9bf1dab50dd1d95150c177a406073d6b9495e98149141960007eb9cc"; __utmc=51854390; __utmv=51854390.100--|2=registration_date=20151007=1^3=entry_date=20151007=1; __utma=51854390.1480226250.1515393354.1515393354.1515399873.2; __utmz=51854390.1515399873.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/crossin/activities',
'Host':'www.zhihu.com',
'Referer':'https://www.zhihu.com/people/crossin/following',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
}


to_crawl = ['crossin']
crawled = []

def get_following(user):
    print 'crawling', user
    global to_crawl,crawled
    url = url_1 + user + url_2
    for i in range(10):
        req = requests.get(url=url,headers=headers)
        data = req.json()
        print type(data)

        for user in data['data']:
            if user['follower_count']>600000:
                token = user['url_token'] # find token of url
                if token not in to_crawl and token not in crawled:
                    to_crawl.append(token)

        paging = data['paging']
        if paging['is_end']:
            break
        url = paging['next'].replace('http:','https:')

while len(to_crawl)>0:
    user = to_crawl.pop()
    crawled.append(user)
    get_following(user)

