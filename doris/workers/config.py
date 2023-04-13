from kombu import Queue

task_queues = (
    Queue('gpu_tasks', routing_key='gpu_tasks'),
    Queue('tasks', routing_key='tasks'),
)

task_routes = {
    'doris.tasks.*': {'queue': 'tasks'},
    'doris.gpu_tasks.*': {'queue': 'gpu_tasks'},
}
