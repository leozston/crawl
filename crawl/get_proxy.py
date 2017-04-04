# -*- coding:utf-8 -*-
import requests
import urllib2
from bs4 import BeautifulSoup
import re
import os.path


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
            print tdlist[1].string  # 这里提取IP值
            print tdlist[2].string  # 这里提取端口值
    return proxy_list

get_proxy()