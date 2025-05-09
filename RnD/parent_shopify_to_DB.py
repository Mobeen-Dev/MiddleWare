import os
import time
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# ---------------------------
# Shopify configuration
# ---------------------------
SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
ACCESS_TOKEN = os.getenv("PARENT_SHOPIFY_API_SECRET")
API_VERSION = "2025-07"  # specify the API version

if not SHOPIFY_STORE or not ACCESS_TOKEN:
    raise ValueError("Please set SHOPIFY_STORE_NAME and SHOPIFY_API_SECRET in your .env file.")

# Build fully qualified domain (append ".myshopify.com" if necessary)
if "." not in SHOPIFY_STORE:
    store_domain = f"{SHOPIFY_STORE}.myshopify.com"
else:
    store_domain = SHOPIFY_STORE

shopify_url = f"https://{store_domain}/admin/api/{API_VERSION}/graphql.json"

shopify_headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# GraphQL query to retrieve product details, variants, and images.
# We request additional fields: productType, descriptionHtml, and tags.
shopify_query = """
query ($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    edges {
      cursor
      node {
        id
        title
        handle
        productType
        descriptionHtml
        tags
        variants(first: 249) {
          edges {
            node {
              id
              title
              sku
              inventoryQuantity
              price
            }
          }
        }
        images(first: 100) {
          edges {
            node {
              src
            }
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

# ---------------------------
# Supabase configuration
# ---------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# Function to insert data into Supabase
# ---------------------------
def insert_product_into_supabase(product):
    # Extract product-level details.
    full_product_id = product["id"]
    product_id = full_product_id.split('/')[-1]
    product_id = int(product_id)
    title = product.get("title", "")
    handle = product.get("handle", "")
    # Use productType, descriptionHtml, and join tags list if available.
    product_type = product.get("productType", "")
    description = product.get("descriptionHtml", "")
    tags = product.get("tags", [])
    # If tags is a list, join with commas; otherwise use empty string.
    tags_value = ",".join(tags) if isinstance(tags, list) else str(tags)
    status = product.get("status", "active")  # default status
    status = status.lower()=="active"


    # print("Inserting product:", new_product)
    #
    # prod_response = supabase.table("products").insert(new_product).execute()
    # print("Inserted product:", prod_response)



    # Insert images.
    all_images = []
    images_edges = product.get("images", {}).get("edges", [])
    if images_edges:
        for edge in images_edges:
            node = edge.get("node", {})
            all_images.append(node.get("src",''))

    else:
        all_images = ["https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"]



    # Insert each variant.
    all_variants = []
    variants_edges = product.get("variants", {}).get("edges", [])
    for variant_edge in variants_edges:
        variant = variant_edge["node"]
        full_variant_id = variant["id"]
        # Convert variant id string to int (if numeric part is convertible)
        variant_id_str = full_variant_id.split('/')[-1]
        try:
            variant_id = int(variant_id_str)
        except ValueError:
            variant_id = variant_id_str  # Fallback to string if conversion fails

        var_title = variant.get("title", "-")

        sku = variant.get("sku", "")
        # Convert price to float if possible.
        try:
            print(variant.get("price"))
            price = int(float(variant.get("price")))
        except (ValueError, TypeError):
            price = 0
        inventory_quantity = variant.get("inventoryQuantity", 0)

        new_variant = {
            "id": product_id,
            "title": title,
            "tags": tags_value,
            "images": all_images,
            "product_active": status,
            "inv_quantity": inventory_quantity,
            "sync_enable":True
        }
        prod_response = supabase.table("products").insert(new_variant).execute()
        print("Inserted product:", prod_response)
        break


def insert_product_variant_into_supabase(product):
    full_product_id = product["id"]
    pid = full_product_id.split('/')[-1]
    pid = int(pid)
    variants_edges = product.get("variants", {}).get("edges", [])
    for variant_edge in variants_edges:
        variant = variant_edge["node"]
        full_variant_id = variant["id"]
        # Convert variant id string to int (if numeric part is convertible)
        variant_id_str = full_variant_id.split('/')[-1]
        try:
            variant_id = int(variant_id_str)
        except ValueError:
            variant_id = 404  # Fallback to string if conversion fails
    
        var_title = variant.get("title", "-")

        # sku = variant.get("sku", "")
        # Convert price to float if possible.
        try:
            print(variant.get("price"))
            price = float(variant.get("price"))
        except (ValueError, TypeError):
            price = 0
        inventory_quantity = variant.get("inventoryQuantity", 0)
    
        new_variant = {
            "pid": pid,
            "vid": variant_id,
            "title": var_title,
            "retail_price": price,
            "b2b_price": price,
            "inv_quantity": inventory_quantity
        }
        prod_response = supabase.table("variants").insert(new_variant).execute()
        print("Inserted variant:", prod_response)
            
# ---------------------------
# Main process: Fetch from Shopify and insert into Supabase
# ---------------------------
def main():
    variables = {"first": 200, "after": None}
    payload = {"query": shopify_query, "variables": variables}
    has_next_page = True

    while has_next_page:
        try:
            response = requests.post(shopify_url, headers=shopify_headers, json=payload)
            response.raise_for_status()
            data = response.json()
            time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"Encountered error: {e}. Retrying in 60 seconds...")
            time.sleep(30)
            continue  # Retry on error

        products_edges = data["data"]["products"]["edges"]
        count =0
        for product_edge in products_edges:
            count = count+1
            if count == 285:
                break
            product = product_edge["node"]
            insert_product_into_supabase(product)
            insert_product_variant_into_supabase(product)
          
        break



        # Update pagination
        page_info = data["data"]["products"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        variables["after"] = page_info["endCursor"]
        payload["variables"] = variables

    print("Data insertion complete.")

if __name__ == "__main__":
    main()
