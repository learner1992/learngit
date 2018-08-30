# -*- encoding: utf-8 -*-
"""
queue_consumer.py
Created on 2018/8/30 21:06
Copyright (c) 2018/8/30.
@author: ogc
"""
import threading
from python.common.util.log_util import LogUtil
import base_consumer_action
import random, time


class Consumer(threading.Thread):
    _WORK_TRY_NUM = 0

    def __init__(self, queue, name, sleep_time, work_try_num):
        super(self.__class__, self).__init__()
        self.queue = queue
        self.name = name
        self.sleep_time = sleep_time
        self.work_try_num = work_try_num
        Consumer._WORK_TRY_NUM = work_try_num
        self.rl = LogUtil().get_logger('consumer', 'consumer' + self.name[:self.name.find("_")])

    def run(self):
        while True:
            try:
                # 这是一个阻塞方法
                action = self.queue.get()
                if not isinstance(action, base_consumer_action.ConsumerAction):
                    raise Exception("action not extends consumer base")
                sleep_time = random.randint(0, self.sleep_time * 10) * 0.1
                time.sleep(sleep_time)
                action.consumer_thread_name = self.name
                start_time = time.clock()
                re = action.action()
                end_time = time.clock()

                work_time = int(round(end_time - start_time))
                self.rl.info(("queue name %s finish,sleep time %s \'s,action time %s \'s"
                              "action retry %s times,result:%s") % \
                             (self.name, sleep_time, work_time, action.try_num, re.__str__() if re is not None else ""))
                if not re[0] and action.try_num<self.work_try_num:
                    action.try_num+=1
                    self.queue.put(action)
                self.queue.task_done()
            except:
                self.rl.exception()
