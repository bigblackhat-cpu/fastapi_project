from fastapi import FastAPI,Depends
from celery_app import ocr_api
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os
dotenv.load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[os.getenv('RABBITMQ_URL')],  # 允许的前端地址（可多个）
    # 或者开发时临时允许所有：
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST 等）
    allow_headers=["*"],  # 允许所有请求头
)


@app.get('/')
async def root():
    return {"message":"Hello there is fastapi app"}


@app.post('/api/ocr_transform')
async def ocr_transform(pic_url:str):
    """
    Docstring for ocr_transform

    here will make a message to rabbitmq use celery, we will use delay 
    """

    resule = ocr_api.delay(url=pic_url)
    
    return {'res': f'消息已发送，进入推理计算,{resule.ready()}'}



