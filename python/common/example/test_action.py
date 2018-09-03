#-*- encoding: utf-8 -*-
"""
test_action.py
Created on 2018/9/3 0:40
Copyright (c) 2018/9/3.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.util.db_util import DBUtil
from python.common.util.util import Util
from python.configs import config
from python.common.action.base_producer_action import ProducerAction
from python.common.action.base_consumer_action import ConsumerAction
from python.common.action.queue_producer import Producer
from python.common.action.queue_consumer import Consumer
import Queue,sys

queue_name="ogc_queue"
class OGCProducer(ProducerAction):
    def __init__(self,limit,fail_times):
        super(self.__class__,self).__init__()
        self.limit=limit
        self.fail_times=fail_times
        self.rl=LogUtil().get_logger('producer','producer'+queue_name)
    def queue_items(self):
        select_queue_sql="""
        select id,action,params from hainiu_queue where 
        type=1 and is_work=0 and fail_times<=%s
        limit 0,%s for update;
        """
        update_queue_sql="""
        update hainiu_queue set is_work=1 where id in (%s);
        """
        return_list=[]
        try:
            d=DBUtil(config._OGC_DB)
            sql=select_queue_sql % (self.fail_times,self.limit)
            select_dict=d.read_dict(sql)
            query_ids=[]
            for record in select_dict:
                id=record['id']
                action=record['action']
                params=record['params']
                query_ids.append(str(id))
                c=OGCConsumer(id,action,params)
                return_list.append(c)
            if query_ids:
                ids=','.join(query_ids)
                sql=update_queue_sql % ids
                d.execute(sql)
        except:
            self.rl.exception()
            self.rl.error()
            d.rollback()
        finally:
            d.close()
        return return_list

class OGCConsumer(ConsumerAction):
    def __init__(self,id,ac,params):
        super(self.__class__,self).__init__()
        self.id=id
        self.ac=ac
        self.params=params
        self.rl=LogUtil().get_logger('consumer','consumer'+queue_name)
    def action(self):
        is_success=True
        try:
            print self.ac,self.params
        except:
            is_success=False
            self.rl.exception()
        #这里是另外的写法
        return super(self.__class__,self).result(is_success,[self.id,self.ac,self.params])
    def success_action(self,values):
        delete_sql="""
        delete from hainiu_queue where id=%s
        """
        try:
            d=DBUtil(config._OGC_DB)
            id=values[0]
            sql=delete_sql%id
            d.execute(sql)
        except:
            self.rl.exception()
            self.rl.error()
            d.rollback()
        finally:
            d.close()
    def fail_action(self,values):
        update_sql="""
        update hainiu_queue set fail_times=fail_times+1,fail_ip='%s' where id=%s;
        """
        update_sql1="""
        update hainiu_queue set is_work=0 where id =%s
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
            self.rl.error()
            self.rl.exception()
        finally:
            d.close()

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    q=Queue.Queue()
    pp=OGCProducer(20,6)
    p=Producer(q,pp,queue_name,10,2,2,3)
    p.start_work()

