# -*- coding:utf-8 -*-
import urllib2
import re
import sys
from MySqlDBMgr import MySqlDBMgr
from NetHelper import NetHelper
from Parser import Parser

tags = [u'小说', u'散文', u'历史', u'爱情', u'管理', u'编程', u'生活', u'心理']


class SpiderMain:

    mySqlDBMgr = MySqlDBMgr()
    netHelper = NetHelper()
    parser = Parser()

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.start = 0
        self.tagIndex = 0
        self.param = '&filter=&type='
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
        self.filePath = 'DoubanTop250.txt'

    def GetBookDetail(self, subjectId):
        book = None
        try:
            URL = 'https://book.douban.com/subject/' + str(subjectId)
            page = self.netHelper.GetPage(URL)
            if page is None:
                print 'net error'
                return book
            file = open('book.txt', 'w')
            file.write(page)
            file.close()
            book = self.parser.ParseDetailInfo(page)
            book.subjectId = subjectId
            return book
        except Exception, e:
            print 'GetBookDetail', e

    def GetBook(self):
        try:
            while self.tagIndex < 8:
                while self.start < 100 * 20:
                    print '开始抓取 ' + tags[self.tagIndex] + '第 ' + str(self.start / 20 + 1) + ' 页图书'
                    URL = 'https://book.douban.com/tag/' + tags[self.tagIndex] + '?start=' + str(self.start)
                    page = self.netHelper.GetPage(URL)
                    if page is None:
                        self.start += 20
                        continue
                    subjectIdSet = self.parser.ParseSubjectId(page)
                    for subjectId in subjectIdSet:
                        print subjectId
                        book = self.mySqlDBMgr.FindBookBySubjectId(subjectId)
                        if book is not None:
                            bookId = book.id
                            categoryId = self.tagIndex + 1
                            self.mySqlDBMgr.InsertBookCategory(bookId, categoryId)
                        else:
                            book = self.GetBookDetail(subjectId)
                            if book is None:
                                continue
                            self.mySqlDBMgr.InsertBookInfo(book)
                            book = self.mySqlDBMgr.FindBookBySubjectId(subjectId)
                            bookId = book.id
                            categoryId = self.tagIndex + 1
                            self.mySqlDBMgr.InsertBookCategory(bookId, categoryId)
                    self.start += 20
                self.start = 0
                self.tagIndex += 1
        except:
            print '抓取 ' + str(tags[self.tagIndex]) + ' 第 ' + str(self.start / 20) + ' 页失败 ' + str(self.start)

    def main(self):
        print '开始抓取图书数据'
        self.GetBook()
        print '抓取完毕...'

DoubanSpoder = SpiderMain()
DoubanSpoder.main()
