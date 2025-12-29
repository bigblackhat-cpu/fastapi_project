import time
from . import app  # ← 导入上面创建的 app 实例

# 示例任务：ping
@app.task
def pingTask():
    print('===========task is start =========')
    for i in range(10):
        time.sleep(1)
        print(i + 1)
    print('===========task is successfully =========')
    return "ping"

@app.task()
def ocr_api(url: str):
    global model_instance
    if model_instance is None:
        raise RuntimeError("❌ 模型未加载！请检查 worker 初始化是否成功。")
    
    output = model_instance.predict(url)
    for res in output:
        res.save_to_json(save_path="output")
        res.save_to_markdown(save_path="output")
    return "task is successfully."