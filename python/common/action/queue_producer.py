# -*- encoding: utf-8 -*-
"""
queue_producer.py
Created on 2018/8/30 21:42
Copyright (c) 2018/8/30.
@author: ogc
"""
import threading, time
from python.common.util.log_util import LogUtil
import base_producer_action
import queue_consumer


class Producer(threading.Thread):
    def __init__(self, queue, action, name, max_num, sleep_time, work_sleep_time, work_try_num):
        super(self.__class__, self).__init__()
        self.queue = queue
        self.action = action
        self.name = name
        self.max_num = max_num
        self.sleep_time = sleep_time
        self.work_sleep_time = work_sleep_time
        self.work_try_num = work_try_num
        self.rl = LogUtil().get_logger("producer", "producer" + self.name)
        if not isinstance(action, base_producer_action.ProducerAction):
            raise Exception("action not extends producer base")

    def run(self):
        action_list = []
        while True:
            try:
                start_time = time.clock()
                if len(action_list) == 0:
                    action_list = self.action.queue_items()
                total_items = len(action_list)
                self.rl.info('get queue %s total items is %s ' % (self.name, total_items))
                while True:
                    if len(action_list) == 0:
                        break
                    unfinished_tasks = self.queue.unfinished_tasks
                    if unfinished_tasks <= self.max_num:
                        action = action_list.pop()
                        self.queue.put(action)

                end_time = time.clock()
                work_time = int(round(end_time - start_time))
                work_mins = work_time / 60
                self.rl.info('put queue %s total items is %s ,total time is %s \'s,(at %s items per mins' % \
                              (self.name, total_items, work_time,
                               int(total_items) if work_mins == 0 else round(float(total_items / work_mins), 2)))
                time.sleep(self.sleep_time)
            except:
                self.rl.exception()
    def start_work(self):
        for i in range(0,self.max_num):
            qc=queue_consumer.Consumer(self.queue,self.name+"_"+str(i),self.work_sleep_time,self.work_try_num)
            qc.start()
        time.sleep(5)
        self.start()
