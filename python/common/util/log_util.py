#-*- encoding: utf-8 -*-
"""
log_util.py
Created on 2018/8/30 19:33
Copyright (c) 2018/8/30.
@author: ogc
"""
import content,logging
from logging.handlers import TimedRotatingFileHandler

class LogUtil:
    base_logger=content._NULL_STR
    log_dict={}
