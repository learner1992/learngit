#-*- encoding: utf-8 -*-
"""
db_util.py
Created on 2018/8/31 19:08
Copyright (c) 2018/8/31.
@author: ogc
"""
from python.configs import config
import MySQLdb
class DBUtil:
    def __init__(self,db):
        self.db=MySQLdb.connect(host=db['HOST'],user=db['USER'],passwd=db['PASSWD'],db=db['DB'],
                                charset=db['CHARSET'],port=db['PORT'])
    def read_one(self,sql):
        self.cursor=self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    def read_tuple(self,sql):
        self.cursor=self.db.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def read_dict(self,sql):
        self.cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def executemany(self,sql,values):
        self.curosr=self.db.cursor()
        self.cursor.executemany(sql,values)
        self.db.commit()
    def execute_no_commit(self,sql):
        self.cursor=self.db.cursor()
        self.cursor.execute(sql)
    def execute(self,sql):
        self.cursor=self.db.cursor()
        self.cursor.execute(sql)
        self.db.commit()
    def commit(self):
        self.db.commit()
    def rollback(self):
        self.db.rollback()
    def rollback_close(self):
        self.db.rollback()
        self.db.close()
    def close(self):
        self.cursor=self.db.cursor()
        self.cursor.close()
        self.db.close()

if __name__=="__main__":
    # db=DBUtil(config._OGC_DB)
    # sql="""
    #     insert into test (id,name,class_id) values(%d,'%s',%d);
    # """
    # for i in range(10):
    #     sql_local=sql % (i,'ogc_%s' % i,i)
    #     db.execute(sql_local)
    # d=db.read_dict("select * from test")
    # print d
    # db.close()
    pass