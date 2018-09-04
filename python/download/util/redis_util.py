#-*- encoding: utf-8 -*-
"""
redis_util.py
Created on 2018/9/2 16:30
Copyright (c) 2018/9/2.
@author: ogc
"""
import threading,time,json,sys
from rediscluster import StrictRedisCluster
class RedisUtil(object):
    _instance_lock=threading.Lock()

    def __init__(self):
        pass
    #实现单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(RedisUtil, "_instance"):
            with RedisUtil._instance_lock:
                if not hasattr(RedisUtil,"_instance"):
                    RedisUtil._instance=object.__new__(cls)
        return RedisUtil._instance
    #
    def create_conn(self):
        redis_nodes=[
            {'host':'nn1.hadoop','port':6379},
            {'host':'nn2.hadoop', 'port': 6379},
            {'host':'s1.hadoop', 'port': 6379},
            {'host':'s2.hadoop', 'port': 6379},
            {'host':'s3.hadoop', 'port': 6379},
            {'host':'s4.hadoop', 'port': 6379},
                     ]
        try:
            redisconn=StrictRedisCluster(startup_nodes=redis_nodes)
        except Exception:
            print "Connect error"
            sys.exit(1)
        self.redisconn=redisconn
        return redisconn
    #
    def get_conn(self):
        if not hasattr(self,'redisconn'):
            RedisUtil.redisconn=self.create_conn()
            self.redisconn=RedisUtil.redisconn
        return self.redisconn
    #
    def kyes_limit_scan(self,pattern='*',limit=1,cursor=0):
        """
        批量获取keys
        :param pattern:
        :param limit:获取前limit条中符合条件的
        :param cursor:
        :return:
        """
        limit_keys_obj=self.get_conn().scan(cursor,pattern,limit)
        limit_keys_list=[]
        for key,value in limit_keys_obj.items():
            for i in value[1]:
                limit_keys_list.append(i)
        return limit_keys_list
    #
    def get_values_batch_keys(self,keys):
        '''
        通过keys获取值values 列表
        :param keys:
        :return:
        '''
        return self.get_conn().mget(keys)
    #
    def get_value_for_key(self,key):
        return self.get_conn().get(key)
    #
    def set_data(self,key,value):
        return self.get_conn().set(key,value)
    #字典形式
    def set_batch_datas(self,keydicts):
        return self.get_conn().mset(keydicts)
    #
    def delete_data(self,key):
        return self.get_conn().delete(key)
    #
    def delete_batch(self,keys):
        for i in keys:
            self.get_conn().delete(i)
    #
    def rename_key(self,src,dst_new):
        return self.get_conn().rename(src,dst_new)
    #
    def get_all_key_value(self):
        keys=self.get_conn().keys()
        for i in keys:
            print i,':',self.get_conn().get(i)

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # g=RedisUtil()
    # dicts={'key1':11,'key2':22,'key3':'你好'}
    # s=g.set_batch_datas(dicts)
    # print s
    # list=['key1','key2','key3']
    # dd=g.get_values_batch_keys(list)
    # print dd
    redis_conn = RedisUtil().get_conn()
    redis = RedisUtil()
    print redis.get_value_for_key("down:9ea8932ebd6f148e5c24513d5d8cafb4")
    # sum=0
    # for i in range(12):
    #     s=redis.kyes_limit_scan(pattern='*', limit=1,cursor=i)
    #     print len(s),s
    #     sum+=len(s)
    # print sum
    # while True:
    #     redis_list = redis.get_values_batch_keys("down*")
    #     print redis_list
    #     if redis_list.__len__()==0:
    #         break
    #     for each in redis_list:
    #         print each[5:]
    #     print len(redis.get_values_batch_keys(redis_list))
    redis_len = len(redis.get_conn().keys())
    page_size = 10
    page_num = redis_len / page_size
    print redis_len,page_num
    for i in range(0, page_num):
        redis_key = redis.kyes_limit_scan(pattern="exist*", limit=page_size*(i+1), cursor=0)
        print redis_key.__len__(),redis_key
    # print redis.keys_limit_scan(pattern='*', limit=1, cursor=1)


    # print len(redis_conn.keys("down*"))



