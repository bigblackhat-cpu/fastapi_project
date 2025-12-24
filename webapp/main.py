from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import routers
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

app.include_router(routers.router)

