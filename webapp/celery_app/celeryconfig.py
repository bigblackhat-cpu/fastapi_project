from kombu import Queue, Exchange
import os
import dotenv
dotenv.load_dotenv()

broker_url = os.getenv('RABBITMQ_BROKER')
result_backend = os.getenv('REDIS_BACKEND')

# 序列化
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# 时区（建议启用）
# timezone = 'Asia/Shanghai'
# enable_utc = False

# 并发
worker_prefetch_multiplier = 1
# concurrency = 1 只能用command输入

# 队列控制（关键！）
task_create_missing_queues = False

# 默认队列
task_default_queue = 'christmas_queue'

# 队列定义（显式 exchange），启动worker的时候会创建
task_queues = (
    Queue(
        'christmas_queue',
        exchange=Exchange('christmas_exchange', type='direct'),
        routing_key='simple_routing',
        queue_arguments={
            'x-max-length': 10,
            'x-overflow': 'reject-publish'
        }
    ),
)

# 路由
task_routes = {
    'tasks.ping': {'queue': 'christmas_queue'},

}

# 任务过期
task_expires = 60 * 30  # 30 分钟

# ACK 和重试（关键修复！）
task_acks_late = True   # ← 必须为 True！
task_default_retry_delay = 60
task_max_retries = 3

# 超时
task_time_limit = 300
task_soft_time_limit = 270

# 结果后端
result_expires = 60 * 60 * 24  # 24 小时

# 可选：忽略结果（如果不需要）
# task_ignore_result = True