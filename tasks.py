# tasks.py
from broker import broker
from sync_service import SyncService

service = SyncService()

@broker.task(retry_on_error=True, max_retries=3)
async def process_order(payload: dict) -> str:
    await service.handle_incoming_orders(payload)
    return "ok"

@broker.task(retry_on_error=True, max_retries=3)
async def process_product_update(payload: dict) -> str:
    await service.handle_product_update(payload)
    return "ok"

@broker.task(retry_on_error=True, max_retries=3)
async def refresh_all_products() -> str:
    await service.handle_all_products_sync()
    return "ok"
