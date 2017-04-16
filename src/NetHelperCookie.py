# -*- coding:utf-8 -*-
import ssl
import urllib2
import sys
import cookielib 
import random
import time


class NetHelperCookie(object):
    proxies = list()
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.headers = {
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn,zh;q=0.8',
            'Connection': 'keep-alive'}
        self.count = 0
        self.cookie = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handler)
        self.lastTime = 0
        file = open('proxyIP.txt', 'rU')
        lines = file.readlines()
        for line in lines:
            print 'ip: ' + line.strip()
            self.proxies.append(line.strip())
        ssl._create_default_https_context = ssl._create_unverified_context

    def GetPage(self, URL):
        page = None
        self.count += 1
        try:
            if self.count >= 10:
                random_proxy = random.choice(self.proxies)
                proxy_support = urllib2.ProxyHandler({"http":random_proxy})
                self.opener = urllib2.build_opener(proxy_support, self.handler)
                self.count = 0
                self.cookie.clear()
            request = urllib2.Request(url=URL, headers=self.headers)
            if time.time() - self.lastTime < 1:
                time.sleep(1)
            self.lastTime = time.time()
            print URL
            response = self.opener.open(request, timeout = 5)
            print '页面抓取成功，开始分析: '
            page = response.read().decode('utf-8')
        except Exception, e:
            print '抓取失败, 具体原因: ', e
            exit(0)
        finally:
            return page
