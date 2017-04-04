# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2016-12-24 16:18:01
# @Last Modified by:   HaonanWu
# @Last Modified time: 2016-12-24 17:25:33

import urllib2
import json
from bs4 import BeautifulSoup
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


def nowplaying_movies(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    headers = {'User-Agent':user_agent}
    request = urllib2.Request(url = url, headers = headers)
    response = urllib2.urlopen(request)
    soup_packetpage = BeautifulSoup(response, 'lxml')
    items = soup_packetpage.findAll("li", class_="list-item")
    # items = soup_packetpage.findAll("li", {"class" : "list-item"}) 等价写法
    movies = []
    for item in items:
        if item.attrs['data-category'] == 'nowplaying':
            movie = {}
            movie['title'] = item.attrs['data-title']
            movie['score'] = item.attrs['data-score']
            movie['director'] = item.attrs['data-director']
            movie['actors'] = item.attrs['data-actors']
            movies.append(movie)
            print('%(title)s|%(score)s|%(director)s|%(actors)s' % movie)

    return movies



if __name__ == '__main__':
    # url = 'https://movie.douban.com/nowplaying/beijing/'
    # movies = nowplaying_movies(url)
    #
    # print('%s' % json.dumps(movies, sort_keys=True, indent=4, separators=(',', ': ')))
    # write_url = "C://Users//leoz//Desktop//hacker2017project//crawldata//"
    # v = u"我的"
    #
    # file_path = "C://Users//leoz//Desktop//hacker2017project//crawldata//news//我的.txt"
    # new_path = unicode(file_path, "utf-8")
    # fo = open(new_path, "w")
    #
    #
    # fo.write("我是你们")
    # for i in range(1,5):
    #     print  i
    # print time.time()
    # time.sleep(3)
    # print time.time()
    print time.localtime()