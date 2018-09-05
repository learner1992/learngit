#-*- encoding: utf-8 -*-
"""
news_find_queue.py
Created on 2018/9/5 11:24
Copyright (c) 2018/9/5.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.util.db_util import DBUtil
from python.common.util.util import Util
from python.configs import config
from python.common.util.time_util import TimeUtil
from python.common.action.base_producer_action import ProducerAction
from python.common.action.base_consumer_action import ConsumerAction
from python.common.action.queue_producer import Producer
from python.common.action.queue_consumer import Consumer
from python.common.util.request_util import RequestUtil
from python.common.util.html_util import HtmlUtil
from tld import get_fld
from bs4 import BeautifulSoup
from lxml import etree
import Queue,sys,mx,time

queue_name="news_find_action"
def push_queue_items():
    rl = LogUtil().get_base_logger()
    page_size = 10
    insert_seed_sql = """
        insert into hainiu_queue(type,params,action) values (0,%s,%s);
        """
    count_seed_sql = """
        select count(1) from hainiu_web_seed;
        """
    select_seed_sql = """
            select id,url,category,last_crawl_time from hainiu_web_seed where status=0
            limit %s,%s for update;
            """
    update_queue_sql = """
            update hainiu_web_seed set last_crawl_time='%s' where id in (%s);
            """
    t=TimeUtil()
    try:
        d = DBUtil(config._OGC_DB)
        queue_total = d.read_one(count_seed_sql)[0]
        page_num=queue_total/page_size +1
        query_ids = []
        print page_num,page_size
        for i in range(0,page_num):
            sql=select_seed_sql % (i*page_size,page_size)
            select_list=d.read_tuple(sql)
            insert_list=[]
            for record in select_list:
                id=record[0]
                url=record[1]
                category=record[2]
                last_crawl_time=str(record[3])
                if last_crawl_time is None or int(t.str2timestamp(last_crawl_time[:13], '%Y-%m-%d %H')) <= \
                        int(t.str2timestamp(t.get_dif_time(hour=-1, format='%Y-%m-%d %H'), format='%Y-%m-%d %H')):
                # 进入这里的都是过去爬取的时间在一小时之前,或者没有爬取过
                    insert_list.append((category,url))
                    query_ids.append(str(id))
            d.executemany(insert_seed_sql,insert_list)
        if query_ids:
            ids = ','.join(query_ids)
            sql = update_queue_sql % (t.now_time(), ids)
            print t.now_time(), ids
            d.execute(sql)
    except:
        rl.exception()
        rl.error(sql)
        d.rollback()
    finally:
        d.close()

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    push_queue_items()