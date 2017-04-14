# -*- coding:utf-8 -*-
import sys

class Book:

    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.id = ''
        self.title = ''
        self.author = ''
        self.translator = ''
        self.pubHouse = ''
        self.pubData = ''
        self.price = -1
        self.isbn = 0
        self.subjectId = 0
