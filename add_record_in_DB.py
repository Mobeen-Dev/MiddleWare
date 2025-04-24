# import os
# from dotenv import load_dotenv
# from supabase import create_client, Client
#
# # Load environment variables from the .env file
# load_dotenv()
#
# # Retrieve the Supabase URL and API key from the environment
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
#
# # Initialize the Supabase client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
#
#
# def main():
#     # --- 1. Create (Insert) ---
#     print("Inserting a new record...")
#     # Define the record you want to insert
#     new_record = {
#         "name": "Item 1+1",
#         "description": "This is the first item"
#     }
#     response = supabase.table("items").insert(new_record).execute()
#
#     print("Inserted Data:", response.data)
#
#     # Capture the inserted item's ID (assuming your table has a primary key column named 'id')
#     inserted_id = response.data[0]['id']
#
#     # --- 2. Read (Retrieve) ---
#     print("\nRetrieving records...")
#     response = supabase.table("items").select("*").execute()
#
#
#     # --- 3. Update (Alter) ---
#     print("\nUpdating the inserted record...")
#     update_record = {
#         "name": "Updated Item 1",
#         "description": "Updated description"
#     }
#     response = supabase.table("items").update(update_record).eq("id", inserted_id).execute()
#
#     print("Updated Data:", response.data)
#
#     # --- 4. Delete ---
#     # print("\nDeleting the updated record...")
#     # response = supabase.table("items").delete().eq("id", inserted_id).execute()
#     #
#     # print("Deleted Record:", response.data)
#
#
# if __name__ == "__main__":
#     main()



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
        variants(first: 100) {
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

    new_product = {
        "product_id": product_id,
        "title": title,
        "product_type": product_type,
        "description": description,
        "tags": tags_value,
        "status": status
    }
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
        # Replace default titles with hyphen.
        if var_title in ["Default Title", "Default"]:
            var_title = "-"
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
            "retail_price": price,
            "b2b_price": price,
            "sync_enable": True,
            "inv_quantity": inventory_quantity
        }
        prod_response = supabase.table("products").insert(new_variant).execute()
        print("Inserted product:", prod_response)
        break

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
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"Encountered error: {e}. Retrying in 60 seconds...")
            time.sleep(60)
            continue  # Retry on error

        products_edges = data["data"]["products"]["edges"]
        for product_edge in products_edges:
            product = product_edge["node"]
            insert_product_into_supabase(product)

        # Update pagination
        page_info = data["data"]["products"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        variables["after"] = page_info["endCursor"]
        payload["variables"] = variables

    print("Data insertion complete.")

if __name__ == "__main__":
    main()
