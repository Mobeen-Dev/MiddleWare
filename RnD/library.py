import os
import time
import aiohttp
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv
from logger import get_logger
logger = get_logger("Library")

##############################
#  <   Helper Functions   >  #
##############################

def parse_into_query_params(product:dict, child_p_id:str=""):
    # product = await fetch_product(product_gid)
    # print("Fetched product data:")
    # print(product)
    def handle_variants(vary_items):
        variants = vary_items.split(" / ")
        variant_list = []
        
        for variant in variants:
            parent_variant = [option["name"] for option in product["options"] if variant in option.get("values", [])]
            opt = {"optionName": parent_variant[0], "name": variant}
            variant_list.append(opt)
            # {"optionName": product["options"][1]["name"], "name": variant["node"]["title"].split(' / ')[1]},
        
        return variant_list
    
    variants = product.get("variants").get("edges")
    images = product["media"]["edges"]
    variant_option = None
    query_values = {
        "synchronous": True,
        "identifier":{
            "id": child_p_id,
        },
        "input": {
            "title": product["title"],
            "descriptionHtml": product["descriptionHtml"],
            "vendor": product["vendor"],
            "productType": product["productType"],
            "handle": product["handle"],
            "tags": product["tags"],
            "status": product["status"],

            "files": [
                {
                    "filename": f"1.{image["node"]["image"]["url"].split("?", 1)[0].rpartition(".")[2]}",
                    "alt": "Product image",
                    "contentType": "IMAGE",
                    "duplicateResolutionMode": "APPEND_UUID",
                    "originalSource": image["node"]["image"]["url"].split("?", 1)[0]
                }
                for image in images
            ],
            # "productOptions":product["options"],
            "productOptions": [ {"name": option["name"], 'values':[{ "name": value }for value in option["values"]]}for option in product["options"]],
            "variants": [
                {
                    "optionValues": handle_variants(variant["node"]["title"]),

                    "sku": variant["node"]["sku"],
                    "price": variant["node"]["price"],
                    "compareAtPrice": variant["node"]["compareAtPrice"],
                    "inventoryPolicy": variant["node"]["inventoryPolicy"],
                    "taxable": False,

                    "inventoryQuantities": [
                        {
                            "locationId": "gid://shopify/Location/82558976224",
                            "name": "available",
                            "quantity": variant["node"]["inventoryQuantity"],
                        }
                    ],
                    "inventoryItem": {
                        "tracked": variant["node"]["inventoryItem"]["tracked"],
                        # "cost": 12.34,
                        "requiresShipping": variant["node"]["inventoryItem"]["requiresShipping"],
                        "measurement": variant["node"]["inventoryItem"]["measurement"],
                    }
                }
                for variant in variants
            ]


        }
    }

    return query_values

def product_clone_update_mutation(update:bool):
    if update:
        return """
          mutation ProductCopy($input: ProductSetInput!, $synchronous: Boolean!, $identifier: ProductSetIdentifiers!) {
            productSet(input: $input, synchronous: $synchronous, identifier: $identifier) {
              product {
                id
                variants(first: 249) {
                  edges {
                    node {
                      title
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
    else:
        return """
          mutation ProductCopy($input: ProductSetInput!, $synchronous: Boolean!) {
            productSet(input: $input, synchronous: $synchronous) {
              product {
                id
                variants(first: 249) {
                  edges {
                    node {
                      title
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
    
def product_update_mutation():
    return """
    mutation UpdateProductStatus($id: ID!, $status: ProductStatus!) {
      productSet(
        identifier: { id: $id }
        input: { status: $status }
        synchronous: true
      ) {
        product {
          id
          title
          status
        }
        userErrors {
          field
          message
        }
      }
    }
    """

async def fetch_product_by_id(product_id: int):
    product_gid = f"gid://shopify/Product/{product_id}"
    load_dotenv()
    SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
    ACCESS_TOKEN = os.getenv("PARENT_SHOPIFY_API_SECRET")
    API_VERSION = "2025-01"
    if not SHOPIFY_STORE or not ACCESS_TOKEN:
        raise ValueError("Set PARENT_SHOPIFY_STORE_NAME and PARENT_SHOPIFY_API_SECRET in .env")
    
    url = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{API_VERSION}/graphql.json"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    
    # Use the complete query from above
    query = """
    query GetProductById($id: ID!) {
      product(id: $id) {
        id
        title
        handle
        description
        descriptionHtml
        vendor
        productType
        status
        createdAt
        updatedAt
        tags
        options {
          name
          values
        }
        priceRange {
          minVariantPrice {
            amount
            currencyCode
          }
          maxVariantPrice {
            amount
            currencyCode
          }
        }
        compareAtPriceRange {
          minVariantCompareAtPrice {
            amount
            currencyCode
          }
          maxVariantCompareAtPrice {
            amount
            currencyCode
          }
        }
        totalInventory
        variants(first: 249) {
          edges {
            node {
              id
              title
              sku
              taxable
              price
              compareAtPrice
              inventoryQuantity
              availableForSale
              barcode
              createdAt
              updatedAt
              inventoryPolicy
              inventoryItem {
                id
                tracked
                measurement {
                  weight {
                    value
                    unit
                  }
                }
                unitCost {
                  amount
                  currencyCode
                }
                countryCodeOfOrigin
                harmonizedSystemCode
                requiresShipping
              }
              image {
                width
                height
                id
                altText
                url
                width
                height
              }
            }
          }
        }
        images(first: 50) {
          edges {
            node {
              id
              altText
              url
              width
              height
            }
          }
        }
        media(first: 20) {
          edges {
            node {

              ... on MediaImage {
                image {
                  id
                  altText
                  url
                  width
                  height
                }
              }
            }
          }
        }


      }
    }

    """
    variables = {"id": product_gid}
    payload = {"query": query, "variables": variables}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            result = await resp.json()
            if errors := result.get("errors"):
                raise RuntimeError(f"GraphQL errors: {errors}")
            return result["data"]["product"]

async def send_graphql_mutation(mutation:str, variables: dict, receiver:str="child"):
    """
       Executes the ProductCopy mutation with the given variables.
       Returns the parsed 'productSet' dict on success.
       Raises RuntimeError on any GraphQL or userError.
    """
    load_dotenv()
    if receiver == "child":
        SHOPIFY_STORE = os.getenv("CHILD_SHOPIFY_STORE_NAME")
        ACCESS_TOKEN = os.getenv("CHILD_SHOPIFY_API_SECRET")
        API_VERSION = os.getenv("CHILD_SHOPIFY_API_VERSION")
    else:
        SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
        ACCESS_TOKEN = os.getenv("PARENT_SHOPIFY_API_SECRET")
        API_VERSION = os.getenv("PARENT_SHOPIFY_API_VERSION")

    if not SHOPIFY_STORE or not ACCESS_TOKEN:
        raise RuntimeError("Set PARENT_SHOPIFY_STORE_NAME and PARENT_SHOPIFY_API_SECRET in your .env")

    GRAPHQL_ENDPOINT = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{API_VERSION}/graphql.json"
    HEADERS = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": ACCESS_TOKEN
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                GRAPHQL_ENDPOINT,
                headers=HEADERS,
                json={"query": mutation, "variables": variables}
            ) as resp:
                resp.raise_for_status()
                result = await resp.json()
    
        # 3. Top-level GraphQL errors
        if "errors" in result:
            raise RuntimeError(f"GraphQL errors: {result['errors']}")
    
        data = result.get("data")
        if not data:
            raise RuntimeError(f"No 'data' field in response: {result}")
        if receiver == "child":
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
    except Exception as err:
        logger.exception(str(err))
        return {}
    
async def sync_product(p_id:int=404, child_p_id:int=404):
    product = await fetch_product_by_id(p_id)
    # print(product)
    query_params = parse_into_query_params(product, f"gid://shopify/Product/{child_p_id}")
    # query_params = parse_response_to_query(product, "gid://shopify/Product/8872805433568") #Update
    mutation = product_clone_update_mutation(child_p_id != 404)
    print(query_params)
    new_product = await send_graphql_mutation(mutation, query_params)
    return new_product
    # print(wow)

async def update_product_in_db(parent_p_id: int, product: dict) -> None:
    # 1. Load credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in .env")
    # 2. Initialize sync client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)  # :contentReference[oaicite:0]{index=0}

    # 3. Offload the blocking update to a thread
    child_p_id = int(product["product"]["id"].split('/')[-1])
    response = (
        supabase.table("products")
        .update({"child_id": child_p_id})
        .eq("id", parent_p_id)
        .execute()
    )
    variants = product["product"]["variants"]["edges"]
    for variant_json in variants:
        variant = variant_json["node"]
        variant_vid = variant["id"]
        variant_vid = int(variant_vid.split('/')[-1])
        variant_title = variant["title"]
        response = (
            supabase.table("variants")
            .update({"child_vid": variant_vid})
            .eq("pid", parent_p_id)
            .eq("title", variant_title)
            .execute()
        )
        if parent_p_id == 6960937467990:
            print(response)
        time.sleep(1)

async def sync_db_product():
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in .env")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    BATCH_SIZE = 200
    offset = 0
    # try:
                    # Round 1 - Updates and SyncedEnabled Products & create if not already present
    
    while True:
        start = offset
        end = offset + BATCH_SIZE - 1

        resp = (
            supabase
            .table("products")
            .select("*")
            .eq("sync_enable", True)
            .order("id", desc=False)  # ascending
            # .gt("retail_price", 1000)
            .range(start, end)
            .execute()
        )

        batch = resp.data or []
        if not batch:
            # no more rows
            break

        ids = [(row["id"], row["child_id"]) for row in batch]
        logger.info(f"Fetched IDs {start}–{end}")

                    # ----- your processing goes here -----
        for id, child_id in ids:
            if not child_id :
                product = await sync_product(id)
                print("@@@\n\n")
                print(product)
                if product :
                    await update_product_in_db(id, product)
            elif child_id :
                pass
                # await sync_product(id, child_id)
                # pid = int(product["product"]["id"].split('/')[-1])
                # update_product_in_db(id, pid)
                # print(product)

            # product = await sync_product(id)
            # pid = int(product["product"]["id"].split('/')[-1])
            update_product_in_db(id, pid)
            # print(product)

                    # Round 2  - Check for Active but DeSynced Products
        # ---------------------------------------

        offset += BATCH_SIZE


                    # Round 2  - Check for Active but DeSynced Products

    # while True:
    #     start = offset
    #     end = offset + BATCH_SIZE - 1
    #     # query to get those child_ids which are unsynced but active in store
    #     resp = (
    #         supabase
    #         .table("products")
    #         .select("*")
    #         .eq("sync_enable", False)
    #         .eq("isActive", True)
    #         .order("id", desc=False)  # ascending
    #         # .gt("retail_price", 1000)
    #         .range(start, end)
    #         .execute()
    #     )
    #
    #     batch = resp.data or []
    #     if not batch:
    #         # no more rows
    #         break
    #
    #     ids = [row["child_id"] for row in batch]
    #     add_log(f"Fetched IDs {start}–{end}:" + str(ids))
    #
    #     # ----- your processing goes here -----
    #     for child_id in ids:
    #         if child_id:
    #             await set_product_status(child_id)
    #             await update_product_status(child_id)
    #             # how to deactivate the product
    #
    #
    #
    #     # ---------------------------------------
    #
    #     offset += BATCH_SIZE
      
    # except Exception as err:
    #     logger.exception(str(err))
    
async def set_product_status(id:int=404, status:str="DRAFT"):
    mutation = product_update_mutation()
    query_params = {
      "id": f"gid://shopify/Product/{id}",
      "status": status
    }
    # query_params = parse_response_to_query(product, "gid://shopify/Product/8872805433568") #Update
    result = await send_graphql_mutation(mutation, query_params)
    print(result)
    
async def update_product_status(child_p_id: int, status:bool=False) -> None:
    # 1. Load credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in .env")

    # 2. Initialize sync client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)  # :contentReference[oaicite:0]{index=0}

    # 3. Offload the blocking update to a thread
    response = await asyncio.to_thread(
        lambda: supabase.table("products")
                        .update({"isActive": status})
                        .eq("child_id", child_p_id)
                        .execute()
    )  # :contentReference[oaicite:1]{index=1}

    # 4. Handle result
    # print(response)
    
##############################
#  <  Services Function  >   #
##############################









if __name__ == "__main__":
    # asyncio.run(sync_product(7476055474262))
    asyncio.run(sync_db_product())
