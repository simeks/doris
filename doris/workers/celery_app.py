import time

import redis

from celery import Celery

celery_app = Celery("tasks", broker="redis://redis:6379/0")
redis_client = redis.Redis(host='redis', port=6379)

@celery_app.task(bind=True)
def process_data(self, data):
    for d in data:
        message = f'{3*d}'
        redis_client.publish('results_channel', message)
        time.sleep(1)
    redis_client.publish('results_channel', 'STOP')

# # Set up a semaphore to limit concurrent access to the model
# if not hasattr(process_data, "model_semaphore"):
#     from threading import Semaphore
#     process_data.model_semaphore = Semaphore(4)  # Replace 4 with the desired level of concurrency
