import asyncio
import time

from exceptiongroup import catch

from config import base_url, NO_IMAGE_URL, DISCONTINUED_KEYWORDS, REFURBISHED_KEYWORDS, USED_PRODUCT_KEYWORDS
from database import DB_Client
from logger import get_logger
from config import settings
from productFeed import ProductFeed, ProductFeedManager
from shopify import Shopify
from test import parent_shopify

manager = ProductFeedManager()
logger = get_logger("DataFeed")

enum_validations = {
  'availability': ["in stock", "available for order", "preorder", "out of stock", "discontinued"],
  'condition': ["new", "refurbished", "used"],
  'gender': ["male", "female", "unisex"]
}


def availability_status(variant):
  title_list = variant["displayName"].lower().split()
  for title in title_list:
    if title in DISCONTINUED_KEYWORDS:
      return "discontinued"
  if variant["sellableOnlineQuantity"] > 0:
    return "in stock"
  elif variant["sellableOnlineQuantity"] < 0:
    return "available for order"
  elif variant["sellableOnlineQuantity"] == 0:
    return "out of stock"
  
  return "preorder"
def condition_status(variant):
  title_list = variant["displayName"].lower().split()
  for title in title_list:
    if title in REFURBISHED_KEYWORDS:
      return "refurbished"
    if title in USED_PRODUCT_KEYWORDS:
      return "used"
  return "new"
def format_price(variant):
  price = variant.get('price', 1)
  if price:
    unit = 'PKR'
    return str(price)+unit
def format_weight(variant):
  UNIT_MAP = {
    "GRAMS": "g",
    "KILOGRAMS": "kg",
    "OUNCES": "oz",
    "POUNDS": "lb"
  }
  weights = variant["inventoryItem"].get('measurement', {}).get('weight', None)
  if weights:
    value = weights.get('value', 1)
    unit = weights.get('unit', 'POUNDS')
    unit = UNIT_MAP.get(unit, 'lb')
    return str(value)+unit
def format_title(base_title, variant):
  if variant["title"] != "Default Title":
    return base_title+ " : "+variant["title"]
  else :
    return base_title
  


parent_shopify = Shopify(settings.parent_store, "DataFeed Shopify")

query="""
  query GetProductsAndVariants($after: String) {
    products(first: 249, after: $after) {
      nodes {
        category {
          fullName
        }
        productType
        id
        description
        title
        vendor
        handle
        images(first: 10) {
          edges {
            node {
              url
            }
          }
        }
        variants(first: 249) {
          nodes {
            inventoryItem {
              measurement {
                weight {
                  value
                  unit
                }
              }
            }
            displayName
            id
            title
            price
            sellableOnlineQuantity
            image {
              url
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
"""
query_params={
  "after": None
}

hasNextPage = True
while hasNextPage :
  try:
    result = asyncio.run(parent_shopify.send_graphql_mutation(query, query_params, "GetProductsAndVariants"))
    result = result['data']['products']
  except Exception as e:
    time.sleep(3)
    continue
  # Pagintion Control
  pageInfo = result["pageInfo"]
  hasNextPage = pageInfo["hasNextPage"]
  # hasNextPage = False
  query_params['after'] = pageInfo["endCursor"]
  # Product Handling Logic
  products:list = result["nodes"]
  
  for product in products:
    try:
      title = product["title"]
      vendor = product["vendor"]
      product_url = base_url+product["handle"]
      description = product["description"]
      description += "This is description Provided by Store Please visit store for Official Documentation and description of Product"
      item_group_id = parent_shopify.extract_id_from_gid(product["id"])
      product_image = product.get("images",{})
      if product_image:
        product_image = product_image.get('edges',[])
      
      additional_image_link = [url.get('node',{}).get('url') for url in product_image]
      if additional_image_link:
        product_image = additional_image_link[0]
        additional_image_link = ",".join(additional_image_link[1:])
      else:
        product_image = NO_IMAGE_URL
        additional_image_link = ""

      
  
      product_type = product.get("category", {})
      if product_type:
        product_type = product_type.get("fullName","")
      else:
        product_type = ""
      variants = product["variants"]["nodes"]
    except Exception as e:
      continue
    
    for variant in variants:
      try:
        variant_title = format_title(title, variant)
        sku_id = parent_shopify.extract_id_from_gid(variant["id"])
        availability = availability_status(variant)
        condition =  condition_status(variant)
        price = format_price(variant)
        v_image = variant["image"]
        if v_image:
          v_image = v_image.get('url')
          additional_image_link += f",{product_image}"
        else:
          v_image = product_image
        variant_url = product_url+f"?variant={sku_id}"
        shipping_weight = format_weight(variant)
        
        product1 = ProductFeed(
          sku_id=sku_id,
          title=variant_title,
          description=description,
          availability=availability,
          condition=condition,
          price=price,
          link=variant_url,
          image_link=v_image,
          brand=vendor,
          item_group_id=item_group_id,
          product_type=product_type,
          google_product_category=product_type,
          shipping_weight=shipping_weight,
          additional_image_link=additional_image_link
        )
        manager.add_product(product1)
      except Exception as e:
        continue
  
# Export to CSV
manager.export_to_csv("product_feed.csv", "bucket/")
# logger.info("Re-New DataFeed File")
