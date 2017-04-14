# -*- coding:utf-8 -*-
import urllib2
import sys


class NetHelper(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}

    def GetPage(self, URL):
        page = None
        try:
            request = urllib2.Request(url=URL, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print '抓取失败, 具体原因: ', e.reason
        finally:
            return page
