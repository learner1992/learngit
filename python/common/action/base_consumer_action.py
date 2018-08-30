#-*- encoding: utf-8 -*-
"""
base_consumer_action.py
Created on 2018/8/30 20:54
Copyright (c) 2018/8/30.
@author: ogc
"""
class ConsumerAction(object):
    '''
    消费者基类
    '''
    def __init__(self):
        self.try_num=1
        self.consumer_thread_name=''
    def action(self):
        pass
    def result(self,is_success,values):
        result_value=[]
        result_value.append(is_success)
        if not is_success:
            self.fail_action(values)
        else:
            self.success_action(values)
        for re in values:
            result_value.append(re)
        return result_value
    def fail_action(self,values):
        pass
    def success_action(self,values):
        pass
