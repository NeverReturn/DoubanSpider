# -*- coding:utf-8 -*-
import ssl
import urllib2
import sys
import cookielib 
import random
import time


class NetHelperCookie(object):
    proxies = [
    "114.216.227.25:808", "183.21.43.233:32312", "124.88.67.19:80", "221.216.94.77:808"
    "61.191.173.31:08", "14.145.181.96:28357", "183.10.161.90:47447", "113.229.171.2:16217"
    "111.155.124.70:8123", "114.101.90.15:41354", "183.153.23.121:808", "123.115.22.206:33623"
    ]
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
            response = self.opener.open(request)
            print '页面抓取成功，开始分析: '
            page = response.read().decode('utf-8')
        except Exception, e:
            print '抓取失败, 具体原因: ', e
        finally:
            return page
