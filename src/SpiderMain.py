# -*- coding:utf-8 -*-
import sys
import GetProxyIP
from MySqlDBMgr import MySqlDBMgr
from NetHelperCookie import NetHelperCookie
from Parser import Parser

reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()

tags = [u'小说', u'散文', u'历史', u'爱情', u'管理', u'编程', u'生活', u'心理', u'美食',
    u'教育', '励志', u'数学', u'设计', u'军事', u'经济', u'文学', u'诗歌', u'传记',
    u'随笔', u'杂文', u'武侠', u'科幻', u'青春', u'悬疑', u'穿越', u'哲学', u'艺术',
    u'国学', u'政治', u'旅行', u'两性', u'养生', u'通信', u'互联网', u'体育']


class SpiderMain:
    mySqlDBMgr = MySqlDBMgr()
    netHelper = NetHelperCookie()
    parser = Parser()

    def __init__(self):
        self.start = 0
        self.tagIndex = 24
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
            while self.tagIndex < len(tags):
                while self.start < 50 * 20:
                    print '开始抓取', tags[self.tagIndex], '第', self.start / 20 + 1, '页图书'
                    URL = 'https://book.douban.com/tag/' + tags[self.tagIndex] + '?start=' + str(self.start)
                    page = self.netHelper.GetPage(URL)
                    if page is None:
                        self.start += 20
                        continue
                    file = open('book.txt', 'w')
                    file.write(page)
                    file.close()
                    subjectIdSet = self.parser.ParseSubjectId(page)
                    if subjectIdSet is None:
                        self.start += 20
                        continue
                    for subjectId in subjectIdSet:
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
        except Exception, e:
            print '抓取 ' + str(tags[self.tagIndex]) + ' 第 ' + str(self.start / 20) + ' 页失败 ' + str(self.start), e

    def main(self):
        print '开始抓取图书数据'
        self.GetBook()
        print '抓取完毕...'

GetProxyIP.GetProxyIP()
DoubanSpoder = SpiderMain()
DoubanSpoder.main()
