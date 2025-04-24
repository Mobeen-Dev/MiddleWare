
import os
import time

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
ACCESS_TOKEN = os.getenv("PARENT_SHOPIFY_API_SECRET")
API_VERSION = "2025-01"  # using the version provided in the sample

if not SHOPIFY_STORE or not ACCESS_TOKEN:
    raise ValueError("Please set SHOPIFY_STORE_NAME and SHOPIFY_ACCESS_TOKEN in your .env file.")
print(SHOPIFY_STORE, ACCESS_TOKEN)
# Build the API endpoint URL
url = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{API_VERSION}/graphql.json"

# Prepare headers
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Construct the GraphQL query for the three most recent products
query = """
        query ($first: Int!, $after: String) {
            products(first: $first, after: $after) {
                edges {
                    cursor
                    node {
                        id
                        title
                        handle
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
                        images(first: 1) {
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
variables = {
            'first': 200,
            'after': None
        }
# Prepare the JSON payload
payload = {"query": query, 'variables': variables}

all_products = []
has_next_page = True

while has_next_page:
    try:
        # Make the HTTP POST request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data)
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(f"Encountered error: {e}. Retrying in 60 seconds...")
        time.sleep(60)
        continue  # Retry the request after the delay

    products = data['data']['products']['edges']
    for product_edge in products:
        product = product_edge['node']
        product_id = product['id'].split('/')[-1]
        # Use a valid placeholder image if there are no images.
        if product['images']['edges']:
            image_src = product['images']['edges'][0]['node']['src']
        else:
            image_src = "https://via.placeholder.com/150?text=No+Image"

        for variant_edge in product['variants']['edges']:
            variant = variant_edge['node']
            var_title = variant['title'] if variant['title'] not in ["Default Title", "Default"] else "-"
            all_products.append({
                "img_path": image_src,
                "product_id": product_id,
                "title": product['title'],
                "var_title": var_title,
                "stock": variant.get('inventoryQuantity', 0),
                "costprice": variant.get('price', 'N/A'),
                "sku": variant.get('sku', 'N/A'),
                "product_link": f"https://STORE/products/{product['handle']}",
                "var_id": variant['id'].split('/')[-1]
            })

    page_info = data['data']['products']['pageInfo']
    has_next_page = page_info['hasNextPage']
    variables['after'] = page_info['endCursor']

# Extract the product edges and print the product ID and title
print(f"Length of orders = {len(all_products)}")