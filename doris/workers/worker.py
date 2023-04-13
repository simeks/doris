import os

import redis

from celery import Celery

REDIS_URL = os.getenv('REDIS_URL')

app = Celery(
    'worker',
    broker=REDIS_URL,
    #backend=REDIS_URL,
)
app.config_from_object('doris.workers.config')

redis_client = redis.Redis(host='redis', port=6379)

app.autodiscover_tasks([
    'doris.tasks',
])
