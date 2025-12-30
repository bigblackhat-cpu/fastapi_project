
model_instance = None

def model_init():
    global model_instance
    print("🔧 正在初始化 Worker 进程，加载 PaddleOCRVL 模型...")
    from paddleocr import PaddleOCRVL  # 👈 替换为实际导入路径
    model_instance = PaddleOCRVL()
    print(f'模型加载成功，id：{id(model_instance)}')
    print("✅ PaddleOCRVL 模型加载成功！")

def create_model():
    print('get model_instance')
    return model_instance