# webapp/celery_app/__init__.py
from celery import Celery
from celery.signals import worker_process_init

app = Celery('fastapi_app')
app.config_from_object('webapp.celery_app.celeryconfig')

# 自动发现 tasks 模块（相对于当前包）
app.autodiscover_tasks(['webapp.celery_app'])  # 注意：这里是模块路径，不是文件路径



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