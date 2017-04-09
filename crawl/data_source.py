# -*- coding:utf-8 -*-
import requests
import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import sys
import random
import time
import socket
reload(sys)
sys.setdefaultencoding('utf-8')

#获取代理
def get_proxy():
    proxy_list = []
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
    headers = {'User-Agent': user_agent}
    session = requests.session()
    for pageindex in range(1,2):
        page = session.get("http://www.xicidaili.com/wt/" + str(pageindex), headers=headers)
        soup = BeautifulSoup(page.text)  # 这里没有装lxml的话,把它去掉用默认的就好

        # 匹配带有class属性的tr标签
        taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
        for trtag in taglist:
            tdlist = trtag.find_all('td')  # 在每个tr标签下,查找所有的td标签
            proxy = {'http': tdlist[1].string + ':' + tdlist[2].string}
            proxy_support = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)

            url_test = "http://news.focus.cn/bj/yaowen/1"  #测试的url
            user_agent_test = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers_test = {'User-Agent': user_agent_test}
            try:
                request_test = urllib2.Request(url_test, headers=headers_test)
                response_test = urllib2.urlopen(request_test, timeout=3)
                content = response_test.read().decode('utf-8')
                proxy_list.extend(proxy)
                print "ok"
            except Exception, e:
                print "not ok"
                continue
            except socket.timeout as e:
                print "time out"
                print type(e)  # catched
            print tdlist[1].string  # 这里提取IP值
            print tdlist[2].string  # 这里提取端口值
    proxy_self = {'http': "127.0.0.1:80"}
    proxy_list.append(proxy_self)
    return proxy_list



news_dic = {}
baike_dic = {}
write_url = "C://Users//leoz//Desktop//hacker2017project//crawldata//"

#获取新闻的url和标题
def get_news():
    navs = ["yaowen","shichang","zhengce","tudi","shuju","qiye","fangtan","xiangmu","gundong"]
    number = 0
    page = 1
    number = 0
    for nav in navs:
        while True:
            number += 1
            if number % 20 == 0:
                print "crawler have a rest"
                time.sleep(60 * 1)
            print time.localtime()
            url = 'http://news.focus.cn/bj/' + nav + "/" + str(page)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = { 'User-Agent' : user_agent }
            try:
                request = urllib2.Request(url,headers = headers)
                response = urllib2.urlopen(request, timeout=20)
                content = response.read().decode('utf-8')
                pattern = re.compile('<div class="item-content clearfix">.*?<h4>.*?<a href="(.*?)" target="_blank">(.*?)</a></h4>', re.S)
                items = re.findall(pattern,content)
                if len(items) == 0:
                    break
                for item in items:
                    number += 1
                    print number,time.time(), item[0], item[1]
                    # news_dic[item[0]] = item[1]
                    write_news_content(item[0])
            except socket.timeout as e:
                print "time out"
                print type(e)  # catched
            except socket.error as e:
                print "socket error"
            except urllib2.URLError, e:
                print "get_news try except "
                if hasattr(e,"code"):
                    print e.code
                if hasattr(e,"reason"):
                    print e.reason
            page += 1

#获取百科的url和标题
def get_baike():
    number = 0
    page = 500
    number = 0
    while True:
        number += 1
        if number % 20 ==0:
            print "crawler have a rest"
            time.sleep(60 * 1)
        print time.localtime()
        url = 'http://baike.focus.cn/bj/p' + str(page)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            pattern = re.compile('<div class="content">.*?<span class="article-title">.*?<a href="(.*?)" target="_blank">(.*?)</a>',re.S)
            items = re.findall(pattern, content)
            if len(items) == 0:
                break
            for item in items:
                number += 1
                print number, time.time(), item[0], item[1]
                # baike_dic[item[0]] = item[1]
                write_baike_content(item[0])
        except socket.timeout as e:
            print "time out"
            print type(e)  # catched
        except socket.error as e:
            print "socket error"
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        page += 1
        if page > 2084:
            break

#获取新闻的内容
def write_news_content(value):
    # 设置使用代理
    # proxy = proxy_list[random.randint(0, len(proxy_list))]
    # proxy_support = urllib2.ProxyHandler(proxy)
    # # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler(debuglevel=1))
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)

    url = value
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        time.sleep(random.randint(1, 4))
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request, timeout=20)
        content = response.read().decode('utf-8')
        article_items = BeautifulSoup(content).findAll("p", {"style":"text-indent: 2em; text-align: left;"})
        if len(article_items) > 0:
            #获取文章的内容，将图片等去掉
            content_article = ""
            content_article_list = []
            for article_item in article_items:
                content_article_list.append(article_item.text)
            content_article = "\n".join(content_article_list)
            #写入文件，若没有内容，则跳过
            file_path = write_url + "news//" + get_news_filepath(url) + ".txt";
            if len(content_article) > 0:
                fo = open(file_path, "w")
                fo.write(content_article)
    except socket.timeout as e:
        print "time out"
        print type(e)  # catched
    except socket.error as e:
        print "socket error"
    except urllib2.URLError, e:
        print "write_news_content write end"
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    except urllib2.HTTPError, e:
        print "HTTPError"


#获取百科的内容
def write_baike_content(value):
    url = value
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        time.sleep(random.randint(1, 4))
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        article_items = BeautifulSoup(content).findAll("p", {"style":"text-indent: 2em; text-align: left;"})
        if len(article_items) > 0:
            #获取文章的内容，将图片等去掉
            content_article = ""
            content_article_list = []
            for article_item in article_items:
                content_article_list.append(article_item.text)
            content_article = "\n".join(content_article_list)
            #写入文件，若没有内容，则跳过
            file_path = write_url + "baike//" + get_baike_filepath(url) + ".txt";
            if len(content_article) > 0:
                fo = open(file_path, "w")
                fo.write(content_article)
    except socket.timeout as e:
        print "time out"
        print type(e)  # catched
    except socket.error as e:
        print "socket error"
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    print "write end"

#新闻的路径
def get_news_filepath(value):
    list = value.split('/')
    result = "_".join(list[4:6])
    result = result.replace(".html", "")
    return result

#百科的路径
def get_baike_filepath(value):
    list = value.split('/')
    result = "_".join(list[5:6])
    result = result.replace(".html", "")
    return result


def get_loupan():
    page = 1
    number = 0
    while True:
        time.sleep(5)
        number += 1
        if number % 20 == 0:
            print "crawler have a rest"
            time.sleep(60 * 1)
        print time.localtime()
        url = 'http://house.focus.cn/search/index_p' + str(page) + '.html'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            pattern = re.compile(
                '<div class="lp-t-title">.*?<a class="_click" type="1" target="_blank".*?href="http://house.focus.cn/loupan/(.*?).html',
                re.S)
            items = re.findall(pattern, content)
            if len(items) == 0:
                break
            for item in items:
                loupan_list.add(item)
                print number, item
        except socket.timeout as e:
            print "time out"
            print type(e)  # catched
        except socket.error as e:
            print "socket error"
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        page += 1
        if page > 2084:
            break
        f = open("C:\Users\leoz\Desktop\hacker2017project\groupId.txt", 'w')
        f.write(",".join(loupan_list))

# print "获取代理:", time.time()
# # proxy_list = get_proxy()
# print "获取代理结束:", time.time()
# print "获取百科:", time.time()
# get_baike()
# print "获取新闻结束:", time.time()
# print "获取新闻:", time.time()
# get_news()
# print "获取新闻结束:", time.time()
loupan_list = set()
get_loupan()
print loupan_list
loupan_string = ",".join(loupan_list)
print loupan_string

