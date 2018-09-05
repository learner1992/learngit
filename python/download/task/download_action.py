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
from python.common.util.request_util import RequestUtil
from python.common.util.html_util import HtmlUtil
from python.download.util.kafka_util import KafkaUtil
from python.common.util.file_util import FileUtil
from tld import get_fld
from python.common.util.time_util import TimeUtil
import sys,Queue,os,time,re
from lxml import etree
queue_name="download_action"

def get_title(Html):
    '''
    用re抽取网页Title
    '''
    # Html = utf8_transfer(Html)
    compile_rule = ur'<title>.*</title>'
    title_list = re.findall(compile_rule, Html)
    if title_list == []:
        title = ''
    else:
        title = title_list[0][7:-8]
    return title

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
        update hainiu_queue set type=3 where id in (%s);
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
                sql = update_queue_sql %  ids
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
        self.url=action
        self.params=params
        self.rl=LogUtil().get_logger("consumer","consumer"+queue_name)
    def action(self):
        is_success = True
        try:
            # 这里应该是进行消费，也就是把hainiu_queue送过来的链接进行爬取url，然后放到hainiu_web_page中
            #并且保存文件到本地，还有推到kafka中
            r = RequestUtil()
            hu = HtmlUtil()
            u = Util()
            f = FileUtil()
            t = TimeUtil()
            db = DBUtil(config._OGC_DB)
            html = r.http_get_phandomjs(self.url)
            r.close_phandomjs()
            charset = hu.get_doc_charset(etree.HTML(html))
            html = html.decode(charset).encode(sys.getfilesystemencoding())
            title = get_title(html).decode(sys.getfilesystemencoding())
            html_string = str(html).replace('\n', '').replace('\r\n', '')
            md5_html_string = u.get_md5(html_string)
            base_path = config._LOCAL_DATA_DIR % os.sep + 'done'
            file_path = config._LOCAL_DATA_DIR % os.sep + 'done' + os.sep + md5_html_string
            # 写文件
            f.create_path(base_path)
            f.write_file_content(file_path, md5_html_string + "\001" + html_string)
            # 推kafka
            kafka_util = KafkaUtil(config._KAFKA_CONFIG)
            kafka_util.push_message(html_string)
            try:
                #把结果记录写入hianiu_web_page中
                insert_web_page_sql="""
                insert into hainiu_web_page (url,md5,param,domain,host,title,create_time,
                create_day,create_hour,update_time) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");
                """
                create_time = int(t.str2timestamp(t.now_time()))
                create_day = int(t.now_day().replace("-", ""))
                create_hour = int(t.now_hour())
                update_time = int(t.str2timestamp(t.now_time()))
                sql=insert_web_page_sql %(self.url,md5_html_string,"{title:"+self.params+"}",
                                          get_fld(self.url),hu.get_url_host(self.url),title,
                                          create_time,create_day,create_hour,update_time)
                db.execute(sql)
            except:
                self.rl.exception()
                self.rl.error(sql)
                db.rollback()
            finally:
                db.close()
        except:
            is_success = False
            self.rl.exception()
        return super(self.__class__, self).result(is_success, [self.id, self.url, self.params])

    def success_action(self, values):
        # 成功了就把hainiu_queue的记录删除
        delete_queue_sql = """
        delete from hainiu_queue where id in (%s);
        """
        try:
            sql = delete_queue_sql %  values[0]
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
                update hainiu_queue set fail_times=fail_times+1,fail_ip='%s' where id=%s;
                """
        update_sql1 = """
                update hainiu_queue set status=0,last_crawl_time='' where id =%s
                """
        try:
            d = DBUtil(config._OGC_DB)
            id = values[0]
            u = Util
            ip = u.get_local_ip()
            sql = update_sql % (ip, id)
            d.execute(sql)
            d.execute_no_commit(sql)
            #超过单机器尝试次数，工作状态置为不工作
            if (self.try_num == Consumer.work_try_num):
                sql = update_sql1 % id
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
    pp=DownloadActionProducer(20,6)
    p=Producer(q,pp,queue_name,2,2,2,3)
    p.start_work()
