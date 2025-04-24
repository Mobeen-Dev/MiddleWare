import os
import asyncio
import aiohttp
from dotenv import load_dotenv

async def fetch_product(product_gid: str):
    load_dotenv()
    SHOPIFY_STORE = os.getenv("PARENT_SHOPIFY_STORE_NAME")
    ACCESS_TOKEN   = os.getenv("PARENT_SHOPIFY_API_SECRET")
    API_VERSION    = "2025-01"
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
    variants(first: 100) {
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

async def main():
    # Example: replace with your real product GID
    product_gid = "gid://shopify/Product/7476035223638"
    product = await fetch_product(product_gid)
    print("Fetched product data:")
    print(type(product))

    variants = product.get("variants").get("edges")
    images = product["media"]["edges"]
    print(images)
    variable = {
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
                    "alt": "Product image – WhatsApp logo",
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
                    "optionValues": [
                        {"optionName": product["options"][0]["name"], "name": variant["node"]["title"]},
                    ],

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
    print("Fetched variant data:", variable)


if __name__ == "__main__":
    asyncio.run(main())
