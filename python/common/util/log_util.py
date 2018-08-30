#-*- encoding: utf-8 -*-
"""
log_util.py
Created on 2018/8/30 19:33
Copyright (c) 2018/8/30.
@author: ogc
"""
import logging,content
from logging.handlers import TimedRotatingFileHandler
from python.configs import config

class LogUtil:
    #设置单例日志对象
    base_logger=content._NULL_STR
    #设置字典判断日志对象是否已经生成，第一次生成单例对象后，将其放入dict中
    log_dict={}
    #判断单例对象是否为空，是则调用__get_logger重新生成，否则返回已有的对象
    def get_base_logger(self):
        if LogUtil.base_logger==content._NULL_STR:
            LogUtil.base_logger=self.__get_logger('info','info')
        return LogUtil.base_logger
    #接收日志名和文件名，合并为key，将生成的日志对象作为值，放入dict中
    #放入之前肯定要先看看是不是已经存在了，最后返回这个日志对象
    def get_logger(self,log_name,file_name):
        key=log_name+file_name
        if not LogUtil.log_dict.has_key(key):
            LogUtil.log_dict[key]=self.__get_logger(log_name,file_name)
        return LogUtil.log_dict[key]
    #这个方法用来重新生成一个LogUtil对象
    def __get_new_logger(self,log_name,file_name):
        l=LogUtil()
        l.__get_logger(log_name,file_name)
        return l
    #这里是真正的生成日志对象过程，self是必须加的，否则就是
    def __get_logger(self,log_name,file_name):
        self.logger=logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        #D是用day做分割？
        fh=TimedRotatingFileHandler(config.LOG_DIR % file_name,'D')
        fh.suffix="%Y%m%d.log"
        fh.setLevel(logging.INFO)
        ch=logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        return self
    def info(self,msg):
        self.logger.info(msg)
        self.logger.handlers[0].flush()
    def error(self,msg):
        self.logger.error(msg)
        self.logger.handlers[0].flush()
    def exception(self,msg='Exception Logged'):
        self.logger.exception(msg)
        self.logger.handlers[0].flush()

if __name__=="__main__":
    b=LogUtil().get_base_logger()
    b.info("info")
    b.error("error")
    try:
        1/0
    except:
        b.exception()







