#-*- encoding: utf-8 -*-
"""
time_util.py
Created on 2018/9/1 21:43
Copyright (c) 2018/9/1.
@author: ogc
"""
import datetime
import time
class TimeUtil:
    #返回当前天
    def now_day_utc(self,format='%Y-%m-%d'):
        return self.now_time_utc(format)
    #
    def now_hour_utc(self,format='%H'):
        return self.now_time_utc(format)
    #
    def now_min_utc(self,format='%M'):
        return self.now_time_utc(format)
    #
    def now_time_utc(self,format='%Y-%m-%d %H:%M:%S'):
        utc_now=datetime.datetime.utcnow()
        return utc_now.__format__(format)
    #
    def now_day(self,format='%Y-%m-%d'):
        return self.now_time(format)
    #
    def now_hour(self,format='%H'):
        return self.now_time(format)
    #
    def now_min(self,format='%M'):
        return self.now_time(format)
    #
    def now_time(self,format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format,time.localtime())
    #
    def get_dif_day_utc(self,format='%Y-%m-%d',hour=-1):
        return self.get_dif_time_utc(hour,format)
    #
    def get_dif_hour_utc(self,format='%H',hour=-1):
        return self.get_dif_time_utc(hour,format)
    #
    def get_dif_time_utc(self,hour,format='%Y-%m-%d %H:%M:%S',minute=0):
        dt=self.now_time_utc()
        d1=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
        d3=d1+datetime.timedelta(hours=hour,minutes=minute)
        return d3.__format__(format)
    #
    def get_dif_day(self,format='%Y-%m-%d',hour=-1):
        return self.get_dif_time(hour,format)
    #
    def get_dif_hour(self,format='%H',hour=-1):
        return self.get_dif_time(hour,format)
    #
    def get_dif_time(self,hour,format='%Y-%m-%d %H:%M:%S',minute=0):
        dt=self.now_time()
        d1=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
        d3=d1+datetime.timedelta(hours=hour,minutes=minute)
        return d3.__format__(format)
    #
    def str2timestamp(self,str,format='%Y-%m-%d %H:%M:%S'):
        try:
            if str:
                return time.mktime(time.strptime(str,format))
            else:
                return None
        except:
            return None
    #
    def timestamp2str(self,timestamp,format='%Y-%m-%d %H:%M:%S'):
        try:
            if timestamp:
                return time.strftime(format,time.localtime(timestamp))
            else:
                return None
        except:
            return None
    def get_dif_time_str(self,datastr,hour,format='%Y-%m-%d %H:%M:%S',minute=0):
        d1=datetime.datetime.strptime(datastr,'%Y-%m-%d %H:%M:%S')
        d3=d1+datetime.timedelta(hours=hour,minutes=minute)
        return d3.__format__(format)

if __name__ == "__main__":
    a = TimeUtil()
    print a.now_time()
    print a.now_day()
    print a.now_hour()
    print a.now_day_utc()
    print a.now_hour_utc()
    print a.get_dif_day_utc()
    print a.get_dif_hour_utc()
    print "###"
    print a.get_dif_time(hour=0,minute=-10,format='%Y-%m-%d %H')
    print a.get_dif_time(hour=-1,minute=-10,format='%Y-%m-%d %H:%M:00')
    print a.now_time(format='%Y-%m-%d %H:%M:00')
    print a.str2timestamp('2016-12-14 04:45:52')
    print a.timestamp2str(1481661952)
    print a.get_dif_time_str('2018-04-12 14:44:00',-24)
    last_crawl_time="2018-09-02 23:31:28"
    # if int(a.str2timestamp(str=last_crawl_time, format='%Y-%m-%d %H')) <= int(
    #         a.str2timestamp(a.get_dif_time(hour=-1, format='%Y-%m-%d %H'))):
    #     print '时间相等'
    # else:
    print last_crawl_time[:13]
    print a.str2timestamp(last_crawl_time[:12], '%Y-%m-%d %H')
    print int(a.str2timestamp(a.get_dif_time(hour=-1, format='%Y-%m-%d %H'),format='%Y-%m-%d %H'))



































