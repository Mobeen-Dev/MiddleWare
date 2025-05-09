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
#
# # Run the asynchronous main function
# if __name__ == '__main__':
#     asyncio.run(main())

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
SHOPIFY_STORE = os.getenv("CHILD_SHOPIFY_STORE_NAME")
ACCESS_TOKEN  = os.getenv("CHILD_SHOPIFY_API_SECRET")
API_VERSION   = "2025-07"  # adjust if needed

if not SHOPIFY_STORE or not ACCESS_TOKEN:
    raise RuntimeError("Set PARENT_SHOPIFY_STORE_NAME and PARENT_SHOPIFY_API_SECRET in your .env")

GRAPHQL_ENDPOINT = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# The ProductCopy mutation
PRODUCT_COPY_MUTATION = """
mutation ProductCopy($input: ProductSetInput!, $synchronous: Boolean!, $identifier: ProductSetIdentifiers!) {
  productSet(input: $input, synchronous: $synchronous, identifier: $identifier) {
    product {
      id
      variants(first: 2) {
        edges {
          node {
            id
            sku
            price
            inventoryPolicy
            inventoryItem {
              tracked
            }
          }
        }
      }
    }
    productSetOperation {
      id
      status
      userErrors {
        code
        field
        message
      }
    }
    userErrors {
      code
      field
      message
    }
  }
}
"""
async def product_copy(variables: dict) -> dict:
    """
    Executes the ProductCopy mutation with the given variables.
    Returns the parsed 'productSet' dict on success.
    Raises RuntimeError on any GraphQL or userError.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            GRAPHQL_ENDPOINT,
            headers=HEADERS,
            json={"query": PRODUCT_COPY_MUTATION, "variables": variables}
        ) as resp:
            resp.raise_for_status()
            result = await resp.json()

    # 3. Top-level GraphQL errors
    if "errors" in result:
        raise RuntimeError(f"GraphQL errors: {result['errors']}")

    data = result.get("data")
    if not data:
        raise RuntimeError(f"No 'data' field in response: {result}")

    ps = data.get("productSet")
    if ps is None:
        # Could be completely null if the mutation itself wasn't found, or input invalid
        raise RuntimeError(f"No 'productSet' returned in response: {result}")

    # 4. Collect userErrors on the root and operation
    root_errors = ps.get("userErrors") or []
    op = ps.get("productSetOperation") or {}
    op_errors = op.get("userErrors") or []

    if root_errors or op_errors:
        raise RuntimeError(f"User errors: {root_errors + op_errors}")

    # 5. Success — return the productSet payload
    return ps


async def main2():
    # Example dynamic variables; replace with your actual input
    variables = {'synchronous': True, 'identifier': {'id': "gid://shopify/Product/8872805433568"}, 'input': {'title': 'Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger Ultrasonic Mist Maker Fogger Humidifier', 'descriptionHtml': '<p><span>This <strong>Ultrasonic Mist Maker Fogger </strong>has\xa0required no heat or chemicals used. This <strong>best mist maker</strong>\xa0with 12 LED colourful light. <strong>12 LED ultrasonic mist maker fogger </strong>is e</span><span>asy to operate, long service life, self-protective. This<strong> mist maker fogger water fountain </strong>i</span><span>deal for indoor or outdoor fountains, water feature, and office.\xa0This\xa0<strong>ultrasonic humidity\xa0maker </strong>adds</span><span>\xa0a stunning mist effect to your pond or water tank to filter the bad smell with electro and ultrasonic technology. This <strong>mist machine</strong> is a beautiful gift for your friends and family.\xa0</span><span></span></p>\n<p><span>We have also\xa0<bdi><a title="Ultrasonic mist maker fogger 12 led colorful light 1a 24v humidifier in pakistan – digilog.pk" href="/products/ultrasonic-mist-maker-fogger-12-led-colorful-light-1a-24v-in-pakistan" target="_blank" data-mce-href="/products/ultrasonic-mist-maker-fogger-12-led-colorful-light-1a-24v-in-pakistan" aria-label="Visit a webpage about Ultrasonic mist maker fogger 12 led colorful light 1a 24v humidifier in pakistan – digilog.pk">Ultrasonic Humidifiers With Cotton Swab</a>,\xa0<a href="https://hallroad.org/mini-usb-water-float-donuts-shape-humidifier-air-diffuser-mist-maker-moisture-air-in-pakistan.html" target="_blank" data-mce-href="https://hallroad.org/mini-usb-water-float-donuts-shape-humidifier-air-diffuser-mist-maker-moisture-air-in-pakistan.html">Air Diffuser Mist Maker Moisture Air</a>\xa0etc.</bdi></span></p>\n<h2><strong>Features Of\xa0Ultrasonic Mist Maker ;</strong></h2>\n<ul>\n<li><span>100% brand new, high quality.</span></li>\n<li><span>Perfect and meticulous, exquisite workmanship and first-class quality.</span></li>\n<li><span>Whether it is for your own use or for a friend, it is a good gift.</span></li>\n<li><span>No heat or chemicals used. Adopt the principle of Electronic high-frequency oscillation.</span></li>\n<li><span>Fogger contains a larger number of air negative ions and can increase the humidity of the air, making the air fresher!</span></li>\n<li><span>With 12 LED colourful light. Easy to operate, long service life, self-protection</span></li>\n</ul>\n<h2><strong>Specifications Of Best Mist Maker Fogger Water Fountain:</strong></h2>\n<ol>\n<li><span><strong>Power: </strong>24V 2A\xa0(need to 24V power supply)</span></li>\n<li><span><strong>Cable length:</strong> 136 cm</span></li>\n<li><span><strong>Round thing height: </strong>2.5cm</span></li>\n<li><span><strong>Body Material: </strong>ABS</span></li>\n<li><span><strong>Light Source: </strong>LED Bulbs</span></li>\n<li><span><strong>Item Type:</strong> Underwater Lights</span></li>\n</ol>\n<h2><strong>Instructions:</strong></h2>\n<ol>\n<li><span>Do not turn over the Mist Maker When the switch is turned on, keep upright, or it may damage the atomizer.</span></li>\n<li><span>Please ensure that the daily running time is less than 10 hours, otherwise, the life of atomizing slice will be shorted.</span></li>\n<li><span>Don\'t touch the atomizing slice while the Mist Maker is working.</span></li>\n<li><span>Ensure the water at high quality, use clean tap water. (water quality deterioration may influence the lifetime)</span></li>\n<li><span>Please switch off the power before Movement or maintenance.</span></li>\n<li><span>The atomizing slice is consumable, and its service life is≥3000 hours. If marked reduction of Mist present, please clean atomizing slice with a cotton swab(don\'t need to use any detergent).</span></li>\n<li><span>If marked reduction of Mist still presents after cleaning, please change a new atomizing slice. (Recommend to buy another atomizing transducer slice)</span></li>\n</ol>\n<h2>\n<span></span><strong>Package Includes:</strong>\n</h2>\n<ul>\n<li>\n<span>1 x\xa012 LED ultrasonic mist maker fogger</span><span></span>\n</li>\n<li>1 x 24v Power Supply (USED)</li>\n</ul>\n<h2>Note:</h2>\n<p>Power Supply/Addapter shape might be different as shown in pictures and scratches on its body guarentee of working</p>\n<p><span>Best Online Shopping website for Ultrasonic Mist Maker Fogger 12 LED Colorful Light 2A 24V in cheap price in Karachi, Lahore, Islamabad, Rawalpindi, Sukkur, Peshawar, Multan, Quetta, Faisalabad and all over Pakistan.</span></p>\n<p><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"></p>\n<p><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"></p>\n<p><img src="/products/aquarium-garden-pond-mist-maker-humidifier-ultrasonic-fogger-ultrasonic-mist-maker-fogger-humidifier-1" data-mce-src="https://hallroad.digilog.pk/images/watermarked/detailed/24/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__5_.jpg"><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"><img loading="lazy" alt="Aquarium Garden Pond Mist Maker Humidifier Ultrasonic Fogger" data-original="https://cdn.shopify.com/s/files/1/0744/0764/1366/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.jpg" src="https://digilog.pk/cdn/shop/files/Ultrasonic-Mist-Maker-Fogger-12-LED-Colorful-Light-1A-24V-In-Lahore-Karachi-Islamabad-Peshawar-Quetta-Mardan-Multan.webp"></p>', 'vendor': 'Digilog.pk', 'productType': '', 'handle': 'aquarium-garden-pond-mist-maker-humidifier-ultrasonic-fogger-ultrasonic-mist-maker-fogger-humidifier-1', 'tags': ['12 LED Colorful Light', 'Fogger Purify', 'humidifier', 'inv ok', 'kh', 'sea', 'Ultrasonic Mist Maker', 'Water Fountain'], 'status': 'ACTIVE', 'files': [{'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/mist_maker_b106d0eb-6cae-418b-aec8-5dc3df58a47e.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__8_bae618d6-48c4-4dd5-b2fa-6d7eb05834dc.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__7_00093c94-d3df-46ea-b4fc-37a11e04955b.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__9_d28cd0f5-04b9-492e-8f25-b54bc24873b8.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__6_2ca228f7-eccb-47f4-934b-e87f7d8792f2.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__4_e99e67aa-b641-4fed-af7a-e93dc22b0a8b.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__3_7843e45f-cad6-4a5d-8a85-9416a9bdaa70.webp'}, {'filename': '1.webp', 'alt': 'Product image', 'contentType': 'IMAGE', 'duplicateResolutionMode': 'APPEND_UUID', 'originalSource': 'https://cdn.shopify.com/s/files/1/0559/7832/8150/files/Ultrasonic_Mist_Maker_Fogger_12_LED_Colorful_Light_1A_24V_In_Lahore_Karachi_Islamabad_Peshawar_Quetta_Mardan_Multan_Sibbi_Pakistan__1_21ea6a52-1eda-4533-8e55-f4fe84d7cab5.webp'}], 'productOptions': [{'name': 'Title', 'values': [{'name': 'Default Title'}]}], 'variants': [{'optionValues': [{'optionName': 'Title', 'name': 'Default Title'}], 'sku': '', 'price': '1450.00', 'compareAtPrice': None, 'inventoryPolicy': 'DENY', 'taxable': False, 'inventoryQuantities': [{'locationId': 'gid://shopify/Location/82558976224', 'name': 'available', 'quantity': 0}], 'inventoryItem': {'tracked': True, 'requiresShipping': True, 'measurement': {'weight': {'value': 0.0, 'unit': 'KILOGRAMS'}}}}]}}

    try:
        result = await product_copy(variables)
        print("Mutation succeeded. Result:")
        print(result)
    except Exception as e:
        print(f"Error during ProductCopy mutation:\n{e}")

if __name__ == "__main__":
    asyncio.run(main2())
