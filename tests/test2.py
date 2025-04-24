import os
import asyncio
import aiohttp
from dotenv import load_dotenv

async def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve environment variables
    SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
    ACCESS_TOKEN = os.getenv("PARENT_SHOPIFY_API_SECRET")
    API_VERSION = "2025-01"  # Using the version provided in your sample

    if not SHOPIFY_STORE or not ACCESS_TOKEN:
        raise ValueError("Please set SHOPIFY_STORE_NAME and SHOPIFY_API_SECRET in your .env file.")

    # Build the API endpoint URL for Shopify GraphQL
    url = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{API_VERSION}/graphql.json"

    # Prepare headers for the request
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }

    # GraphQL query to fetch products data
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
    payload = {"query": query, "variables": variables}

    all_products = []
    has_next_page = True

    # Use aiohttp ClientSession to make asynchronous calls
    async with aiohttp.ClientSession() as session:
        while has_next_page:
            try:
                async with session.post(url, headers=headers, json=payload) as resp:
                    # Raise exception for non-200 responses
                    resp.raise_for_status()
                    data = await resp.json()
                    print(data)
                    # Wait for 2 seconds asynchronously to throttle requests
                    await asyncio.sleep(0.5)
            except aiohttp.ClientError as e:
                print(f"Encountered error: {e}. Retrying in 60 seconds...")
                await asyncio.sleep(60)
                continue  # Retry the request after the delay

            # Process the products data from the response
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
                        # Adjust the URL format as needed for your store
                        "product_link": f"https://{SHOPIFY_STORE}.myshopify.com/products/{product['handle']}",
                        "var_id": variant['id'].split('/')[-1]
                    })

            # Update pagination variables based on response
            page_info = data['data']['products']['pageInfo']
            has_next_page = page_info['hasNextPage']
            variables['after'] = page_info['endCursor']
            payload['variables'] = variables

    print(f"Length of orders = {len(all_products)}")

# Run the asynchronous main function
if __name__ == '__main__':
    asyncio.run(main())
