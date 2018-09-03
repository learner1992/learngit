#-*- encoding: utf-8 -*-
"""
config.py
Created on 2018/8/30 19:31
Copyright (c) 2018/8/30.
@author: ogc
"""
#日志地址
LOG_DIR="D:\\tmp\\log\\python\\%s"

#数据地址
_LOCAL_DATA_DIR = 'D:\\tmp\\log\\data\\%s'


#数据库配置
_OGC_DB={'HOST':'localhost','USER':'root','PASSWD':'admin','DB':'ogc','CHARSET':'utf8','PORT':3306}

#数据库配置
#_HAINIU_DB = {'HOST':'nn2.hadoop', 'USER':'hainiu', 'PASSWD':'12345678', 'DB':'hainiucralwer', 'CHARSET':'utf8', 'PORT':3306}

#报警电话
_ALERT_PHONE = '110'

#下载任务配置_测试
_DOWN_CONFIG = {'QUERY_LIMIT':20,'QUERY_FAIL_TIMES':6,'WORK_THREAD_NUMS':5,'QUEUE_SLEEP_TIMES':2,'WORK_SLEEP_TIMES':3,'FAIL_RETRY_TIMES':2,'FILE_FLAG':'one'}

#下载任务配置
#_DOWN_CONFIG = {'QUERY_LIMIT':20,'FILE_FLAG':'one','QUERY_FAIL_TIMES':6,'WORK_THREAD_NUMS':10,'QUEUE_SLEEP_TIMES':1,'WORK_SLEEP_TIMES':3,'FAIL_RETRY_TIMES':2}

#查找新闻任务配置_测试
_FIND_NEWS_CONFIG = {'QUERY_LIMIT':1,'QUERY_FAIL_TIMES':6,'WORK_THREAD_NUMS':1,'QUEUE_SLEEP_TIMES':1,'WORK_SLEEP_TIMES':3,'FAIL_RETRY_TIMES':2}

#查找新闻任务配置
#_FIND_NEWS_CONFIG = {'QUERY_LIMIT':10,'QUERY_FAIL_TIMES':6,'WORK_THREAD_NUMS':5,'QUEUE_SLEEP_TIMES':1,'WORK_SLEEP_TIMES':3,'FAIL_RETRY_TIMES':2}

#KAFKA队列配置
_KAFKA_CONFIG = {'HOST':'nn1.hadoop:9092,nn2.hadoop:9092,s1.hadoop:9092', 'TOPIC':'ogc'}