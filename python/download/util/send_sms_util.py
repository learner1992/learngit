#-*- encoding: utf-8 -*-
"""
send_sms_util.py
Created on 2018/9/2 19:47
Copyright (c) 2018/9/2.
@author: ogc
"""
from python.configs import config
from python.common.util.log_util import LogUtil
import urllib2
import urllib


class SendSmsUtil:

    def send_sms(self, content, phone=config._ALERT_PHONE):
        """send alter sms for phone with content
        """
        l = LogUtil().get_base_logger()
        try:
            send_url = 'http://send.sms.hainiu.com:8080/s?command=cralwer&phone=%s&' % (phone)
            send_url += urllib.urlencode({'content': content.decode('utf-8').encode('gbk')})
            r = urllib2.urlopen(send_url).read()
            print "here01"
            if '0-OK' != r:
                print "here"
                l.error("短信发送失败,短信服务器返回状态为:%s,手机号:%s,内容:%s" % (r, phone, content))
                return False
        except:
            l.exception()
            return False
        return True

#暂时用不了，因为上面没有那个网址端口
if __name__ == '__main__':
    SendSmsUtil().send_sms('你好''110')
