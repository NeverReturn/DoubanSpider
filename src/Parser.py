# -*- coding:utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup  
from BookInfo import Book


class Parser:

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.subjectListPattern = re.compile(
            u'<ul *?class="subject-list">(.*?)</ul>', re.S)
        self.subjectIdPattern = re.compile(
            u'<a *?class="nbg".*?subject_id:\'(.*?)\'.*?>', re.S)
        self.infoPattern = re.compile(
            u'<div[^>]id="info".*?>(.*?)</div>', re.S)
        self.titlePattern = re.compile(
            u'<span *?property="v:itemreviewed">(.*?)</span>', re.S)
        self.authorPattern = re.compile(
            u'<span.*?class="pl">.*?作者.*?<a.*?>(.*?)</a>', re.S)
        self.pubHousePattern = re.compile(
            u'<span *?class="pl"> *?出版社.*?</span>(.*?)<br/>', re.S)
        self.translatorPattern = re.compile(
            u'<span *?class="pl"> *?译者.*?<a.*?>(.*?)</a>', re.S)
        self.pubDataPattern = re.compile(
            u'<span *?class="pl"> *?出版年.*?</span>(.*?)<br/>', re.S)
        self.pricePattern = re.compile(
            u'<span *?class="pl"> *?定价.*?</span>.*?(\d+\.*\d*).*?<br/>', re.S)
        self.isbnPattern = re.compile(
            u'<span *?class="pl"> *?ISBN.*?</span>(.*?)<br/>', re.S)

    def ParseDetailInfo(self, page):
        try:
            book = Book()
            title = re.search(self.titlePattern, page)
            if title is not None:
                book.title = title.group(1).strip()
            bookInfos = re.search(self.infoPattern, page)
            bookInfo = bookInfos.group(1).strip()
            author = re.search(self.authorPattern, bookInfo)
            if author is not None:
                book.author = author.group(1).strip()
            '''
                print book.author
            else:
                print 'author not found!'
            '''
            pubHouse = re.search(self.pubHousePattern, bookInfo)
            if pubHouse is not None:
                book.pubHouse = pubHouse.group(1).strip()
            '''
                print book.pubHouse
            else:
                print 'pubHouse not found!'
            '''
            translator = re.search(self.translatorPattern, bookInfo)
            if translator is not None:
                book.translator = translator.group(1).strip()
            '''
                print book.translator
            else:
                print 'translator not found!'
            '''
            pubData = re.search(self.pubDataPattern, bookInfo)
            if pubData is not None:
                book.pubData = pubData.group(1).strip()
            '''
                print book.pubData
            else:
                print 'pubData not found!'
            '''
            price = re.search(self.pricePattern, bookInfo)
            if price is not None:
                book.price = price.group(1).strip()
            '''
                print book.price
            else:
                print 'price not found!'
            '''
            isbn = re.search(self.isbnPattern, bookInfo)
            if isbn is not None:
                book.isbn = isbn.group(1).strip()
            return book
            '''
                print book.isbn
            else:
                print 'isbn not found!'
            '''
        except Exception, e:
            print e

    def ParseSubjectId(self, page):
        subjectIdSet = set()
        try:
            soup = BeautifulSoup(page, 'lxml')
            subjectItems = soup.select('.subject-item')
            for subjectItem in subjectItems:
                subjectId = re.search(self.subjectIdPattern, str(subjectItem))
                if subjectId is not None:
                    subjectIdSet.add(subjectId.group(1).strip())
        except Exception, e:
            print e
        finally:
            return subjectIdSet

