import sys
import time

from celery import Task

from ...workers.worker_gpu import app

class InferenceTask(Task):
    def __init__(self):
        super().__init__()
        print('InferenceTask init', sys.argv)
        time.sleep(5)
        self.init = True

@app.task(bind=True, base=InferenceTask)
def inference_task(self, data):
    print('inference_task ', sys.argv)

