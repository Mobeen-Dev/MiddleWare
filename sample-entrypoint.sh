#!/bin/sh
set -e

# Start Taskiq worker (background)
taskiq worker broker:broker -fsd &

# Start FastAPI (background)
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Optional: give it a moment
sleep 5

# Replace shell with scheduler (foreground = container PID 1)
exec taskiq scheduler broker:scheduler
