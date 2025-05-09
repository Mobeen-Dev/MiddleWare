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
mutation draftOrderCreate($input: DraftOrderInput!) {
  draftOrderCreate(input: $input) {
    draftOrder {
      id
      name
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
# Function to parse order webhook
# ---------------------------
def fetch_parent_variants(child_ids: list[int]) -> list[tuple[ [int], [float] ] ]:
  """
  Returns a list of (vid, retail_price) tuples corresponding to each child_id
  in child_ids. If a child_id isn’t found or an error occurs, returns (None, None).
  """
  # 1) Do one big query
  resp = (
    supabase
    .table("variants")
    .select("child_vid, vid, retail_price")
    .in_("child_vid", child_ids)
    .execute()
  )

  # if resp.error:
  #   raise RuntimeError(f"Supabase error: {resp.error.message}")
  
  # 2) Build a lookup by child_vid
  lookup = {
    row["child_vid"]: (row["vid"], row["retail_price"])
    for row in resp.data
  }
  
  # 3) Return results in the same order as child_ids
  return [lookup.get(cid, (None, None)) for cid in child_ids]
def fetch_parent_variant_id(id):
    resp = (
      supabase
      .table("variants")
      .select("*")
      .eq("child_vid",int(id))
      .execute()
    )
    
    # if resp.error:
    #   print(f"❌ Error: {resp.error.message}")
    #   return 41219660382294, 4.04
    print(resp)
    
    row:dict = resp.data[0]
    return row["vid"], row["retail_price"]


def make_new_customer(customer:dict):
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
    response = requests.post(shopify_url, headers=shopify_headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["data"]["customerCreate"]["customer"]["id"]
 
  except requests.exceptions.RequestException as e:
    print(f"Encountered error: {e}. Retrying in 60 seconds...")
    time.sleep(30)




def process_customer(customer, phone_no):
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
    filters += f"phone:{phone_no}"
  print(filters)
  variables["filter"] = filters
  print()
  payload = {"query": query, "variables": variables}
  
  try:
    response = requests.post(shopify_url, headers=shopify_headers, json=payload)
    response.raise_for_status()
    data = response.json()
    data =  data["data"]["customers"]["nodes"]
    id = None
    for node in data:
      node_email = node["defaultEmailAddress"]["emailAddress"]
      node_phone_number = node["defaultPhoneNumber"]["phoneNumber"]
      if mail and node_email == mail:
        return node["id"]
      elif node_phone_number == phone and phone:
        return node["id"]
      elif node_phone_number == phone_no and phone_no:
        return node["id"]
      
    return make_new_customer(customer)
    
  except requests.exceptions.RequestException as e:
    print(f"Encountered error: {e}. Retrying in 60 seconds...")
    time.sleep(30)
    



def process_line_items(line_items:list):
  updated_line_items = []
  total_bill = 0
  item_ids = [item['variant_id'] for item in line_items]
  parent_variants = fetch_parent_variants(item_ids)
  for idx, (vid, price) in enumerate(parent_variants):
    # print(f"Item #{idx}: first={vid}, second={price}")
    v_id = f"gid://shopify/ProductVariant/{vid}"
    qty = line_items[idx]["quantity"]
    total_bill += price * qty
    updated_line_items.append({
      "variantId": v_id,
      "quantity": qty,
    })
  # for item in line_items:
  #   # child_v_id = f"gid://shopify/ProductVariant/{item['variant_id']}"
  #   child_v_id = item['variant_id']
  #   id, price = fetch_parent_variant_id(child_v_id)
  #   id = f"gid://shopify/ProductVariant/{id}"
  #   total_bill += price*item["quantity"]
  #   updated_line_items.append({
  #     "variantId": id,
  #     "quantity": item["quantity"],
  #   })
  return updated_line_items, total_bill

def process_shipping_address(shipping_address:dict):
  return {
  "address1" : shipping_address["address1"],
  "address2": shipping_address["address2"],
  "city": shipping_address["city"],
  "company": shipping_address["company"],
  "countryCode": shipping_address["country_code"],
  "firstName":  shipping_address["first_name"],
  "lastName": shipping_address["last_name"],
  "phone": shipping_address["phone"],
  "provinceCode":shipping_address["province_code"],
  "zip": shipping_address["zip"],
  }

def parse_order_webhook(order_webhook: dict ):
  customer = order_webhook["customer"]
  line_items = order_webhook["line_items"]
  order_note = f"Order: {order_webhook["name"]}\n LineItems Price:{order_webhook['total_line_items_price']}"
  
  shipping_address = process_shipping_address(order_webhook["shipping_address"])
  billingAddress = order_webhook["billing_address"]
  email = order_webhook["email"]
  phone = order_webhook["phone"]
  line_items, total_bill = process_line_items(line_items)
  variables = {
    "input": {
      "customerId": process_customer(customer),
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
    
  return variables
  
  



# ---------------------------
# Main process: Fetch from Shopify and insert into Supabase
# ---------------------------
def main():
  webhook = {
        "id": 6103715840224,
        "admin_graphql_api_id": "gid://shopify/Order/6103715840224",
        "app_id": 1354745,
        "browser_ip": "103.125.177.132",
        "buyer_accepts_marketing": False,
        "cancel_reason": None,
        "cancelled_at": None,
        "cart_token": None,
        "checkout_id": 35828845412576,
        "checkout_token": "243412f124c643cac6c2b219ccd71195",
        "client_details": {
          "accept_language": None,
          "browser_height": None,
          "browser_ip": "103.125.177.132",
          "browser_width": None,
          "session_hash": None,
          "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        },
        "closed_at": None,
        "company": None,
        "confirmation_number": "QLHZRZN8M",
        "confirmed": True,
        "contact_email": "first.customer@ollaya.com",
        "created_at": "2025-05-01T00:57:48-04:00",
        "currency": "PKR",
        "current_shipping_price_set": {
          "shop_money": {
            "amount": "1235.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "1235.00",
            "currency_code": "PKR"
          }
        },
        "current_subtotal_price": "79670.00",
        "current_subtotal_price_set": {
          "shop_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          }
        },
        "current_total_additional_fees_set": None,
        "current_total_discounts": "0.00",
        "current_total_discounts_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "current_total_duties_set": None,
        "current_total_price": "80905.00",
        "current_total_price_set": {
          "shop_money": {
            "amount": "80905.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "80905.00",
            "currency_code": "PKR"
          }
        },
        "current_total_tax": "0.00",
        "current_total_tax_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "customer_locale": "en",
        "device_id": None,
        "discount_codes": [],
        "duties_included": False,
        "email": "first.customer@ollaya.com",
        "estimated_taxes": False,
        "financial_status": "paid",
        "fulfillment_status": None,
        "landing_site": None,
        "landing_site_ref": None,
        "location_id": None,
        "merchant_business_entity_id": "MTc1MjEyOTQ3Njgw",
        "merchant_of_record_app_id": None,
        "name": "-\u003E1003",
        "note": None,
        "note_attributes": [],
        "number": 3,
        "order_number": 1003,
        "order_status_url": "https://ollaya.myshopify.com/75212947680/orders/780f1ba2885319d53940a5e989b7d4c6/authenticate?key=de4c02ca9a0247d0911de89bb040c508",
        "original_total_additional_fees_set": None,
        "original_total_duties_set": None,
        "payment_gateway_names": [
          "manual"
        ],
        "phone": "+923222222222",
        "po_number": None,
        "presentment_currency": "PKR",
        "processed_at": "2025-05-01T00:57:47-04:00",
        "reference": None,
        "referring_site": None,
        "source_identifier": None,
        "source_name": "shopify_draft_order",
        "source_url": None,
        "subtotal_price": "79670.00",
        "subtotal_price_set": {
          "shop_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          }
        },
        "tags": "",
        "tax_exempt": True,
        "tax_lines": [],
        "taxes_included": False,
        "test": False,
        "token": "780f1ba2885319d53940a5e989b7d4c6",
        "total_cash_rounding_payment_adjustment_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "total_cash_rounding_refund_adjustment_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "total_discounts": "0.00",
        "total_discounts_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "total_line_items_price": "79670.00",
        "total_line_items_price_set": {
          "shop_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "79670.00",
            "currency_code": "PKR"
          }
        },
        "total_outstanding": "0.00",
        "total_price": "80905.00",
        "total_price_set": {
          "shop_money": {
            "amount": "80905.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "80905.00",
            "currency_code": "PKR"
          }
        },
        "total_shipping_price_set": {
          "shop_money": {
            "amount": "1235.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "1235.00",
            "currency_code": "PKR"
          }
        },
        "total_tax": "0.00",
        "total_tax_set": {
          "shop_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "0.00",
            "currency_code": "PKR"
          }
        },
        "total_tip_received": "0.00",
        "total_weight": 4588,
        "updated_at": "2025-05-01T00:57:49-04:00",
        "user_id": 98522431712,
        "billing_address": {
          "first_name": "First",
          "address1": "Near Poggival",
          "phone": None,
          "city": "Lahore",
          "zip": None,
          "province": None,
          "country": "Pakistan",
          "last_name": "Customer",
          "address2": None,
          "company": None,
          "latitude": None,
          "longitude": None,
          "name": "First Customer",
          "country_code": "PK",
          "province_code": None
        },
        "customer": {
          "id": 8420523409632,
          "email": "middle.customer@ollaya.com",
          "created_at": "2025-04-30T12:31:57-04:00",
          "updated_at": "2025-05-01T00:57:49-04:00",
          "first_name": "Middle",
          "last_name": "Customer",
          "state": "disabled",
          "note": None,
          "verified_email": True,
          "multipass_identifier": None,
          "tax_exempt": True,
          "phone": "+923222222404",
          "currency": "PKR",
          "tax_exemptions": [],
          "admin_graphql_api_id": "gid://shopify/Customer/8420523409632",
          "default_address": {
            "id": 9533734355168,
            "customer_id": 8420523409632,
            "first_name": "First",
            "last_name": "Customer",
            "company": "",
            "address1": "Near Poggival",
            "address2": "",
            "city": "Lahore",
            "province": "",
            "country": "Pakistan",
            "zip": "",
            "phone": "",
            "name": "First Customer",
            "province_code": None,
            "country_code": "PK",
            "country_name": "Pakistan",
            "default": True
          }
        },
        "discount_applications": [],
        "fulfillments": [],
        "line_items": [
          {
            "id": 14984942321888,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942321888",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 1,
            "name": "100pcs popsicle stick mix colour ice cream sticks in Pakistan",
            "price": "100.00",
            "price_set": {
              "shop_money": {
                "amount": "100.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "100.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875429363936,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b137",
            "taxable": False,
            "title": "100pcs popsicle stick mix colour ice cream sticks in Pakistan",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303523893472,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942354656,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942354656",
            "attributed_staffs": [],
            "current_quantity": 2,
            "fulfillable_quantity": 2,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 409,
            "name": "1800W 40A DC to DC Adjustable Constant Voltage and Current Power Supply Boost converter Module",
            "price": "3500.00",
            "price_set": {
              "shop_money": {
                "amount": "3500.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "3500.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875431035104,
            "properties": [],
            "quantity": 2,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "B365,krt169",
            "taxable": False,
            "title": "1800W 40A DC to DC Adjustable Constant Voltage and Current Power Supply Boost converter Module",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303530053856,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942387424,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942387424",
            "attributed_staffs": [],
            "current_quantity": 3,
            "fulfillable_quantity": 3,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 1,
            "name": "3W 3.7V COB Light Module Diy LED Buy In Pakistan",
            "price": "50.00",
            "price_set": {
              "shop_money": {
                "amount": "50.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "50.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875429331168,
            "properties": [],
            "quantity": 3,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b307",
            "taxable": False,
            "title": "3W 3.7V COB Light Module Diy LED Buy In Pakistan",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303523664096,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942420192,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942420192",
            "attributed_staffs": [],
            "current_quantity": 4,
            "fulfillable_quantity": 4,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 68,
            "name": "4.8 Volt 4 Cell Battery 4.8 v AA Ni-MH Battery 4*AA Cell Pack Rechargeable SM 2Pin Connector",
            "price": "450.00",
            "price_set": {
              "shop_money": {
                "amount": "450.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "450.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875430412512,
            "properties": [],
            "quantity": 4,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b22",
            "taxable": False,
            "title": "4.8 Volt 4 Cell Battery 4.8 v AA Ni-MH Battery 4*AA Cell Pack Rechargeable SM 2Pin Connector",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303528972512,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942452960,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942452960",
            "attributed_staffs": [],
            "current_quantity": 5,
            "fulfillable_quantity": 5,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 18,
            "name": "EVE ER14505 AA 3.6V Lithium-Ion Battery - Long-Lasting Power for Your Devices",
            "price": "550.00",
            "price_set": {
              "shop_money": {
                "amount": "550.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "550.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875427922144,
            "properties": [],
            "quantity": 5,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b561",
            "taxable": False,
            "title": "EVE ER14505 AA 3.6V Lithium-Ion Battery - Long-Lasting Power for Your Devices",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303514685664,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942485728,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942485728",
            "attributed_staffs": [],
            "current_quantity": 4,
            "fulfillable_quantity": 4,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 38,
            "name": "Fy12 Thermometer and Hygrometer Humidity Meter with Display",
            "price": "290.00",
            "price_set": {
              "shop_money": {
                "amount": "290.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "290.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875428708576,
            "properties": [],
            "quantity": 4,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "B443 krt120",
            "taxable": False,
            "title": "Fy12 Thermometer and Hygrometer Humidity Meter with Display",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303519830240,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942518496,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942518496",
            "attributed_staffs": [],
            "current_quantity": 6,
            "fulfillable_quantity": 6,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 6,
            "name": "K75T60 IGBT IKW75N60T 600V 75A IGBT In Pakistan",
            "price": "280.00",
            "price_set": {
              "shop_money": {
                "amount": "280.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "280.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875428741344,
            "properties": [],
            "quantity": 6,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b673",
            "taxable": False,
            "title": "K75T60 IGBT IKW75N60T 600V 75A IGBT In Pakistan",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303520059616,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942551264,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942551264",
            "attributed_staffs": [],
            "current_quantity": 6,
            "fulfillable_quantity": 6,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 508,
            "name": "Mechanic V-Power 8 Ultra / Max 8-Ports 115W Desktop Digital Display High Power Fast Quick Charger",
            "price": "9500.00",
            "price_set": {
              "shop_money": {
                "amount": "9500.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "9500.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875430248672,
            "properties": [],
            "quantity": 6,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b247",
            "taxable": False,
            "title": "Mechanic V-Power 8 Ultra / Max 8-Ports 115W Desktop Digital Display High Power Fast Quick Charger",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303528644832,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942584032,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942584032",
            "attributed_staffs": [],
            "current_quantity": 6,
            "fulfillable_quantity": 6,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 3,
            "name": "Ring Type Cable Lugs O Type Thimble Cable lug tubular, M3mm, 0.25-1.5mm2 Copper Terminal",
            "price": "5.00",
            "price_set": {
              "shop_money": {
                "amount": "5.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "5.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875426611424,
            "properties": [],
            "quantity": 6,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b68",
            "taxable": False,
            "title": "Ring Type Cable Lugs O Type Thimble Cable lug tubular, M3mm, 0.25-1.5mm2 Copper Terminal",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303505248480,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942616800,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942616800",
            "attributed_staffs": [],
            "current_quantity": 5,
            "fulfillable_quantity": 5,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 30,
            "name": "Solar MC4 Spanner Wrench Tool for Connect & Disconnect Solar Connector In Pakistan",
            "price": "400.00",
            "price_set": {
              "shop_money": {
                "amount": "400.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "400.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875430641888,
            "properties": [],
            "quantity": 5,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "B650",
            "taxable": False,
            "title": "Solar MC4 Spanner Wrench Tool for Connect & Disconnect Solar Connector In Pakistan",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303529201888,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          },
          {
            "id": 14984942649568,
            "admin_graphql_api_id": "gid://shopify/LineItem/14984942649568",
            "attributed_staffs": [],
            "current_quantity": 4,
            "fulfillable_quantity": 4,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 0,
            "name": "YZIF Wired Metal Door Magnetic Contact Sensor Detector - Garage Warehouse Security Magnetic Switch Alarm",
            "price": "1500.00",
            "price_set": {
              "shop_money": {
                "amount": "1500.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "1500.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875427299552,
            "properties": [],
            "quantity": 4,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "",
            "taxable": False,
            "title": "YZIF Wired Metal Door Magnetic Contact Sensor Detector - Garage Warehouse Security Magnetic Switch Alarm",
            "total_discount": "0.00",
            "total_discount_set": {
              "shop_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "0.00",
                "currency_code": "PKR"
              }
            },
            "variant_id": 47303508951264,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [],
            "duties": [],
            "discount_allocations": []
          }
        ],
        "payment_terms": None,
        "refunds": [],
        "shipping_address": {
          "first_name": "First",
          "address1": "Near Poggival",
          "phone": None,
          "city": "Lahore",
          "zip": None,
          "province": None,
          "country": "Pakistan",
          "last_name": "Customer",
          "address2": None,
          "company": None,
          "latitude": 31.5203696,
          "longitude": 74.3587473,
          "name": "First Customer",
          "country_code": "PK",
          "province_code": None
        },
        "shipping_lines": [
          {
            "id": 4921629212896,
            "carrier_identifier": None,
            "code": "custom",
            "current_discounted_price_set": {
              "shop_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              }
            },
            "discounted_price": "1235.00",
            "discounted_price_set": {
              "shop_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              }
            },
            "is_removed": False,
            "phone": None,
            "price": "1235.00",
            "price_set": {
              "shop_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "1235.00",
                "currency_code": "PKR"
              }
            },
            "requested_fulfillment_service_id": None,
            "source": "shopify",
            "title": "WOW",
            "tax_lines": [],
            "discount_allocations": []
          }
        ],
        "returns": []
      }
  print(process_customer(webhook["customer"], None))
  return
  variables = parse_order_webhook(webhook)
  payload = {"query": shopify_query, "variables": variables}

  try:
    response = requests.post(shopify_url, headers=shopify_headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print(data)
    time.sleep(0.5)
  except requests.exceptions.RequestException as e:
    print(f"Encountered error: {e}. Retrying in 60 seconds...")
    time.sleep(30)

if __name__ == "__main__":
  main()
