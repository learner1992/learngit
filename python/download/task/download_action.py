#-*- encoding: utf-8 -*-
"""
download_action.py
Created on 2018/9/3 0:38
Copyright (c) 2018/9/3.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.util.db_util import DBUtil
from python.configs import config
from python.common.action.base_producer_action import ProducerAction
from python.common.action.base_consumer_action import ConsumerAction
from python.common.util.util import Util
from python.common.util.time_util import TimeUtil
from python.common.action.queue_producer import Producer
from python.common.action.queue_consumer import Consumer
from python.download.util.redis_util import RedisUtil
queue_name="download_action"
#把数据放入hainiu_queue,不一定用到，例子
class DownloadActionProducer(ProducerAction):
    def __init__(self,limit,fail_times):
        super(self.__class__,self).__init__()
        self.limit=limit
        self.fail_times=fail_times
        self.rl=LogUtil().get_logger("producer","producer"+queue_name)
    def queue_items(self):
        ip=Util().get_local_ip()
        select_queue_sql = """
        select id,action,params from hainiu_queue where 
        fail_times<=%s and locate('%s',fail_ip)=0 and type=2
        limit 0,%s for update;
        """
        #type=3 已被消费者进程拿取过了
        update_queue_sql = """
        update hainiu_web_seed set type=3 where id in (%s);
        """
        return_list = []
        try:
            d = DBUtil(config._OGC_DB)
            sql = select_queue_sql % (self.fail_times, ip, self.limit)
            select_dict = d.read_dict(sql)
            query_ids = []
            t = TimeUtil()
            for each in select_dict:
                id = each['id']
                action = each['action']
                params = each['params']
                query_ids.append(str(id))
                c = DownloadActionConsumer(id, action, params)
                return_list.append(c)
            if query_ids:
                ids = ','.join(query_ids)
                sql = update_queue_sql % (t.now_time(), ids)
                print t.now_time(), ids
                d.execute(sql)
        except:
            self.rl.exception()
            self.rl.error(sql)
            d.rollback()
        finally:
            d.close()
        return return_list

class DownloadActionConsumer(ConsumerAction):
    def __init__(self,id,action,params):
        super(self.__class__,self).__init__()
        self.id=id
        self.action=action
        self.params=params
        self.rl=LogUtil().get_logger("consumer","consumer"+queue_name)
    def action(self):
        is_success = True
        try:
            # 这里应该是进行消费，也就是把hainiu_queue送过来的链接进行爬取url，然后放到hainiu_web_page中
            #并且保存文件到本地，还有推到kafka中
            print self.action, self.params, self.id
            rl = LogUtil().get_base_logger()
            try:
                print "进到消费者线程"

            except:
                rl.exception()
            finally:
                pass
        except:
            is_success = False
            self.rl.exception()
        return super(self.__class__, self).result(is_success, [self.id, self.ac, self.params])

    def success_action(self, values):
        # 成功了就把hainiu_queue的记录删除
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

    def fail_action(self, values):
        #失败了就将记录type恢复为2，并累加fail_times
        update_sql = """
                update hainiu_web_seed set fail_times=fail_times+1,fail_ip='%s' where id=%s;
                """
        update_sql1 = """
                update hainiu_web_seed set status=0,last_crawl_time='' where id =%s
                """
        try:
            d = DBUtil(config._OGC_DB)
            id = values[0]
            u = Util
            ip = u.get_local_ip()
            sql = update_sql % (ip, id)
            d.execute_no_commit(sql)
            if (self.try_num == Consumer.work_try_num):
                sql = update_sql1 % id
                d.execute_no_commit(sql)
            d.commit()
        except:
            self.rl.error(sql)
            self.rl.exception()
        finally:
            d.close()

