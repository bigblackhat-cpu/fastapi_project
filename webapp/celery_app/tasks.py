import time
from . import app #model_instance,model_test  # ← 导入上面创建的 app 实例
import datetime
import uuid
import os
from .lib import create_model

# 示例任务：ping
@app.task
def pingTask():
    print('===========task is start =========')
    for i in range(10):
        time.sleep(1)
        print(i + 1)
    print('===========task is successfully =========')
    return "ping"

# @app.task
# def tes_single():
#     # global model_test
#     print(model_test)
#     return model_test

@app.task
def ocr_api(url: str):
    # global model_instance
    ocr_model = create_model()
    if ocr_model is None:
        raise RuntimeError("❌ 模型未加载！请检查 worker 初始化是否成功。")
    
    output = ocr_model.predict(url)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8] # 生成8位随机字符串

    folder_name = f"ocr_task_{timestamp}_{unique_id}"
    
    # 2. 创建文件夹
    output_dir = os.path.join(os.getcwd(), "output", folder_name)

    for res in output:
        res.save_to_json(save_path=output_dir)
        res.save_to_markdown(save_path=output_dir)
    

    return "task is successfully."