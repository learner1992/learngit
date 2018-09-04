#-*- encoding: utf-8 -*-
"""
news_find_action.py
Created on 2018/9/3 0:39
Copyright (c) 2018/9/3.
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

#把数据放入hainiu_queue,不一定用到，例子
def push_queue_items():
    insert_sql="""
    insert into hainiu_queue(type,params,action) values (1,%s,%s);
    """
    count_sql="""
    select count(1) from hainiu_web_seed;
    """
    select_sql="""
    select url,category from hainiu_web_seed limit %s,%s;
    """
    rl=LogUtil().get_base_logger()
    try:
        d=DBUtil(config._OGC_DB)
        sql=count_sql
        queue_total=d.read_one(sql)[0]
        print "queue total",queue_total
        page_size=1
        page=queue_total/page_size
        for i in range(0,page):
            sql=select_sql % (i*page_size,page_size)
            select_list=d.read_tuple(sql)
            print "page",i
            insert_list=[]
            for record in select_list:
                url=record[0]
                category=record[1]
                insert_list.append((category,url))
                print url,category
            d.executemany(insert_sql,insert_list)
    except:
        rl.exception()
        rl.error(sql)
        d.rollback()
    finally:
        d.close()
class NewsFindActionProducer(ProducerAction):
    def __init__(self,limit,fail_times):
        super(self.__class__, self).__init__()
        self.limit = limit
        self.fail_times = fail_times
        self.rl = LogUtil().get_logger('producer', 'producer' + queue_name)
    def queue_items(self):
        ip=Util().get_local_ip()
        select_seed_sql="""
        select id,url,category,domain,host,last_crawl_time from hainiu_web_seed where 
        fail_times<=%s and locate('%s',fail_ip)=0 and status=0
        limit 0,%s for update;
        """
        update_queue_sql="""
        update hainiu_web_seed set status=1,last_crawl_time='%s' where id in (%s);
        """
        return_list=[]
        try:
            d=DBUtil(config._OGC_DB)
            sql=select_seed_sql % (self.fail_times,ip,self.limit)
            select_dict=d.read_dict(sql)
            # print select_dict
            query_ids=[]
            t=TimeUtil()
            for each in select_dict:
                id=each['id']
                url=each['url']
                category=each['category']
                domain=each['domain']
                host=each['host']
                last_crawl_time=str(each['last_crawl_time'])
                if last_crawl_time is None or int(t.str2timestamp(last_crawl_time[:13],'%Y-%m-%d %H'))<=\
                        int(t.str2timestamp(t.get_dif_time(hour=-1,format='%Y-%m-%d %H'),format='%Y-%m-%d %H')):
                    #进入这里的都是过去爬取的时间在一小时之前,或者没有爬取过
                    query_ids.append(str(id))
                    action=url
                    params=category
                    c = NewsFindActionConsumer(id, action, params)
                    return_list.append(c)
            if query_ids:
                ids=','.join(query_ids)
                sql=update_queue_sql % (t.now_time(),ids)
                print t.now_time(),ids
                d.execute(sql)
        except:
            self.rl.exception()
            self.rl.error(sql)
            d.rollback()
        finally:
            d.close()
        return return_list

class NewsFindActionConsumer(ConsumerAction):
    def __init__(self,id,action,params):
        super(self.__class__,self).__init__()
        self.id = id
        self.ac = action
        self.params = params
        self.rl = LogUtil().get_logger('consumer', 'consumer' + queue_name)
    def action(self):
        is_success=True
        try:
            #这里应该是进行消费，也就是把hainiu_web_seed送过来的链接进行爬取url，然后放到hainiu_queue中
            #成功了就把hainiu_web_seed的status状态修改为0,一遍下一小时继续爬取
            print self.ac,self.params,self.id
            time.sleep(5)
            insert_sql = """
                insert into hainiu_queue(type,params,action) values (0,'%s','%s');
                """
            update_queue_sql = """
            update hainiu_web_seed set status=0,last_crawl_time='%s' where id in (%s);
            """
            rl = LogUtil().get_base_logger()
            try:
                print "进到消费者线程"
                db = DBUtil(config._OGC_DB)
                print insert_sql
                print self.params,self.ac
                sql=insert_sql % (self.params,self.ac)
                print sql
                db.execute(sql)
            except:
                rl.exception()
                rl.error(insert_sql)
                rl.error(update_queue_sql)
                db.rollback()
            finally:
                db.close()
        except:
            is_success=False
            self.rl.exception()
        return super(self.__class__,self).result(is_success,[self.id,self.ac,self.params])
    def success_action(self,values):
        print "success"
        update_queue_sql = """
        update hainiu_web_seed set status=0,last_crawl_time='%s' where id in (%s);
        """
        try:
            sql = update_queue_sql % (TimeUtil().now_time(), self.id)
            db = DBUtil(config._OGC_DB)
            db.execute(sql)
        except:
            self.rl.exception()
            self.rl.error(sql)
            db.rollback()
        finally:
            db.close()
    def fail_action(self,values):
        update_sql="""
        update hainiu_web_seed set fail_times=fail_times+1,fail_ip='%s' where id=%s;
        """
        update_sql1="""
        update hainiu_web_seed set status=0,last_crawl_time='' where id =%s
        """
        try:
            d=DBUtil(config._OGC_DB)
            id=values[0]
            u=Util
            ip=u.get_local_ip()
            sql=update_sql % (ip,id)
            d.execute_no_commit(sql)
            if(self.try_num==Consumer.work_try_num):
                sql=update_sql1 % id
                d.execute_no_commit(sql)
            d.commit()
        except:
            self.rl.error(sql)
            self.rl.exception()
        finally:
            d.close()

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    q=Queue.Queue()
    pp=NewsFindActionProducer(20,6)
    p=Producer(q,pp,queue_name,2,2,2,3)
    p.start_work()
    # push_queue_items()
    # test_beautiful("http://www.autohome.com.cn/all")
    # test_beautiful("http://sports.sina.com.cn/roll/index.shtml#pageid=13&lid=2503&k=&num=50&page=1")

