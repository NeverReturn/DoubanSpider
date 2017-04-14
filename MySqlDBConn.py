#encoding=utf-8
'''
Created on 2012-11-12

Mysql Conn连接类
'''

import MySQLdb

class DBConn:

    conn = None

    #建立和数据库系统的连接
    def connect(self):
        self.conn = MySQLdb.connect(host="localhost",port=3306,user="root", passwd="8591715" ,db="allbookinfo",charset="utf8")

    #获取操作游标
    def cursor(self):
        try:
            return self.conn.cursor()
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    #关闭连接
    def close(self):
        return self.conn.close()
