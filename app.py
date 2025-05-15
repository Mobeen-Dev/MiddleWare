from fastapi import FastAPI, Request, HTTPException
from typing import List, Dict
import uvicorn
from tasks import *
# We will implement workers here
from contextlib import asynccontextmanager
from taskiq_fastapi import init           # <- FastAPI plugin
from broker import broker           # <- re-use broker
from datetime import datetime
from sync_service import SyncService
from taskiq_fastapi import init as taskiq_init
import taskiq_fastapi
from logger import get_logger
SyncService = SyncService()
app_logger = get_logger("WebApp")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect the broker
    await broker.startup()
    yield
    # Shutdown: close the broker connection
    await broker.close()
    
    
app = FastAPI(
  title="Shopify Bridge API",
  version="25.5.9",
  description="Receives JSON payloads and provides retrieval endpoints.",
  lifespan=lifespan,
)

# one-liner that lets Taskiq reuse FastAPI dependencies
taskiq_init(broker, "app:app")

data_store: List[Dict] = []

    
@app.get(
  "/health",
  summary="Health check",
  description="Simple endpoint to verify the service is running."
)
async def health_check():
    return {"status": "ok"}

# ——— webhook endpoints ————————————————————————
@app.post("/order_webhook", summary="Incoming Order Webhook Endpoint")
async def order_webhook(request: Request):
  try:
    payload = await request.json()
    task = await process_order.kiq(payload)  # ← returns AsyncTaskiqTask
    return {
      "status": "queued",
      "task_id": task.task_id
    }
  except Exception as e:
    app_logger.error("order_webhook :: %s", e)
    raise HTTPException(status_code=400, detail=str(e))

  


@app.post("/receive", summary="Bypass Endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}
  


@app.post("/update_product_webhook", summary="product update webhook endpoint")
async def update_product_webhook(request: Request):
  try:
    payload = await request.json()
    task = await process_product_update.kiq(payload)
    return {
      "status": "queued",
      "task_id": task.task_id
    }
  except Exception as e:
    app_logger.error("update_product_webhook :: %s", e)
    raise HTTPException(status_code=400, detail=str(e))
  # try:
  #   json_data = await request.json()
  #   await SyncService.handle_product_update(json_data)
  #   return {"status": "Data received successfully."}
  # except Exception as e:
  #   SyncService.logger.error(e)
  #   raise HTTPException(status_code=400, detail=str(e))
  

@app.post("/delete_product_webhook", summary="product delete webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.post("/create_product_webhook", summary="product create webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.get("/ui", summary="FlutterFlow UI Endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.get("/display")
@app.get("/")
async def display_data():
    return {"Working ...."}

# ——— optional: task status endpoint ————————————————

@app.get("/tasks/{task_id}")
async def task_status(task_id: str):
    # res = await taskiq.result_backend.get_result(task_id)
    # if res:
    #     return res.dict()         # {"status": "success", "return_value": …}
    return {"state": "PENDING"}

def main():
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,         # only for development
        log_level="info"
    )


if __name__ == "__main__":
    main()
