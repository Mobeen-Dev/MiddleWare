from taskiq import SimpleRetryMiddleware
from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler
from datetime import datetime
from config import settings
import subprocess
import sys

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


@broker.task(schedule=[{"cron": "0 */8 * * *"  }])  # Every 8 hours (0:00, 8:00, 16:00) "0 */8 * * *"
async def run_script_every_8_hours():
    """Run a specific Python script every 8 hours"""
    script_path = "dataFeed.py"
    
    try:
        
        # Method A: Run Python script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
    
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "Script execution timed out"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
