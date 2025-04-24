import json
from datetime import datetime  # :contentReference[oaicite:0]{index=0}
import os


def add_log( content: str, temperature: str="ACKNOWLEDGE",filename: str = "ServerLogs.json" ) -> None:
    """
    Append a log entry to a JSON file with fields:
      - datetime: ISO 8601 timestamp (with microseconds)
      - temperature: user-defined level (e.g., 'CRITICAL', 'REGULAR')
      - content: the log message

    If the file does not exist, it is created with an initial empty list [].

    :param filename: Path to the JSON log file.
    :param content:  Log message to record.
    :param temperature:  Severity or category of the log.
    """
    # 1. Prepare the new record
    record = {
        "datetime": datetime.now().isoformat(),  # :contentReference[oaicite:1]{index=1}
        "temperature": temperature,
        "content": content
    }

    # 2. Read existing records (or start with empty list)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)  # :contentReference[oaicite:2]{index=2}
                if not isinstance(data, list):
                    # If file isn’t a list, reset to empty list
                    data = []
            except json.JSONDecodeError:
                # Corrupted or empty file—start fresh
                data = []
    else:
        data = []

    # 3. Append and write back
    data.append(record)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  # :contentReference[oaicite:3]{index=3}


