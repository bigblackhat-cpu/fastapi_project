import time
from celery_app import app  # ← 导入上面创建的 app 实例

# 示例任务：ping
@app.task
def ping():
    print('===========task is start =========')
    for i in range(5):
        time.sleep(1)
        print(i + 1)
    print('===========task is successfully =========')
    return "ping"