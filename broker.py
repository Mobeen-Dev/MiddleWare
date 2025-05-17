from taskiq import SimpleRetryMiddleware
from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler
from config import settings

# Message broker – RabbitMQ via AMQP
broker = (
    AioPikaBroker(settings.amqp_url)
    .with_middlewares(SimpleRetryMiddleware(default_retry_count=3))
)

# Scheduler so tasks can self-declare cron/ETA labels
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
