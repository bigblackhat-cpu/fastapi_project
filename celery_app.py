from celery import Celery
from kombu import Queue
import time
import os
import dotenv
dotenv.load_dotenv()

app_celery = Celery(
    'tasks',
    broker=os.getenv('RABBITMQ_BROKER'),
    backend=os.getenv('REDIS_BACKEND')
)

# 显式声明队列，参数必须和已存在的队列完全一致！
app_celery.conf.task_queues = (
    Queue(
        'celery_app',
        queue_arguments={
            'x-max-length': 2,
            'x-overflow': 'reject-publish'   # 如果你也设置了这个，也要加上！
        }
    ),
)

app_celery.conf.worker_prefetch_multiplier = 0

@app_celery.task(queue ='celery_app' )
def add(name: str):
    print('===start')
    time.sleep(30)
    print("end")
    return f'Hellow my name is {name}'