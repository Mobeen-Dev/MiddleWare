from fastapi import FastAPI, Request, HTTPException
from typing import List, Dict
import uvicorn

from datetime import datetime
from sync_service import SyncService
SyncService = SyncService()
app = FastAPI(
  title="Shopify Bridge API",
  version="25.5.9",
  description="Receives JSON payloads and provides retrieval endpoints."
)
data_store: List[Dict] = []

@app.get(
  "/health",
  summary="Health check",
  description="Simple endpoint to verify the service is running."
)
async def health_check():
    return {"status": "ok"}


@app.post("/order_webhook", summary="Order webhook endpoint")
async def receive_data(request: Request):
  try:
    json_data = await request.json()
    await SyncService.handle_incoming_orders(json_data)
    return {"status": "Data received successfully."}
  except Exception as e:
    SyncService.logger.error(e)
    raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/update_product_webhook", summary="product update webhook endpoint")
async def receive_data(request: Request):
  try:
    json_data = await request.json()
    await SyncService.handle_product_update(json_data)
    return {"status": "Data received successfully."}
  except Exception as e:
    SyncService.logger.error(e)
    raise HTTPException(status_code=400, detail=str(e))
  

@app.post("/delete_product_webhook", summary="product delete webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.post("/create_product_webhook", summary="product create webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.get("/ui", summary="product create webhook endpoint")
async def receive_data(request: Request):
    return {"status": "Data received successfully."}


@app.get("/display")
@app.get("/")
async def display_data():
    return {"received_entries"}

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
