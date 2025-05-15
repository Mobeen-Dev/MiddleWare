from taskiq import SimpleRetryMiddleware
from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler

# 1️⃣ Message broker – RabbitMQ via AMQP
broker = (
    AioPikaBroker("amqp://guest:guest@localhost:5672/")
    .with_middlewares(SimpleRetryMiddleware(default_retry_count=3))
)

# 2️⃣ Optional scheduler so tasks can self-declare cron/ETA labels
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
