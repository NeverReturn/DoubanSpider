# -*- coding:utf-8 -*-
import sys
import MySqlDBConn
from BookInfo import Book


class MySqlDBMgr(object):

    dbconn = MySqlDBConn.DBConn()

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        print 'MySqlDBMgr Init'
        self.dbconn.connect()

    def __del__(self):
        self.dbconn.close()

    def InsertBookInfo(self, book):
        sql = u'insert into bookinfo(title, author, translator, pubhouse, pubdata, price, isbn, subjectId)'
        sql += u' values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, %s, %s)'
        temp = sql % (book.title, book.author, book.translator, book.pubHouse,
            book.pubData, book.price, book.isbn, book.subjectId)
        try:
            self.dbconn.cursor().execute(temp)
            self.dbconn.commit()
        except Exception, e:
            print 'InsertBookInfo', e

    def InsertBookCategory(self, bookId, categoryId):
        values = (bookId, categoryId)
        sql = u'select * from bookcategory where bookId=%s and categoryId=%s'
        temp = sql % values
        cursor = self.dbconn.cursor()
        try:
            cursor.execute(temp)
        except Exception, e:
            print 'InsertBookCategory', e
        result = cursor.fetchone()
        if result is not None:
            return
        sql = u'insert ignore into bookcategory(bookId, categoryId) values (%s, %s)'
        temp = sql % values
        try:
            self.dbconn.cursor().execute(temp)
            self.dbconn.commit()
        except Exception, e:
            print 'InsertBookCategory', e

    def FindBookBySubjectId(self, subjectId):
        sql = u'select * from bookInfo where subjectId=' + str(subjectId)
        try:
            cursor = self.dbconn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception, e:
            print 'FindBookBySubjectId', e
        if result is not None:
            book = Book()
            book.id = result[0]
            book.title = result[1]
            book.author = result[2]
            book.translator = result[3]
            book.pubHouse = result[4]
            book.pubData = result[5]
            book.price = result[6]
            book.isbn = result[7]
            book.subjectId = result[8]
            return book
        else:
            return None

    def FindBookByIsbn(self, isbn):
        sql = u'select * from bookInfo where isbn=' + str(isbn)
        try:
            cursor = self.dbconn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception, e:
            print 'FindBookByIsbn', e
        if result is not None:
            book = Book()
            book.id = result[0]
            book.title = result[1]
            book.author = result[2]
            book.translator = result[3]
            book.pubHouse = result[4]
            book.pubData = result[5]
            book.price = result[6]
            book.isbn = result[7]
            book.subjectId = result[8]
            return book
        else:
            return None
