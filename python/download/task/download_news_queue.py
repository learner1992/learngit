#-*- encoding: utf-8 -*-
"""
download_news_queue.py
Created on 2018/9/3 0:38
Copyright (c) 2018/9/3.
@author: ogc
"""
from python.common.util.log_util import LogUtil
from python.common.util.db_util import DBUtil
from python.configs import config
from python.download.util.redis_util import RedisUtil
import sys
def push_queue_items():
    redis = RedisUtil()
    rl=LogUtil().get_base_logger()
    # redis_key = redis.kyes_limit_scan(pattern="down*", limit=10)
    # print redis_key
    # type为2意思是从redis中获取的待下载链接，为3意思是已经被消费者拿去下载了
    insert_queue_sql = """
            insert into hainiu_queue(type,params,action) values (2,'from redis','%s');
            """
    try:
        db=DBUtil(config._OGC_DB)
        redis_len=len(redis.get_conn().keys())
        page_size=10
        page_num=redis_len/page_size
        # redis_len = len(redis.get_conn().keys("down*"))
        # sum=0
        for i in range(0,page_num):
            redis_key=redis.kyes_limit_scan(pattern="down*",limit=page_size*(i+1),cursor=0)
            # sum+=len(redis_key)
            if len(redis_key) != 0:
                redis_value = redis.get_values_batch_keys(redis_key)
                for each in redis_value:
                    print redis_value
                    sql=insert_queue_sql%(each)
                    db.execute_no_commit(sql)
                db.commit()
                redis.delete_batch(redis_key)
            #避免后面无用的扫描
            # if sum==redis_len:
            #     break
        #下面是一下全取出来，没有分页的方法
        # redis_key=redis.get_conn().keys("down*")
        # print redis_key
        # if len(redis_key) !=0:
        #     redis_value = redis.get_values_batch_keys(redis_key)
        #     for each in redis_value:
        #         print redis_value
        #         sql=insert_queue_sql%(each[5:])
        #         db.execute_no_commit(sql)
        #     db.commit()
        #     redis.delete_batch(redis_key)
    except:
        rl.exception()
        rl.error(insert_queue_sql)
        db.rollback()
    finally:
        db.close()

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    push_queue_items()