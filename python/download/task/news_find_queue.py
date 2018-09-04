#-*- encoding: utf-8 -*-
"""
news_find_queue.py
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
from python.download.util.redis_util import RedisUtil
queue_name="new_find_queue"

def call_beautiful(url):
    '''
    给定url，获取
    :param url:
    :return:
    '''
    # url='http://roll.news.qq.com'
    r=RequestUtil()
    hu=HtmlUtil()
    t=TimeUtil()
    html=r.http_get_phandomjs(url)
    charset=hu.get_doc_charset(etree.HTML(html))
    domain=get_fld(url)
    host=hu.get_url_host(url)
    u=Util()
    rl=LogUtil().get_base_logger()
    print "domain:",domain,":host:",host
    soup=BeautifulSoup(html,'lxml')
    a_docs=soup.find_all("a")
    for a in a_docs:
        a_href=get_format_url(url,a,host,charset)
        if a_href and a.text:
            print a.text
            xpath=hu.get_dom_parent_xpath_js(a)
            create_time=int(t.str2timestamp(t.now_time()))
            create_day=int(t.now_day().replace("-",""))
            create_hour=int(t.now_hour())
            update_time=int(t.str2timestamp(t.now_time()))
            if get_fld(a_href)==domain:
                print a_href
                #说明是内链接，写入redis数据库
                redis_conn=RedisUtil().get_conn()
                redis=RedisUtil()
                key1="exist:"+u.get_md5(a_href)
                print redis_conn.keys(key1)
                if not redis_conn.keys(key1):
                    key2="down:"+u.get_md5(a_href)
                    dicts = {key1:url, key2:url}
                    redis.set_batch_datas(dicts)
                    #同时写入mysql-internal数据库保存信息
                    try:
                        db=DBUtil(config._OGC_DB)
                        insert_internal_sql="""
                        insert into hainiu_web_seed_internally (url,md5,param,domain,host,a_url,a_md5,
                        a_host,a_xpath,a_title,create_time,create_day,create_hour,update_time) 
                        values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");
                        """
                        sql=insert_internal_sql %(url,u.get_md5(url),"{title:"+a.text+"}",domain,host,a_href,u.get_md5(a_href),
                                                  hu.get_url_host(a_href),xpath,a.text,create_time,create_day,create_hour,update_time)
                        db.execute(sql)
                    except:
                        rl.exception()
                        rl.error(sql)
                        db.rollback()
                    finally:
                        db.close()
            else:
                #外连接写入mysql数据库，因为这部分只写，不会爬取
                db=DBUtil(config._OGC_DB)
                insert_external_sql="""
                insert into hainiu_web_seed_externally (url,md5,param,domain,host,a_url,a_md5,
                        a_host,a_xpath,a_title,create_time,create_day,create_hour,update_time) 
                        values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");
                        """
                sql = insert_internal_sql % (url, u.get_md5(url), a.text, domain, host, a_href, u.get_md5(a_href),
                                             hu.get_url_host(a_href), xpath, a.text,create_time,create_day,create_hour,update_time)
                try:
                    db.execute(sql)
                except:
                    rl.exception()
                    rl.error(sql)
                    db.rollback()
                finally:
                    db.close()
            # print a_href,'_',xpath,u.get_md5(xpath)


def get_format_url(url, a_doc, host,charset='utf-8'):
    a_href = a_doc.get('href')
    try:
        if a_href is not None and a_href.__len__() > 0:
            a_href = str(a_href).strip()
            a_href = a_href[:a_href.index('#')] if a_href.__contains__('#') else a_href
            a_href = a_href.encode(charset)
            # a_href = urllib.quote(a_href,safe='.:/?&=')
            if a_href.startswith('//'):
                url = 'https:' + a_href if url.startswith('https:') else 'http:' + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            elif a_href.startswith('/'):
                url = 'https://' + host + a_href if url.startswith('https:') else 'http://' + host + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            elif a_href.startswith('./') or a_href.startswith('../'):
                url = mx.URL.URL(str(url) + '/' + a_href)
                a_href = url.url
            elif not a_href.startswith('javascript') and not a_href.startswith('mailto') and not a_href.startswith(
                    'http') and a_href != '':
                url = 'https://' + host + '/' + a_href if url.startswith('https:') else 'http://' + host + '/' + a_href
                url = mx.URL.URL(str(url))
                a_href = url.url
            a_href = a_href[:-1] if a_href.endswith('/') else a_href
            # a_href = a_href.lower()
        get_fld(a_href)
    except:
        return ''

    if not a_href.startswith('http'):
        return ''
#这里是对后面的参数排序，进行归一化
    if a_href.__contains__('?'):
        a_params_str = a_href[a_href.index('?') + 1:]
        a_params = a_params_str.split('&')
        a_params.sort()
        a_params_str = '&'.join(a_params)
        a_href = a_href[:a_href.index('?') + 1] + a_params_str

    return a_href
class NewsFindQueueProducer(ProducerAction):
    def __init__(self,limit,fail_times):
        super(self.__class__, self).__init__()
        self.limit = limit
        self.fail_times = fail_times
        self.rl = LogUtil().get_logger('producer', 'producer' + queue_name)
    def queue_items(self):
        ip=Util().get_local_ip()
        select_queue_sql="""
        select id,action,params from hainiu_queue where 
        type=0 and fail_times<=%s and locate('%s',fail_ip)=0
        limit 0,%s for update;
        """
        #type=1意思是url已经分配给消费者了
        update_queue_sql="""
        update hainiu_queue set type=1 where id in (%s);
        """
        return_list=[]
        try:
            d=DBUtil(config._OGC_DB)
            sql=select_queue_sql % (self.fail_times,ip,self.limit)
            select_dict=d.read_dict(sql)
            print select_dict
            query_ids=[]
            for each in select_dict:
                id=each['id']
                url=each['action']
                category=each['params']
                query_ids.append(str(id))
                c = NewsFindQueueConsumer(id, url, category)
                return_list.append(c)
            if query_ids:
                ids=','.join(query_ids)
                sql=update_queue_sql % ids
                d.execute(sql)
        except:
            self.rl.exception()
            self.rl.error(sql)
            d.rollback()
        finally:
            d.close()
        return return_list

class NewsFindQueueConsumer(ConsumerAction):
    def __init__(self,id,action,params):
        super(self.__class__,self).__init__()
        self.id = id
        self.url = action
        self.params = params
        self.rl = LogUtil().get_logger('consumer', 'consumer' + queue_name)
    def action(self):
        is_success=True
        try:
            #这里应该是进行消费，也就是把hainiu_web_seed送过来的链接进行爬取url，然后放到redis中
            # 插入两条数据，如果数据已经存在了就pass，如果数据不存在就插入hainiu_queue中
            rl = LogUtil().get_base_logger()
            try:
                print "进到消费者线程"
                call_beautiful(self.url)
            except:
                rl.exception()
            finally:
                pass
        except:
            is_success=False
            self.rl.exception()
        return super(self.__class__,self).result(is_success,[self.id,self.url,self.params])
    def success_action(self,values):
        #成功之后应该删除hainiu_queue表中的数据,这里为了测试方便先修改状态，之后改成删除
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
        #失败之后恢复type为0，以便让其他线程继续访问
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

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    q=Queue.Queue()
    pp=NewsFindQueueProducer(20,6)
    p=Producer(q,pp,queue_name,2,2,2,3)
    p.start_work()