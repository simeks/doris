import time

from ..workers.worker import app, redis_client

@app.task()
def process_data(data):
    print('process_data', data)
    for d in data:
        message = f'{2*d}'
        redis_client.publish('results_channel', message)
        time.sleep(1)
    redis_client.publish('results_channel', 'STOP')
