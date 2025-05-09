import asyncio
from logger import get_logger
import aiohttp

import os
import time

import aiohttp
import asyncio
import traceback
from supabase import create_client, Client
from dotenv import load_dotenv
from logger import get_logger

class Shopify:
  def __init__(self, shopify_store_name, access_token, api_version):
    self.ACCESS_TOKEN = access_token
    self.API_VERSION = api_version
    self.SHOPIFY_STORE = shopify_store_name
    self.URL = f"https://{self.SHOPIFY_STORE}.myshopify.com/admin/api/{self.API_VERSION}/graphql.json"
    self.HEADER = {
      "Content-Type": "application/json",
      "X-Shopify-Access-Token": self.ACCESS_TOKEN
    }
    
    self.logger = get_logger("Shopify.py")
    

  async def fetch_product_by_id(self, product_id: int):
    product_gid = f"gid://shopify/Product/{product_id}"
    
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
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session, \
                   session.post(self.URL, headers=self.HEADER, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        self.logger.warning(f"fetch_product_by_id :: {e}")
        return None
    
    if errs := data.get("errors"):
      self.logger.error(f"fetch_product_by_id::GraphQL errors: {errs}")  # optional
      return None
      
    return data.get("data", {}).get("product")
  
  async def send_graphql_mutation(self, mutation: str, variables: dict, receiver: str = "child"):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.post(
            self.URL,
            headers=self.HEADER,
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
      return result
    except Exception as err:
      self.logger.exception(str(err))
      return {}
  
    
  async def sync_product(self, p_id: int = 404, child_p_id: int = 404):
    product = await self.fetch_product_by_id(p_id)
    # print(product)
    query_params = self.parse_into_query_params(product, f"gid://shopify/Product/{child_p_id}")
    # query_params = parse_response_to_query(product, "gid://shopify/Product/8872805433568") #Update
    mutation = self.product_clone_update_mutation(child_p_id != 404)
    print(query_params)
    new_product = await self.send_graphql_mutation(mutation, query_params)
    return new_product
    # print(wow)
  
  async def update_product_status(child_p_id: int, status: bool = False) -> None:
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
  
  def parse_into_query_params(self, product: dict, child_p_id: str = None):
    # product = await fetch_product(product_gid)
    # print("Fetched product data:")
    
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
        "productOptions": [{"name": option["name"], 'values': [{"name": value} for value in option["values"]]} for
                           option in product["options"]],
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
    if child_p_id:
      query_values["identifier"]= {"id" : child_p_id}
    
    return query_values
  
  def product_clone_update_mutation(self, update: bool=True):
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
    
  # status Update
  def product_update_mutation(self):
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
  
  async def set_product_status(self, id: int = 404, status: str = "DRAFT"):
    mutation = self.product_update_mutation()
    query_params = {
      "id": f"gid://shopify/Product/{id}",
      "status": status
    }
    # query_params = parse_response_to_query(product, "gid://shopify/Product/8872805433568") #Update
    result = await self.send_graphql_mutation(mutation, query_params)
    self.logger.info(str(result))
  
  async def update_product(self, child_pid, product_data):
    mutation = self.product_clone_update_mutation()
    query_params = self.parse_into_query_params(product_data, f"gid://shopify/Product/{child_pid}")
    new_product = await self.send_graphql_mutation(mutation, query_params)
    return new_product
  
  async def create_product(self, parent_pid, product_data):
    mutation = self.product_clone_update_mutation(False) # False for creating Product
    query_params = self.parse_into_query_params(product_data)
    new_product = await self.send_graphql_mutation(mutation, query_params)
    return new_product
  
  async def make_new_customer(self, customer: dict):
    print("making new custoemr")
    mutation = """
    mutation CreateCustomer($input: CustomerInput!) {
      customerCreate(input: $input) {
        customer {
          id
          firstName
          lastName
          defaultEmailAddress{
            emailAddress
          }
          defaultPhoneNumber{
            phoneNumber
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    address = customer["default_address"]
    variables = {
      "input": {
        "firstName": customer["first_name"],
        "lastName": customer["last_name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "addresses": [
          {
            "address1": address["address1"],
            "phone": address["phone"],
            "city": address["city"],
            "country": address["country"],
            "zip": address["zip"],
            
          }
        ]
      }
    }
    payload = {"query": mutation, "variables": variables}


    try:
      timeout = aiohttp.ClientTimeout(total=5)
      async with aiohttp.ClientSession(timeout=timeout) as session, \
          session.post(self.URL, headers=self.HEADER, json=payload) as resp:
        resp.raise_for_status()
        data = await resp.json()
      
      return data["data"]["customerCreate"]["customer"]["id"]
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
      self.logger.warning(f"fetch_product_by_id :: {e}")
      return None
  
  async def process_customer(self, customer, phone_no=None):
    query = """
    query GetCustomersByContact(
    $first: Int = 100,
    $after: String,
    $filter: String!
    ) {
      customers(first: $first, after: $after, query: $filter) {
        pageInfo {
          hasNextPage
          endCursor
        }
            nodes {
        id
        firstName
        lastName
        createdAt
        defaultEmailAddress{
          emailAddress
        }
        defaultPhoneNumber{
          phoneNumber
        }

      }
      }
    }
    """
    variables = {
      "first": 5,
      "after": None,
    }
    filters = None
    mail = customer.get("email")
    phone = customer.get("phone")
    if mail:
      filters = f"email:{mail}"
    if phone:
      filters += " OR "
      filters += f"phone:{phone}"
    if phone_no:
      filters += " OR "
      filters += f"order. phone:{phone_no}"

    variables["filter"] = filters

    payload = {"query": query, "variables": variables}
    
    
    try:
      data = await self.send_graphql_mutation(query, variables, "Parent")
      data = data["data"]["customers"]["nodes"]

      for node in data:
        node_email = node["defaultEmailAddress"]["emailAddress"]
        node_phone_number = node["defaultPhoneNumber"]["phoneNumber"]
        if mail and node_email == mail:
          return node["id"]
        elif node_phone_number == phone and phone:
          return node["id"]
        elif node_phone_number == phone_no and phone_no:
          return node["id"]
      
      return self.make_new_customer(customer)
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
      self.logger.warning(f"process_customer :: {e}")
      return None
  
  def process_shipping_address(self, shipping_address: dict):
    return {
      "address1": shipping_address["address1"],
      "address2": shipping_address["address2"],
      "city": shipping_address["city"],
      "company": shipping_address["company"],
      "countryCode": shipping_address["country_code"],
      "firstName": shipping_address["first_name"],
      "lastName": shipping_address["last_name"],
      "phone": shipping_address["phone"],
      "provinceCode": shipping_address["province_code"],
      "zip": shipping_address["zip"],
    }
  
  
  def draft_order_mutation(self):
    return """
      mutation draftOrderCreate($input: DraftOrderInput!) {
        draftOrderCreate(input: $input) {
          draftOrder {
            id
            name
          }
        }
      }
      """