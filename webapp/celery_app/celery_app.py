from celery import Celery
from celery.signals import worker_process_init

app = Celery('fastapi_app')
app.config_from_object('celeryconfig')


model_instance = None

# @worker_process_init.connect
# def init_worker_process(**kwargs):
#     """
#     在每个 Celery worker 子进程启动时调用
#     """
#     global model_instance
#     print("🔧 正在初始化 Worker 进程，加载 PaddleOCRVL 模型...")
#     from paddleocr import PaddleOCRVL  # 👈 替换为实际导入路径
#     model_instance = PaddleOCRVL()
    
#     print("✅ PaddleOCRVL 模型加载成功！")

# @app.task(queue='celery_app')
# def ocr_api(url: str):
#     global model_instance
#     if model_instance is None:
#         raise RuntimeError("❌ 模型未加载！请检查 worker 初始化是否成功。")
    
#     output = model_instance.predict(url)
#     for res in output:d
#         res.save_to_json(save_path="output")
#         res.save_to_markdown(save_path="output")
#     return "task is successfully."
import time
@app.task()
def ping():
    print('===========task is start =========')
    for i in range(5):
        time.sleep(1)
        print(i+1)
    print('===========task is successfuly =========')
    return 
