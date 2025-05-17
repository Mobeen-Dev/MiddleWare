from shopify import  Shopify
from database import DB_Client
from logger import get_logger
from config import settings


class SyncService:
  def __init__(self):
    self.parent_shopify = Shopify(settings.parent_store, "Parent Shopify")
    self.child_shopify = Shopify(settings.child_store, "Child Shopify")
    self.db = DB_Client()
    self.logger = get_logger("SyncService")
    
  def handle_product_create(self, product):
    self.db.add_new_product(product)
  
  async def handle_product_update(self, product):
    parent_pid = product['id']
    product_data = await self.parent_shopify.fetch_product_by_id(parent_pid)
    print("product_data")
    print(product_data)
    child_pid = self.db.verify_sync_product(parent_pid)
    if child_pid:
      response = await self.child_shopify.update_product(child_pid, product_data)
      id = response["product"]["id"]
      id = id.split('/')[-1]
      self.logger.info(f"Product Updates :: parent {parent_pid} -> child {id} updated")
    else:
      await self.db.insert_parent_shopify_product_into_db(product_data)
      product = await self.child_shopify.create_product(parent_pid, product_data)
      print("child_shopify product created")
      print(product)
      self.db.update_child_ids(parent_pid, product)
      
  async def handle_product_delete(self, product):
    # query database to remove p_id and its associated vid
    pass

  async def handle_product_re_sync(self, product):
    # delete the previous product create a new product
    pass
  
  async def handle_all_products_sync(self, product):
    # check which products are not present in db Add them
    pass
  
  async def handle_incoming_orders(self, orders):
    mutation = self.parent_shopify.draft_order_mutation()
    variables = await self.parse_order_webhook(orders)
    response = await self.parent_shopify.send_graphql_mutation(mutation, variables, "Parent")
    id = response["data"]["draftOrderCreate"]["draftOrder"]["id"]
    id = id.split('/')[-1]
    self.logger.info(f"Place Order :: parent {orders["id"]} -> child {id} updated ")
  
  async def parse_order_webhook(self, order_webhook: dict):
    customer = order_webhook["customer"]
    cid = await self.parent_shopify.process_customer(customer)
    line_items = order_webhook["line_items"]
    order_note = f"Order: {order_webhook["name"]}\n LineItems Price:{order_webhook['total_line_items_price']}"
    
    shipping_address = self.parent_shopify.process_shipping_address(order_webhook["shipping_address"])
    billingAddress = order_webhook["billing_address"]
    email = order_webhook["email"]
    phone = order_webhook["phone"]
    line_items, total_bill = self.process_line_items(line_items)
    variables = {
      "input": {
        "note": order_note,
        "tags": [
          "B2B"
        ],
        "shippingAddress": shipping_address,
        
        "appliedDiscount": {
          "description": "B2B",
          "value": 1,
          "valueType": "PERCENTAGE",
          "title": "appliedDiscount"
        },
        "lineItems": line_items
      }
    }
    if email:
      variables["input"]["email"] = email
    if phone:
      variables["input"]["phone"] = phone
    if cid:
      variables["input"]["customerId"] = cid
    
    return variables
  
  def process_line_items(self, line_items: list):
    updated_line_items = []
    total_bill = 0
    item_ids = [item['variant_id'] for item in line_items]
    parent_variants = self.db.fetch_parent_variants(item_ids)
    for idx, (vid, price) in enumerate(parent_variants):
      # print(f"Item #{idx}: first={vid}, second={price}")
      v_id = f"gid://shopify/ProductVariant/{vid}"
      qty = line_items[idx]["quantity"]
      total_bill += price * qty
      updated_line_items.append({
        "variantId": v_id,
        "quantity": qty,
      })
    return updated_line_items, total_bill