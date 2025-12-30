# Celery

```
本项目
start command
uv run celery -A webapp.celery_app worker -P solo
uv run celery -A webapp.celery_app worker --loglevel=info --concurrency=1
uv run fastapi run webapp/main.py --host 0.0.0.0 --port 8001



第三方
 python -m pip install paddlepaddle-gpu==3.2.2 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
 python -m pip install -U "paddleocr[doc-parser]"


 测试
 paddleocr doc_parser -i https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/paddleocr_vl_demo.png
```
## 命令行上能配置的
### 模式选择
启动的时候，可以选择并发模式，也就是 worker 的时候，指定用什么模式。
```cmd

进程模式
celery -A app worker -P prefork

协程模式
celery -A app worker -P gevent -c 100
celery -A app worker -P eventle

单进程单线程，window模式
celery -A app worker -P solo

多线程模式，累赘模式，因为单个python进程里的全部线程，没法分配到多个cpu核心，利用多个cpu核心计算的。
celery -A app worker -P threads -c 10

```

### 并发数量选择
除了 solo 模式，都有并发概念，那就能配置并发数，也就是 -c (concurrency)，但是并发底层和模式是有不同的
```
celery worker -P prefork -c 8
开8个子进程，每个进程只做一个任务，主要进程是一个管理进程。

celery worker -P gevent -c 100
开1个进程，里面有个线程，叫事件循环线程，里面有100个协程
```
python里，进程这个单位，是能被不同cpu核处理的

### 指定队列
默认会开一个celery队列，但是要接入一个就要指定
```python
celery -A proj worker -Q high,default
```

## 文件里能配置的
### prefxetch
碗里吃着，手里抓着  
每一个 concurrency， 都有个规则，能处理着一个任务，手里抓x个任务，这样一个c接的任务就是x+1，消息队列里看可能就很奇怪，直接指定x+1的数量n。  
如果 worker_prefxetch_multiplier = 1，那么x就是0，手里不抓任务
```
app.conf.worker_prefxetch_multiplier = 1
```
### workrt 挂了消息回到队列
```
task_acks_late = True
```
### 任务执行时间配置
```
task_time_limit = 300       # hard limit
task_soft_time_limit = 280  # soft limit
```
### 执行多少次重启
```
worker_max_tasks_per_child = 100
```
### 发信息到指定队列
2个配置方式，一个调用指定方式
```python
# 发到指定队列
@app.task(queue="high")
def send_email():
    pass

app.conf.task_queues = (
    Queue("default"),
    Queue("high"),
    Queue("low"),
)

send_email.apply_async(queue="high")
```

### 队列路由
因为我们有exchange，这个是celery连接上自动创的
```
task_routes = {
    "proj.tasks.send_email": {"queue": "high"},
    "proj.tasks.cleanup": {"queue": "low"},
}

```

## 总览 
```python
# proj/celeryconfig.py
from kombu import Queue

worker_prefetch_multiplier = 1
task_acks_late = True
worker_max_tasks_per_child = 100
task_time_limit = 300
task_soft_time_limit = 280

task_default_queue = "default"

task_queues = (
    Queue("default"),
    Queue("high"),
    Queue("low"),
)

task_routes = {
    "proj.tasks.critical_*": {"queue": "high"},
    "proj.tasks.cleanup_*": {"queue": "low"},
}

# 读取方式
app.config_from_object("proj.celeryconfig")

```


## 配置的一些方向
- 任务序列化方式
- 时区配置
- 预取的任务数 进程的最大并发数
- 定义 Exchange（交换机）
- 队列需绑定到 Exchange，并指定 routing_ke
- 路由规则
- 任务过期时间
- 队列最大长度
- 任务重试配置
- Worker 超时
