#-*- encoding: utf-8 -*-
"""
new_seed.py
Created on 2018/9/2 22:59
Copyright (c) 2018/9/2.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.util.db_util import DBUtil
from python.common.util.html_util import HtmlUtil
from python.configs import config
from tld import get_tld
from python.common.util.util import Util
import sys

def create_seed():
    url="http://www.autohome.com.cn/all"
    category="汽车"
    sql="""
    insert into hainiu_web_seed (url,md5,domain,host,category,status) values 
    ('%s','%s','%s','%s','%s',0)
    """
    hu=HtmlUtil()
    domain=get_tld(url)
    host=hu.get_url_host(url)
    u=Util()
    md5=u.get_md5(url)
    rl=LogUtil().get_base_logger()
    try:
        d=DBUtil(config._OGC_DB)
        sql=sql % (url,md5,domain,host,category)
        d.execute(sql)
    except:
        rl.exception()
        d.rollback()
    finally:
        d.close()
if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    create_seed()
