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

app_celery.conf.task_queues = (
    Queue(
        'celery_app',
        queue_arguments={
            'x-max-length': 2,
            'x-overflow': 'reject-publish'   # 如果你也设置了这个，也要加上！
        }
    ),
)

try:
    model_instance = PaddleOCRVL() 
    print("✅ PaddleOCRVL 模型加载成功!")
except Exception as e:
    print(f"❌ 模型加载失败: {e}")
    model_instance = None

@app_celery.task(queue ='celery_app' )
def ocr_api(url: str):
    output = model_instance.predict(url)
    for res in output:
        res.save_to_json(save_path="output")
        res.save_to_markdown(save_path="output")

    return f'task is successfully .'