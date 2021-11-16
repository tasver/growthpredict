import os
import redis
from rq import Worker, Queue, Connection
from rq.registry import ScheduledJobRegistry
from datetime import timedelta
from datetime import datetime


#listen = ['high', 'default', 'low']
#redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:5000')
#conn = redis.from_url(redis_url)
#queue = Queue(connection=conn)
#if __name__ == '__main__':
#    with Connection(conn):
#        worker = Worker(map(Queue, listen))
#        worker.work(with_scheduler=True)

