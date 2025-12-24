from celery import Celery
from kombu import Queue
import time
import os
import dotenv
dotenv.load_dotenv()
from celery.signals import worker_process_init

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

model_instance = None

@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    在每个 Celery worker 子进程启动时调用
    """
    global model_instance
    print("🔧 正在初始化 Worker 进程，加载 PaddleOCRVL 模型...")
    from paddleocr import PaddleOCRVL  # 👈 替换为实际导入路径
    model_instance = PaddleOCRVL()
    
    print("✅ PaddleOCRVL 模型加载成功！")

@app_celery.task(queue='celery_app')
def ocr_api(url: str):
    global model_instance
    if model_instance is None:
        raise RuntimeError("❌ 模型未加载！请检查 worker 初始化是否成功。")
    
    output = model_instance.predict(url)
    for res in output:
        res.save_to_json(save_path="output")
        res.save_to_markdown(save_path="output")
    return "task is successfully."

