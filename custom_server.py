import asyncio
import time

from exceptiongroup import catch

from config import base_url, NO_IMAGE_URL, DISCONTINUED_KEYWORDS, REFURBISHED_KEYWORDS, USED_PRODUCT_KEYWORDS
from database import DB_Client
from logger import get_logger
from config import settings
from productFeed import ProductFeed, ProductFeedManager
from shopify import Shopify
db = DB_Client()
manager = ProductFeedManager()
logger = get_logger("ServerSync")

ImageData = []

parent_shopify = Shopify(settings.parent_store, "Manual Server Shopify")

query = """
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
query_params = {
  "after": None
}

hasNextPage = True
while hasNextPage:
  try:
    result = asyncio.run(parent_shopify.send_graphql_mutation(query, query_params, "GetProductsAndVariants"))
    result = result['data']['products']
  except Exception as e:
    time.sleep(10)
    continue
  # Pagintion Control
  pageInfo = result["pageInfo"]
  hasNextPage = pageInfo["hasNextPage"]
  # hasNextPage = False
  query_params['after'] = pageInfo["endCursor"]
  logger.info(f"Cursor: {pageInfo["endCursor"]}")

  # Product Handling Logic
  products: list = result["nodes"]
  
  for product in products:
    try:
      
      product_image = product.get("images", {})
      if product_image:
        product_image = product_image.get('edges', [])
      
      additional_image_link = [data.get('node', {}).get('url') for data in product_image]
      if additional_image_link:
        product_image = additional_image_link
        # product_image = additional_image_link[0]
        # additional_image_link = ",".join(additional_image_link[1:])
      else:
        product_image = [NO_IMAGE_URL]
        
      data = {
        "id": product["id"].split("/")[-1],
        "data":product_image
        }
      
      ImageData.append(data)
      
  
      

      variants = product["variants"]["nodes"]
    except Exception as e:
      time.sleep(10)
      continue
  
db.update_multiple_product_images(ImageData)
print(ImageData)
