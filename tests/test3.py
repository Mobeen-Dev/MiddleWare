from RnD import logs_handler
import RnD.logs_handler.config
from pythonjsonlogger import jsonlogger
from RnD.logs_handler import RotatingFileHandler, QueueHandler, QueueListener
from queue import SimpleQueue

def setup_production_logger(log_file_path):
    # 1. Create a JSON formatter
    json_fmt = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )

    # 2. Configure a rotating file handler
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(json_fmt)

    # 3. (Optional) Queue-based handler for concurrency
    log_queue = SimpleQueue()
    queue_handler = QueueHandler(log_queue)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(queue_handler)

    # 4. Start a listener that writes queued records to file
    listener = QueueListener(log_queue, file_handler)
    listener.start()

    return logger

# Usage
logger = setup_production_logger('myapp.json')
try:
    # your application code...
    1 / 0
except Exception:
    logger.exception("Unhandled exception occurred")
