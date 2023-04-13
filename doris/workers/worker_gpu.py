import os

import redis

from celery import Celery
from celery.signals import worker_process_init

REDIS_URL = os.getenv('REDIS_URL')

app = Celery(
    'gpu_worker',
    broker=REDIS_URL,
    #backend=REDIS_URL,
)
app.config_from_object('doris.workers.config')
app.conf.worker_proc_alive_timeout = 60 # 60 seconds for it to initialize

redis_client = redis.Redis(host='redis', port=6379)

app.autodiscover_tasks([
    'doris.tasks.gpu',
])

@worker_process_init.connect
def init_worker(*args, **kwargs):
    print('INITIALIZING WORKER', args, kwargs)
