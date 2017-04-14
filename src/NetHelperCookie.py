# -*- coding:utf-8 -*-
import ssl
import urllib2
import sys
import cookielib


class NetHelperCookie(object):
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
        ssl._create_default_https_context = ssl._create_unverified_context

    def GetPage(self, URL):
        page = None
        self.count += 1
        try:
            if self.count == 100:
                self.count = 0
                self.cookie.clear()
            request = urllib2.Request(url=URL, headers=self.headers)
            response = self.opener.open(request)
            page = response.read().decode('utf-8')
        except Exception, e:
            print '抓取失败, 具体原因: ', e
        finally:
            return page
