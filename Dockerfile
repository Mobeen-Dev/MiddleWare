# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Disable Python buffering & pip cache (speeds up containers)
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Put everything under /app
WORKDIR /app

# Install dependencies first for better layer-caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your source code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Start your app (edit the module path if it’s not main.py ⇢ app variable)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
