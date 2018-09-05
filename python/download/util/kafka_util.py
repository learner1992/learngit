#-*- encoding: utf-8 -*-
"""
kafka_util.py
Created on 2018/9/2 15:44
Copyright (c) 2018/9/2.
@author: ogc
"""
from pykafka import KafkaClient
from python.common.util.util import Util
from python.common.util.log_util import LogUtil
import random,threading

class KafkaUtil:
    __kafka_connect_cache={}
    __lock=threading.Lock()
    #
    def __init__(self,kafka_conf):
        host_list=[host for host in kafka_conf['HOST'].split(',')]
        random.shuffle(host_list)
        host_str=",".join(host_list)
        self.cache_key="_".join((host_str,kafka_conf['TOPIC']))
        self.host=host_str
        self.topic=kafka_conf['TOPIC']
        self.rl=LogUtil().get_logger('consuer','consumer_kafka')
    #
    def push_message(self,message):
        self.__lock.acquire()
        u=Util()
        producer=u.get_dict_value(self.__kafka_connect_cache,self.cache_key)
        if producer is None:
            client=KafkaClient(hosts=self.host)
            topic=client.topics[self.topic]
            producer=topic.get_producer()
            self.__kafka_connect_cache[self.cache_key]=producer
        is_success=True
        try:
            producer.produce(message)
        except:
            is_success=False
            del self.__kafka_connect_cache[self.cache_key]
            self.rl.error('kafka push error chacheKey is %s' % (self.cache_key))
            self.rl.exception()
        self.__lock.release()
        return is_success

from python.configs import config
import time
if __name__=='__main__':
    k=KafkaUtil(config._KAFKA_CONFIG)
    for i in xrange(10):
        print k.push_message("ogc")
    #这里不睡眠就会报弱引用被回收问题，但是因为程序在集群上面是24小时运行的
    #所以对象会被把持住，不会被gc回收
    # time.sleep(10)











