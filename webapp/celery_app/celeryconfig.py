from kombu import Queue
import os
import dotenv
dotenv.load_dotenv()

broker_url = os.getenv('RABBITMQ_BROKER')
result_backend = os.getenv('REDIS_BACKEND')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True



task_queues = (
    Queue(
        'celery_app',
        queue_arguments={
            'x-max-length': 2,
            'x-overflow': 'reject-publish'   # 如果你也设置了这个，也要加上！
        }
    ),
)