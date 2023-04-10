import os

import hupper

from celery_app import celery_app

def run_celery_worker():
    argv = [
        '-A', 'doris.workers.celery_app',
        'worker',
        '--loglevel=info',
        '--concurrency=1',
    ]
    celery_app.worker_main(argv)

if __name__ == '__main__':
    if os.environ.get('AUTORELOAD', False):
        hupper.start_reloader('run_workers.run_celery_worker')
    run_celery_worker()
