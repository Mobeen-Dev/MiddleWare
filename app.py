from fastapi import FastAPI, Request, HTTPException
from typing import List, Dict
import uvicorn
from datetime import datetime

from ProductTitleStorage import ProductTitleStorage
from tasks import *
from fastapi.responses import FileResponse, Response
import os
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from broker import broker
from taskiq_fastapi import init as taskiq_init
from logger import get_logger

manager = ProductTitleStorage()
app_logger = get_logger("WebApp")
from models import ProductSchema, OrderWebhook, ProductDeleteSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup: establish connections
  await broker.startup()
  yield
  # Shutdown: gracefully close connections
  await broker.shutdown()
    
    
app = FastAPI(
  title="Shopify Bridge API",
  version="25.6.19",
  description="Receives JSON payloads and provides retrieval endpoints.",
  lifespan=lifespan,
)

wow=    [
        "https://b2b-control-panel.flutterflow.app",  # Production frontend
        "https://www.flutterflow.app",
        "https://app.flutterflow.io/",
        "https://www.flutterflow.io/"
    ],


app.add_middleware(
    CORSMiddleware,               # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], #
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Taskiq reuse FastAPI dependencies
taskiq_init(broker, "app:app")

data_store: List[Dict] = []
    
@app.get(
  "/health",
  summary="Health check",
  description="Simple endpoint to verify the service is running."
)
async def health_check():
    """Health check endpoint for deployment verification"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "fastapi-app",
        "version": "1.0.0"
    }

# ——— webhook endpoints ————————————————————————
@app.post("/order_webhook", summary="Incoming Order Webhook Endpoint")
async def order_webhook(request: Request):
  try:
    payload:OrderWebhook = await request.json()
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
    payload:ProductSchema = await request.json()
    task = await process_product_update.kiq(payload)
    return {
      "status": "queued",
      "task_id": task.task_id
    }
  except Exception as e:
    app_logger.error("update_product_webhook :: %s", e)
    raise HTTPException(status_code=400, detail=str(e))


@app.post("/delete_product_webhook", summary="product delete webhook endpoint")
async def delete_product_webhook(request: Request):
  try:
    payload:ProductDeleteSchema = await request.json()
    # task = await process_product_update.kiq(payload)
    return {
      "status": "queued",
      # "task_id": task.task_id
    }
  except Exception as e:
    app_logger.error("delete_product_webhook :: %s", e)
    raise HTTPException(status_code=400, detail=str(e))
  


@app.post("/create_product_webhook", summary="product create webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.get("/ui", summary="FlutterFlow UI Endpoint")
async def receive_data(request: Request):
  print(manager.count())
  print(manager.get_all())
  return {
    "count": manager.count(),
    "titles": manager.get_all()
  }


 



@app.get("/data-feed.csv")
async def serve_csv_file():
    # Specify your CSV file path here
    file_path = "bucket/product_feed.csv"  # Update this path
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    
    # Return file directly
    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename="data-feed.csv",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache"
        }
    )

@app.get("/display")
@app.get("/")
async def display_data(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

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
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
