#-*- encoding: utf-8 -*-
"""
demo_queue.py
Created on 2018/8/30 22:14
Copyright (c) 2018/8/30.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.action import base_producer_action,base_consumer_action,queue_consumer,queue_producer
import Queue

class OGCConsumerAction(base_consumer_action.ConsumerAction):
    def __init__(self,text):
        super(self.__class__,self).__init__()
        self.text=text
        self.rl=LogUtil().get_base_logger()
    def action(self):
        result=True
        r_test=''
        try:
            #这里是消费动作
            r_test="OGC"+str(self.text)
        except:
            result=False
            self.rl.exception()
        return self.result(result,[r_test])
    def fail_action(self,values):
        if self.try_num>=queue_consumer.Consumer._WORK_TRY_NUM:
            pass
    def success_action(self,values):
        pass
class OGCProducerAction(base_producer_action.ProducerAction):
        def queue_items(self):
            _list=[]
            for i in range(0,200):
                c=OGCConsumerAction(i)
                _list.append(c)
            return _list

if __name__=="__main__":
    q=Queue.Queue()
    pp=OGCProducerAction()
    p=queue_producer.Producer(q,pp,"OGC",100,10,3,3)
    p.start_work()