from tasks import *
from config import settings
from shopify import  Shopify
from logger import get_logger
from database import DB_Client


class SyncService:
  def __init__(self):
    self.parent_shopify = Shopify(settings.parent_store, "Parent Shopify")
    self.child_shopify = Shopify(settings.child_store, "Child Shopify")
    self.db = DB_Client()
    self.logger = get_logger("SyncService")
    
  async def handle_product_create(self, product):
    await self.db.add_new_product(product)
  
  async def handle_product_update(self, response):
    parent_pid = response['id']
    child_pid, sync_enable, variants_count_db =  self.db.verify_sync_product(parent_pid)
    # print("\n\n Verify sync product output")
    # print("child_pid", child_pid, "sync_enable",sync_enable, "variants_count",variants_count_db)
    
    # Product is not in DB *NewProduct
    if child_pid==404 and not sync_enable :
      product_data = await self.parent_shopify.fetch_product_by_id(parent_pid)
      if product_data:
        await self.db.insert_parent_shopify_product_into_db(product_data)
      

      # print("this is not present in our database")
      return
      #return self.handle_product_create(product)
    if not sync_enable:
      return
    product_variants_count = len(response['variants'])
    # print("product_variants", product_variants_count)
    if variants_count_db != product_variants_count:
      pass
      # if not variants equl in db and in payload
      #   new entry in db for new variants
      #   delete previos shopify product add new
      # try to update the child product with new product also enter new variants in database if not update delete and create new

    #query to get validation discount and variant counts
    # if not valid return
    # if not present in db createproduct

    product_data = await self.parent_shopify.fetch_product_by_id(parent_pid)
    
    self.db.update_product_retail_price(product_data['variants']['edges'])

    # print("product_data")
    # print(product_data)
    price_list = self.db.fetch_variants_by_pid(parent_pid) # All the variants pricing data
    if child_pid:
      query_params = self.child_shopify.parse_into_query_params(product_data, f"gid://shopify/Product/{child_pid}")
      # print(query_params)
      query_params = self.update_params(query_params, price_list)
      response = await self.child_shopify.update_product(query_params)
      if response:
        product_id = response["product"]["id"]
        product_id = product_id.split('/')[-1]
        self.logger.info(f"Product Updates :: parent {parent_pid} -> child {product_id} updated")
      else:
        self.logger.warning(f"Product Updates Not Successful :: parent {parent_pid}")
    else:
      # await self.db.insert_parent_shopify_product_into_db(product_data)
      query_params = self.child_shopify.parse_into_query_params(product_data)
      self.logger.info("QueryParams on line 69 Passed")
      query_params = self.update_params(query_params, price_list)
      self.logger.info("QueryParams Update on line 72 Passed")

      response = await self.child_shopify.create_product(query_params)
      if response:
        product_id = response["product"]["id"]
        product_id = product_id.split('/')[-1]
        self.db.update_child_ids(parent_pid, response)
        self.logger.info(f"Product Created :: parent {parent_pid} -> child {product_id} updated")
      else:
        self.logger.warning(f"Product Creation Not Successful :: parent {parent_pid}")
        
  async def handle_product_delete(self, product):
    # query database to remove p_id and its associated vid
    pass
  
  def update_params(self, query_params, price_list):
    price_list = self.calculate_price(price_list)
    updated_variants = self.apply_price_on_params(query_params, price_list)
    
    # Remove Extra Keys from Params
    for variant in updated_variants:
      del variant['title']
    # Update Params
    query_params["input"]["variants"] = updated_variants
    return query_params

  async def handle_product_re_sync(self, product):
    # delete the previous product create a new product
    pass
  
  async def handle_all_products_sync(self):
    products = await self.parent_shopify.fetch_all_products()
    self.logger.info(f"Product Sync :: All Products Fetched count : {len(products)}")
    for product in products:
      await process_product_update.kiq(product)
  
    return products
  
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
  
  @staticmethod
  def calculate_price(price_list):
    for record in price_list:
      if record['b2b_prcnt']:
        record['b2b_price'] = record['b2b_discount'] * record['retail_price'] / 100
    return price_list
  
  @staticmethod
  def apply_price_on_params(query_params, price_list):
    variants = query_params.get("input", {}).get("variants", [])
    for variant in variants:
      for record in price_list:
        if record['title'] == variant['title']:
          variant['price'] = record['b2b_price']
    return variants
  
