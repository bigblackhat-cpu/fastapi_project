# webapp/celery_app/__init__.py
from celery import Celery

app = Celery('fastapi_app')
app.config_from_object('webapp.celery_app.celeryconfig')

# 自动发现 tasks 模块（相对于当前包）
app.autodiscover_tasks(['webapp.celery_app'])  # 注意：这里是模块路径，不是文件路径