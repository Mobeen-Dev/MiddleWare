import asyncio

from sync_service import SyncService
service = SyncService()

product_update_webhook_single_variant = {
        "admin_graphql_api_id": "gid://shopify/Product/7196017950806",
        "body_html": "\u003Cp\u003ESensirion WOWSHT30-DIS I2C humidity &amp; temperature sensor. SHT3x-DIS is the next generation of Sensirion’s temperature and humidity sensors. It builds on a new CMO sensor chip that is at the heart of Sensirion’s new humidity and temperature platform. The SHT3x-DIS has increased intelligence, reliability and improved accuracy specifications compared to its predecessor. Its functionality includes enhanced signal processing, two distinctive and user selectable I2C addresses and communication speeds of up to 1 MHz. The DFN package has a footprint of 2.5 x 2.5 mm2 while keeping a height of 0.9 mm. This allows for integration of the SHT3x-DIS into a great variety of applications. Additionally, the wide supply voltage range of 2.4 V to 5.5 V guarantees compatibility with diverse assembly situations. All in all, the SHT3x-DIS incorporates 15 years of knowledge of Sensirion, the leader in the humidity sensor industry.\u003C/p\u003E\n\u003Ch2\u003EPin description:\u003C/h2\u003E\n\u003Ctable width=\"100%\"\u003E\n\u003Ctbody\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E1\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003E\u003Cspan\u003EVin\u003C/span\u003E\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003Ethis is the power pin\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E2\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003EGND\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003Ecommon ground for power and logic I2C Logic pins\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E3\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003ESCL\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003EI2C clock pin, connect to your microcontrollers I2C clock line\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E4\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003ESDA\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003EI2C data pin, connect to your microcontrollers I2C data line\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E5\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003EADR\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003EThis is the I2C address selection pin\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E6\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003ERST\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003EHardware reset pin\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 14%;\" data-mce-style=\"width: 14%;\"\u003E7\u003C/td\u003E\n\u003Ctd style=\"width: 19.3968%;\" data-mce-style=\"width: 19.3968%;\"\u003EALR\u003C/td\u003E\n\u003Ctd style=\"width: 60.6032%;\" data-mce-style=\"width: 60.6032%;\"\u003EAlert/Interrupt output\u003C/td\u003E\n\u003C/tr\u003E\n\u003C/tbody\u003E\n\u003C/table\u003E\n\u003Ch2\u003EPackage Includes:\u003C/h2\u003E\n\u003Cul\u003E\n\u003Cli\u003E1 x Sensirion SHT30-DIS I2C humidity and temperature sensor\u003C/li\u003E\n\u003C/ul\u003E\n\u003Ch2\u003ESpecifications\u003C/h2\u003E\n\u003Ctable border=\"3\" style=\"width: 545px;\" data-mce-style=\"width: 545px;\"\u003E\n\u003Ctbody\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 243.138px;\" data-mce-style=\"width: 243.138px;\"\u003EOperating Voltage\u003C/td\u003E\n\u003Ctd style=\"width: 283.862px;\" data-mce-style=\"width: 283.862px;\"\u003E2.4 V - 5.5V\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 243.138px;\" data-mce-style=\"width: 243.138px;\"\u003ELength\u003C/td\u003E\n\u003Ctd style=\"width: 283.862px;\" data-mce-style=\"width: 283.862px;\"\u003E13mm\u003Cbr\u003E\n\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 243.138px;\" data-mce-style=\"width: 243.138px;\"\u003EWidth\u003C/td\u003E\n\u003Ctd style=\"width: 283.862px;\" data-mce-style=\"width: 283.862px;\"\u003E10mm\u003C/td\u003E\n\u003C/tr\u003E\n\u003Ctr\u003E\n\u003Ctd style=\"width: 243.138px;\" data-mce-style=\"width: 243.138px;\"\u003EWeight\u003C/td\u003E\n\u003Ctd style=\"width: 283.862px;\" data-mce-style=\"width: 283.862px;\"\u003E2gm\u003C/td\u003E\n\u003C/tr\u003E\n\u003C/tbody\u003E\n\u003C/table\u003E\n\u003Cbr\u003E",
        "created_at": "2024-05-01T12:06:53+05:00",
        "handle": "sensirion-sht30-dis-i2c-humidity-temperature-sensor",
        "id": 7196017950806,
        "product_type": "",
        "published_at": "2024-05-01T12:06:47+05:00",
        "template_suffix": None,
        "title": "WOW SHT30 I2C Humidity And Temperature Sensor In Pakistan",
        "updated_at": "2025-05-03T09:49:01+05:00",
        "vendor": "Digilog.pk",
        "status": "active",
        "published_scope": "global",
        "tags": "air, Humidity sensor, inv ok, kh, Sensors, Temperature",
        "variants": [
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219660316758",
            "barcode": "",
            "compare_at_price": "850.00",
            "created_at": "2024-05-01T12:06:53+05:00",
            "id": 41219660316758,
            "inventory_policy": "continue",
            "position": 1,
            "price": "888.00",
            "product_id": 7196017950806,
            "sku": "B796,krt105",
            "taxable": True,
            "title": "Default Title",
            "updated_at": "2025-05-03T09:49:01+05:00",
            "option1": "Default Title",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333508497494,
            "inventory_quantity": 159,
            "old_inventory_quantity": 129
          }
        ],
        "options": [
          {
            "name": "Title",
            "id": 9287445479510,
            "product_id": 7196017950806,
            "position": 1,
            "values": [
              "Default Title"
            ]
          }
        ],
        "images": [
          {
            "id": 33844288421974,
            "product_id": 7196017950806,
            "position": 1,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "width": 700,
            "height": 700,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/200_0fb0b7a3-685f-433b-948f-fe0365087790.webp?v=1735044869",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844288421974"
          },
          {
            "id": 33844288454742,
            "product_id": 7196017950806,
            "position": 2,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "width": 700,
            "height": 700,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/197_38a7f56e-c1fb-4e5b-926f-d69aa28c5cf9.webp?v=1735044869",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844288454742"
          },
          {
            "id": 33844288487510,
            "product_id": 7196017950806,
            "position": 3,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "width": 700,
            "height": 700,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/199.webp?v=1735044869",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844288487510"
          },
          {
            "id": 33844288520278,
            "product_id": 7196017950806,
            "position": 4,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "width": 700,
            "height": 700,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/198.webp?v=1735044869",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844288520278"
          }
        ],
        "image": {
          "id": 33844288421974,
          "product_id": 7196017950806,
          "position": 1,
          "created_at": "2024-12-24T17:54:29+05:00",
          "updated_at": "2024-12-24T17:54:29+05:00",
          "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
          "width": 700,
          "height": 700,
          "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/200_0fb0b7a3-685f-433b-948f-fe0365087790.webp?v=1735044869",
          "variant_ids": [],
          "admin_graphql_api_id": "gid://shopify/ProductImage/33844288421974"
        },
        "media": [
          {
            "id": 26319605399638,
            "product_id": 7196017950806,
            "position": 1,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 700,
              "height": 700,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/200_0fb0b7a3-685f-433b-948f-fe0365087790.webp?v=1735044869",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319605399638"
          },
          {
            "id": 26319605432406,
            "product_id": 7196017950806,
            "position": 2,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 700,
              "height": 700,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/197_38a7f56e-c1fb-4e5b-926f-d69aa28c5cf9.webp?v=1735044869",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319605432406"
          },
          {
            "id": 26319605465174,
            "product_id": 7196017950806,
            "position": 3,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 700,
              "height": 700,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/199.webp?v=1735044869",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319605465174"
          },
          {
            "id": 26319605497942,
            "product_id": 7196017950806,
            "position": 4,
            "created_at": "2024-12-24T17:54:29+05:00",
            "updated_at": "2024-12-24T17:54:29+05:00",
            "alt": "SHT30 I2C Humidity And Temperature Sensor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 700,
              "height": 700,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/198.webp?v=1735044869",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319605497942"
          }
        ],
        "variant_gids": [
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219660316758",
            "updated_at": "2025-05-03T04:49:01.000Z"
          }
        ],
        "has_variants_that_requires_components": False,
        "category": {
          "admin_graphql_api_id": "gid://shopify/TaxonomyCategory/na",
          "name": "Uncategorized",
          "full_name": "Uncategorized"
        }
      }
product_update_webhook_multi_variant = {
        "admin_graphql_api_id": "gid://shopify/Product/7196017492054",
        "body_html": "\u003Cp\u003EThis is a packet of 100pcs  2 Watt 5% Resistor or quarter watt resistors. The \u003Cstrong\u003Eresistor \u003C/strong\u003Eis a very commonly used component in approximately every electronics circuit. Might be you need a resistor for LEDs, for op amp, for analog or digital circuit.\u003C/p\u003E\n\u003Cp data-sourcepos=\"5:1-5:36\"\u003E\u003Cstrong\u003EUnleash Your Electronics Potential in Pakistan:\u003C/strong\u003E\u003C/p\u003E\n\u003Cul data-sourcepos=\"7:1-7:118\"\u003E\n\u003Cli data-sourcepos=\"7:1-7:118\"\u003E\n\u003Cstrong\u003EBulk Pack (100pcs):\u003C/strong\u003E Always have the resistors you need for various electronics projects, saving money and time.\u003C/li\u003E\n\u003Cli data-sourcepos=\"8:1-8:160\"\u003E\n\u003Cstrong\u003E2W Power Rating:\u003C/strong\u003E Handle higher currents compared to standard 1/4W resistors, ideal for power circuits and applications with increased power requirements.\u003C/li\u003E\n\u003Cli data-sourcepos=\"9:1-9:108\"\u003E\n\u003Cstrong\u003E5% Tolerance:\u003C/strong\u003E Ensures reliable resistance values within a 5% margin for accurate circuit performance.\u003C/li\u003E\n\u003Cli data-sourcepos=\"10:1-10:93\"\u003E\n\u003Cstrong\u003ECompact &amp; Versatile:\u003C/strong\u003E Integrate seamlessly into breadboards and project enclosures.\u003C/li\u003E\n\u003Cli data-sourcepos=\"11:1-12:0\"\u003E\n\u003Cstrong\u003EEasy to Use:\u003C/strong\u003E Simple to incorporate into various electronic circuits.\u003C/li\u003E\n\u003C/ul\u003E\n\u003Cp\u003EPlease select a value as shown image in the blue marked area.\u003C/p\u003E\n\u003Cp\u003E\u003Cimg src=\"https://digilog.pk/cdn/shop/files/resistor-value.jpg\" data-original=\"https://hallroad.digilog.pk/images/thumbnails/443/443/detailed/22/resistor_value.JPG\" alt=\"1000 Pcs Of 1/4 Watt, Quarter Watt,0.25w 5% Resistor In\" loading=\"lazy\" width=\"411\" height=\"411\"\u003E\u003C/p\u003E\n\u003Ch2\u003EPackage Includes for  2 Watt 5% Resistor:\u003C/h2\u003E\n\u003Cul\u003E\n\u003Cli\u003EA packet of resistor which contains 1000pcs of 1/4w Resistor\u003Cspan style=\"font-size: 15.21px;\"\u003E.\u003C/span\u003E\n\u003C/li\u003E\n\u003C/ul\u003E\n\u003Cp\u003E\u003Cimg alt='Image result for resistor color code\"' src=\"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSlrbLyKFBkgUmmT3Crs_-6mTeQsm5zxzkTRjj_wOb3Es3KrDOB\" width=\"418\" height=\"400\"\u003E\u003Cbr\u003E  \u003C/p\u003E",
        "created_at": "2024-05-01T12:06:38+05:00",
        "handle": "100pcs-2-watt-5-resistor-in-pakistan",
        "id": 7196017492054,
        "product_type": "",
        "published_at": "2024-05-01T12:06:35+05:00",
        "template_suffix": None,
        "title": "100pcs 2 Watt 5% Resistor In Pakistan",
        "updated_at": "2025-05-03T09:50:28+05:00",
        "vendor": "Digilog Electronics",
        "status": "active",
        "published_scope": "global",
        "tags": "10K, 1k, 1M Ohm Volum Resistor, 330r, 4.7k, 470r, aaaa, quarter watt, resistance, resistor",
        "variants": [
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657629782",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657629782,
            "inventory_policy": "continue",
            "position": 1,
            "price": "550.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "1R---B2",
            "updated_at": "2025-05-03T09:50:28+05:00",
            "option1": "1R---B2",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333505876054,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657662550",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657662550,
            "inventory_policy": "continue",
            "position": 2,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "1.5R---B2",
            "updated_at": "2024-12-24T17:54:04+05:00",
            "option1": "1.5R---B2",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333505908822,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657695318",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657695318,
            "inventory_policy": "continue",
            "position": 3,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "2.2R---B3",
            "updated_at": "2024-12-24T17:54:05+05:00",
            "option1": "2.2R---B3",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333505941590,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657728086",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657728086,
            "inventory_policy": "continue",
            "position": 4,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "2.7R---B4",
            "updated_at": "2024-12-24T17:54:05+05:00",
            "option1": "2.7R---B4",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333505974358,
            "inventory_quantity": -3,
            "old_inventory_quantity": -3
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657793622",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657793622,
            "inventory_policy": "continue",
            "position": 5,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "3.3R---B5",
            "updated_at": "2024-12-24T17:54:05+05:00",
            "option1": "3.3R---B5",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506007126,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657826390",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:39+05:00",
            "id": 41219657826390,
            "inventory_policy": "continue",
            "position": 6,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "3.9R---B6",
            "updated_at": "2024-12-24T17:54:05+05:00",
            "option1": "3.9R---B6",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506039894,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657859158",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219657859158,
            "inventory_policy": "continue",
            "position": 7,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "4.7R---B7",
            "updated_at": "2024-12-24T17:54:06+05:00",
            "option1": "4.7R---B7",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506072662,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657891926",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219657891926,
            "inventory_policy": "continue",
            "position": 8,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "5.6R---B8",
            "updated_at": "2024-12-24T17:54:06+05:00",
            "option1": "5.6R---B8",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506105430,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657924694",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219657924694,
            "inventory_policy": "continue",
            "position": 9,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "6.8R---B9",
            "updated_at": "2024-12-24T17:54:06+05:00",
            "option1": "6.8R---B9",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506138198,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657957462",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219657957462,
            "inventory_policy": "continue",
            "position": 10,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "8.2R---B10",
            "updated_at": "2024-12-24T17:54:06+05:00",
            "option1": "8.2R---B10",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506170966,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657990230",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219657990230,
            "inventory_policy": "continue",
            "position": 11,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "10R---B11",
            "updated_at": "2024-12-24T17:54:07+05:00",
            "option1": "10R---B11",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506203734,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658022998",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658022998,
            "inventory_policy": "continue",
            "position": 12,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "12R---B12",
            "updated_at": "2024-12-24T17:54:07+05:00",
            "option1": "12R---B12",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506236502,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658055766",
            "barcode": "",
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658055766,
            "inventory_policy": "continue",
            "position": 13,
            "price": "600.00",
            "product_id": 7196017492054,
            "sku": "",
            "taxable": True,
            "title": "15R---B13",
            "updated_at": "2024-12-24T17:54:07+05:00",
            "option1": "15R---B13",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506269270,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658088534",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658088534,
            "inventory_policy": "continue",
            "position": 14,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "18R---B14",
            "updated_at": "2024-12-24T17:54:07+05:00",
            "option1": "18R---B14",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506302038,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658121302",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658121302,
            "inventory_policy": "continue",
            "position": 15,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "22R---B15",
            "updated_at": "2024-12-24T17:54:08+05:00",
            "option1": "22R---B15",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506334806,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658154070",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658154070,
            "inventory_policy": "continue",
            "position": 16,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "27R---B16",
            "updated_at": "2024-12-24T17:54:08+05:00",
            "option1": "27R---B16",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506367574,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658186838",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658186838,
            "inventory_policy": "continue",
            "position": 17,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "33R---B17",
            "updated_at": "2024-12-24T17:54:08+05:00",
            "option1": "33R---B17",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506400342,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658219606",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658219606,
            "inventory_policy": "continue",
            "position": 18,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "39R---B18",
            "updated_at": "2024-12-24T17:54:08+05:00",
            "option1": "39R---B18",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506433110,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658252374",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658252374,
            "inventory_policy": "continue",
            "position": 19,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "47R---B19",
            "updated_at": "2024-12-24T17:54:09+05:00",
            "option1": "47R---B19",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506465878,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658285142",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658285142,
            "inventory_policy": "continue",
            "position": 20,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "56R---B20",
            "updated_at": "2024-12-24T17:54:09+05:00",
            "option1": "56R---B20",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506498646,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658317910",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658317910,
            "inventory_policy": "continue",
            "position": 21,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "68R---B21",
            "updated_at": "2024-12-24T17:54:09+05:00",
            "option1": "68R---B21",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506531414,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658350678",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658350678,
            "inventory_policy": "continue",
            "position": 22,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "82R---B22",
            "updated_at": "2024-12-24T17:54:09+05:00",
            "option1": "82R---B22",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506564182,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658383446",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658383446,
            "inventory_policy": "continue",
            "position": 23,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "100R---B23",
            "updated_at": "2024-12-24T17:54:09+05:00",
            "option1": "100R---B23",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506596950,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658416214",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658416214,
            "inventory_policy": "continue",
            "position": 24,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "120R---B24",
            "updated_at": "2024-12-24T17:54:10+05:00",
            "option1": "120R---B24",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506629718,
            "inventory_quantity": 3,
            "old_inventory_quantity": 3
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658448982",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658448982,
            "inventory_policy": "continue",
            "position": 25,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "b138",
            "taxable": True,
            "title": "150R---",
            "updated_at": "2024-12-24T17:54:10+05:00",
            "option1": "150R---",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506662486,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658481750",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658481750,
            "inventory_policy": "continue",
            "position": 26,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "b369",
            "taxable": True,
            "title": "180R---",
            "updated_at": "2025-01-17T19:24:26+05:00",
            "option1": "180R---",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506695254,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658514518",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658514518,
            "inventory_policy": "continue",
            "position": 27,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "220R---B27",
            "updated_at": "2025-01-17T19:24:25+05:00",
            "option1": "220R---B27",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506728022,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658547286",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658547286,
            "inventory_policy": "continue",
            "position": 28,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "270R---B28",
            "updated_at": "2025-01-17T19:24:26+05:00",
            "option1": "270R---B28",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506760790,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658580054",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658580054,
            "inventory_policy": "continue",
            "position": 29,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "330R---B29",
            "updated_at": "2025-01-17T19:24:26+05:00",
            "option1": "330R---B29",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506793558,
            "inventory_quantity": -2,
            "old_inventory_quantity": -2
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658612822",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658612822,
            "inventory_policy": "continue",
            "position": 30,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "390R---B30",
            "updated_at": "2025-01-17T19:24:26+05:00",
            "option1": "390R---B30",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506826326,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658645590",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658645590,
            "inventory_policy": "continue",
            "position": 31,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "470R---B31",
            "updated_at": "2025-01-17T19:24:25+05:00",
            "option1": "470R---B31",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506859094,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658678358",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658678358,
            "inventory_policy": "continue",
            "position": 32,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "560R---B32",
            "updated_at": "2024-12-24T17:54:11+05:00",
            "option1": "560R---B32",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506891862,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658711126",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658711126,
            "inventory_policy": "continue",
            "position": 33,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "680R---B33",
            "updated_at": "2024-12-24T17:54:12+05:00",
            "option1": "680R---B33",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506924630,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658743894",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658743894,
            "inventory_policy": "continue",
            "position": 34,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "820R---B34",
            "updated_at": "2024-12-24T17:54:12+05:00",
            "option1": "820R---B34",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506957398,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658776662",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658776662,
            "inventory_policy": "continue",
            "position": 35,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "b470",
            "taxable": True,
            "title": "1K---",
            "updated_at": "2024-12-24T17:54:12+05:00",
            "option1": "1K---",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333506990166,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658809430",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658809430,
            "inventory_policy": "continue",
            "position": 36,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "1.2K---B36",
            "updated_at": "2024-12-24T17:54:12+05:00",
            "option1": "1.2K---B36",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507022934,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658842198",
            "barcode": "",
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658842198,
            "inventory_policy": "continue",
            "position": 37,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "",
            "taxable": True,
            "title": "1.5K---B37",
            "updated_at": "2024-12-24T17:54:13+05:00",
            "option1": "1.5K---B37",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507055702,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658874966",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658874966,
            "inventory_policy": "continue",
            "position": 38,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "1.8K---B38",
            "updated_at": "2024-12-24T17:54:13+05:00",
            "option1": "1.8K---B38",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507088470,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658907734",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658907734,
            "inventory_policy": "continue",
            "position": 39,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "2.2K---B39",
            "updated_at": "2024-12-24T17:54:13+05:00",
            "option1": "2.2K---B39",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507121238,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658940502",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658940502,
            "inventory_policy": "continue",
            "position": 40,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "2.7K---B40",
            "updated_at": "2024-12-24T17:54:13+05:00",
            "option1": "2.7K---B40",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507154006,
            "inventory_quantity": -2,
            "old_inventory_quantity": -2
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658973270",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219658973270,
            "inventory_policy": "continue",
            "position": 41,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "3.3K---B41",
            "updated_at": "2024-12-24T17:54:14+05:00",
            "option1": "3.3K---B41",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507186774,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659006038",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659006038,
            "inventory_policy": "continue",
            "position": 42,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "3.9K---B42",
            "updated_at": "2024-12-24T17:54:14+05:00",
            "option1": "3.9K---B42",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507219542,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659038806",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659038806,
            "inventory_policy": "continue",
            "position": 43,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "4.7K---B43",
            "updated_at": "2024-12-24T17:54:14+05:00",
            "option1": "4.7K---B43",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507252310,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659071574",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659071574,
            "inventory_policy": "continue",
            "position": 44,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "5.6K---B44",
            "updated_at": "2024-12-24T17:54:14+05:00",
            "option1": "5.6K---B44",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507285078,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659104342",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659104342,
            "inventory_policy": "continue",
            "position": 45,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "6.8K---B45",
            "updated_at": "2024-12-24T17:54:14+05:00",
            "option1": "6.8K---B45",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507317846,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659137110",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659137110,
            "inventory_policy": "continue",
            "position": 46,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "8.2K---B46",
            "updated_at": "2024-12-24T17:54:15+05:00",
            "option1": "8.2K---B46",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507350614,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659169878",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659169878,
            "inventory_policy": "continue",
            "position": 47,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "b844",
            "taxable": True,
            "title": "10K--",
            "updated_at": "2024-12-24T17:54:15+05:00",
            "option1": "10K--",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507383382,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659202646",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659202646,
            "inventory_policy": "continue",
            "position": 48,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "12K---B48",
            "updated_at": "2024-12-24T17:54:15+05:00",
            "option1": "12K---B48",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507416150,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659235414",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659235414,
            "inventory_policy": "continue",
            "position": 49,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "15K---B49",
            "updated_at": "2024-12-24T17:54:15+05:00",
            "option1": "15K---B49",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507448918,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659268182",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659268182,
            "inventory_policy": "continue",
            "position": 50,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "18K---B50",
            "updated_at": "2024-12-24T17:54:16+05:00",
            "option1": "18K---B50",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507481686,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659300950",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659300950,
            "inventory_policy": "continue",
            "position": 51,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "22K---B51",
            "updated_at": "2024-12-24T17:54:16+05:00",
            "option1": "22K---B51",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507514454,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659333718",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659333718,
            "inventory_policy": "continue",
            "position": 52,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "27K---B52",
            "updated_at": "2024-12-24T17:54:16+05:00",
            "option1": "27K---B52",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507547222,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659366486",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659366486,
            "inventory_policy": "continue",
            "position": 53,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "33K---B53",
            "updated_at": "2024-12-24T17:54:16+05:00",
            "option1": "33K---B53",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507579990,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659399254",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659399254,
            "inventory_policy": "continue",
            "position": 54,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "39K---B54",
            "updated_at": "2024-12-24T17:54:17+05:00",
            "option1": "39K---B54",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507612758,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659432022",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659432022,
            "inventory_policy": "continue",
            "position": 55,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "47K---B55",
            "updated_at": "2024-12-24T17:54:17+05:00",
            "option1": "47K---B55",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507645526,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659464790",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659464790,
            "inventory_policy": "continue",
            "position": 56,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "56K---B56",
            "updated_at": "2024-12-24T17:54:17+05:00",
            "option1": "56K---B56",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507678294,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659497558",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659497558,
            "inventory_policy": "continue",
            "position": 57,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "68K---B57",
            "updated_at": "2024-12-24T17:54:17+05:00",
            "option1": "68K---B57",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507711062,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659530326",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659530326,
            "inventory_policy": "continue",
            "position": 58,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "82K---B58",
            "updated_at": "2024-12-24T17:54:18+05:00",
            "option1": "82K---B58",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507743830,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659563094",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659563094,
            "inventory_policy": "continue",
            "position": 59,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "100K---B59",
            "updated_at": "2024-12-24T17:54:18+05:00",
            "option1": "100K---B59",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507776598,
            "inventory_quantity": -2,
            "old_inventory_quantity": -2
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659595862",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:40+05:00",
            "id": 41219659595862,
            "inventory_policy": "continue",
            "position": 60,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "120K---B60",
            "updated_at": "2024-12-24T17:54:18+05:00",
            "option1": "120K---B60",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507809366,
            "inventory_quantity": -2,
            "old_inventory_quantity": -2
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659628630",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659628630,
            "inventory_policy": "continue",
            "position": 61,
            "price": "400.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "150K---B61",
            "updated_at": "2024-12-24T17:54:18+05:00",
            "option1": "150K---B61",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507842134,
            "inventory_quantity": 2,
            "old_inventory_quantity": 2
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659694166",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659694166,
            "inventory_policy": "continue",
            "position": 62,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "180K---B62",
            "updated_at": "2024-12-24T17:54:19+05:00",
            "option1": "180K---B62",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507874902,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659726934",
            "barcode": "",
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659726934,
            "inventory_policy": "continue",
            "position": 63,
            "price": "600.00",
            "product_id": 7196017492054,
            "sku": "",
            "taxable": True,
            "title": "220K---B63",
            "updated_at": "2024-12-24T17:54:19+05:00",
            "option1": "220K---B63",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507907670,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659759702",
            "barcode": "",
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659759702,
            "inventory_policy": "continue",
            "position": 64,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "b64",
            "taxable": True,
            "title": "270K---B64",
            "updated_at": "2024-12-24T17:54:19+05:00",
            "option1": "270K---B64",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507940438,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659792470",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659792470,
            "inventory_policy": "continue",
            "position": 65,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "330K---B65",
            "updated_at": "2024-12-24T17:54:19+05:00",
            "option1": "330K---B65",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333507973206,
            "inventory_quantity": -1,
            "old_inventory_quantity": -1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659825238",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659825238,
            "inventory_policy": "continue",
            "position": 66,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "390K---B66",
            "updated_at": "2024-12-24T17:54:19+05:00",
            "option1": "390K---B66",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333508005974,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659858006",
            "barcode": "",
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659858006,
            "inventory_policy": "continue",
            "position": 67,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": "",
            "taxable": True,
            "title": "470K---B67",
            "updated_at": "2024-12-24T17:54:20+05:00",
            "option1": "470K---B67",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333508038742,
            "inventory_quantity": 1,
            "old_inventory_quantity": 1
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659890774",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659890774,
            "inventory_policy": "continue",
            "position": 68,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "560k---B68",
            "updated_at": "2024-12-24T17:54:20+05:00",
            "option1": "560k---B68",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333508071510,
            "inventory_quantity": 0,
            "old_inventory_quantity": 0
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659923542",
            "barcode": None,
            "compare_at_price": None,
            "created_at": "2024-05-01T12:06:41+05:00",
            "id": 41219659923542,
            "inventory_policy": "continue",
            "position": 69,
            "price": "500.00",
            "product_id": 7196017492054,
            "sku": None,
            "taxable": True,
            "title": "1M Ohm---B69",
            "updated_at": "2024-12-24T17:54:20+05:00",
            "option1": "1M Ohm---B69",
            "option2": None,
            "option3": None,
            "image_id": None,
            "inventory_item_id": 43333508104278,
            "inventory_quantity": -2,
            "old_inventory_quantity": -2
          }
        ],
        "options": [
          {
            "name": "Resistance",
            "id": 9287445020758,
            "product_id": 7196017492054,
            "position": 1,
            "values": [
              "1R---B2",
              "1.5R---B2",
              "2.2R---B3",
              "2.7R---B4",
              "3.3R---B5",
              "3.9R---B6",
              "4.7R---B7",
              "5.6R---B8",
              "6.8R---B9",
              "8.2R---B10",
              "10R---B11",
              "12R---B12",
              "15R---B13",
              "18R---B14",
              "22R---B15",
              "27R---B16",
              "33R---B17",
              "39R---B18",
              "47R---B19",
              "56R---B20",
              "68R---B21",
              "82R---B22",
              "100R---B23",
              "120R---B24",
              "150R---",
              "180R---",
              "220R---B27",
              "270R---B28",
              "330R---B29",
              "390R---B30",
              "470R---B31",
              "560R---B32",
              "680R---B33",
              "820R---B34",
              "1K---",
              "1.2K---B36",
              "1.5K---B37",
              "1.8K---B38",
              "2.2K---B39",
              "2.7K---B40",
              "3.3K---B41",
              "3.9K---B42",
              "4.7K---B43",
              "5.6K---B44",
              "6.8K---B45",
              "8.2K---B46",
              "10K--",
              "12K---B48",
              "15K---B49",
              "18K---B50",
              "22K---B51",
              "27K---B52",
              "33K---B53",
              "39K---B54",
              "47K---B55",
              "56K---B56",
              "68K---B57",
              "82K---B58",
              "100K---B59",
              "120K---B60",
              "150K---B61",
              "180K---B62",
              "220K---B63",
              "270K---B64",
              "330K---B65",
              "390K---B66",
              "470K---B67",
              "560k---B68",
              "1M Ohm---B69"
            ]
          }
        ],
        "images": [
          {
            "id": 33844286619734,
            "product_id": 7196017492054,
            "position": 1,
            "created_at": "2024-12-24T17:54:03+05:00",
            "updated_at": "2024-12-24T17:54:03+05:00",
            "alt": "100pcs 2 Watt 5% Resistor In Pakistan",
            "width": 610,
            "height": 610,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/1000-pcs-of-14-watt-quarter-0-25w-5-resistor-in-pakistan-709_1d50e665-a01c-4173-93fc-b39212e8e885.webp?v=1735044843",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844286619734"
          },
          {
            "id": 33844286652502,
            "product_id": 7196017492054,
            "position": 2,
            "created_at": "2024-12-24T17:54:03+05:00",
            "updated_at": "2024-12-24T17:54:03+05:00",
            "alt": "100pcs 2 Watt 5% Resistor In Pakistan",
            "width": 500,
            "height": 500,
            "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/1000-pcs-of-14-watt-quarter-0-25w-5-resistor-in-pakistan-825_babd190a-feb8-450e-8993-0e4331b3c97d.webp?v=1735044843",
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/ProductImage/33844286652502"
          }
        ],
        "image": {
          "id": 33844286619734,
          "product_id": 7196017492054,
          "position": 1,
          "created_at": "2024-12-24T17:54:03+05:00",
          "updated_at": "2024-12-24T17:54:03+05:00",
          "alt": "100pcs 2 Watt 5% Resistor In Pakistan",
          "width": 610,
          "height": 610,
          "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/1000-pcs-of-14-watt-quarter-0-25w-5-resistor-in-pakistan-709_1d50e665-a01c-4173-93fc-b39212e8e885.webp?v=1735044843",
          "variant_ids": [],
          "admin_graphql_api_id": "gid://shopify/ProductImage/33844286619734"
        },
        "media": [
          {
            "id": 26319604121686,
            "product_id": 7196017492054,
            "position": 1,
            "created_at": "2024-12-24T17:54:03+05:00",
            "updated_at": "2024-12-24T17:54:03+05:00",
            "alt": "100pcs 2 Watt 5% Resistor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 610,
              "height": 610,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/1000-pcs-of-14-watt-quarter-0-25w-5-resistor-in-pakistan-709_1d50e665-a01c-4173-93fc-b39212e8e885.webp?v=1735044843",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319604121686"
          },
          {
            "id": 26319604154454,
            "product_id": 7196017492054,
            "position": 2,
            "created_at": "2024-12-24T17:54:03+05:00",
            "updated_at": "2024-12-24T17:54:03+05:00",
            "alt": "100pcs 2 Watt 5% Resistor In Pakistan",
            "status": "READY",
            "media_content_type": "IMAGE",
            "preview_image": {
              "width": 500,
              "height": 500,
              "src": "https://cdn.shopify.com/s/files/1/0559/7832/8150/files/1000-pcs-of-14-watt-quarter-0-25w-5-resistor-in-pakistan-825_babd190a-feb8-450e-8993-0e4331b3c97d.webp?v=1735044843",
              "status": "READY"
            },
            "variant_ids": [],
            "admin_graphql_api_id": "gid://shopify/MediaImage/26319604154454"
          }
        ],
        "variant_gids": [
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657629782",
            "updated_at": "2025-05-03T04:50:28.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658612822",
            "updated_at": "2025-01-17T14:24:26.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658580054",
            "updated_at": "2025-01-17T14:24:26.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658547286",
            "updated_at": "2025-01-17T14:24:26.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658481750",
            "updated_at": "2025-01-17T14:24:26.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658645590",
            "updated_at": "2025-01-17T14:24:25.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658514518",
            "updated_at": "2025-01-17T14:24:25.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659923542",
            "updated_at": "2024-12-24T12:54:20.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659890774",
            "updated_at": "2024-12-24T12:54:20.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659858006",
            "updated_at": "2024-12-24T12:54:20.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659825238",
            "updated_at": "2024-12-24T12:54:19.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659792470",
            "updated_at": "2024-12-24T12:54:19.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659759702",
            "updated_at": "2024-12-24T12:54:19.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659726934",
            "updated_at": "2024-12-24T12:54:19.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659694166",
            "updated_at": "2024-12-24T12:54:19.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659530326",
            "updated_at": "2024-12-24T12:54:18.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659563094",
            "updated_at": "2024-12-24T12:54:18.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659595862",
            "updated_at": "2024-12-24T12:54:18.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659628630",
            "updated_at": "2024-12-24T12:54:18.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659464790",
            "updated_at": "2024-12-24T12:54:17.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659432022",
            "updated_at": "2024-12-24T12:54:17.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659399254",
            "updated_at": "2024-12-24T12:54:17.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659497558",
            "updated_at": "2024-12-24T12:54:17.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659366486",
            "updated_at": "2024-12-24T12:54:16.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659333718",
            "updated_at": "2024-12-24T12:54:16.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659300950",
            "updated_at": "2024-12-24T12:54:16.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659268182",
            "updated_at": "2024-12-24T12:54:16.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659235414",
            "updated_at": "2024-12-24T12:54:15.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659202646",
            "updated_at": "2024-12-24T12:54:15.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659169878",
            "updated_at": "2024-12-24T12:54:15.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659137110",
            "updated_at": "2024-12-24T12:54:15.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659104342",
            "updated_at": "2024-12-24T12:54:14.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659071574",
            "updated_at": "2024-12-24T12:54:14.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659038806",
            "updated_at": "2024-12-24T12:54:14.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219659006038",
            "updated_at": "2024-12-24T12:54:14.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658973270",
            "updated_at": "2024-12-24T12:54:14.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658842198",
            "updated_at": "2024-12-24T12:54:13.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658874966",
            "updated_at": "2024-12-24T12:54:13.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658907734",
            "updated_at": "2024-12-24T12:54:13.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658940502",
            "updated_at": "2024-12-24T12:54:13.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658809430",
            "updated_at": "2024-12-24T12:54:12.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658776662",
            "updated_at": "2024-12-24T12:54:12.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658743894",
            "updated_at": "2024-12-24T12:54:12.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658711126",
            "updated_at": "2024-12-24T12:54:12.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658678358",
            "updated_at": "2024-12-24T12:54:11.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658448982",
            "updated_at": "2024-12-24T12:54:10.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658416214",
            "updated_at": "2024-12-24T12:54:10.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658252374",
            "updated_at": "2024-12-24T12:54:09.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658285142",
            "updated_at": "2024-12-24T12:54:09.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658317910",
            "updated_at": "2024-12-24T12:54:09.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658350678",
            "updated_at": "2024-12-24T12:54:09.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658383446",
            "updated_at": "2024-12-24T12:54:09.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658219606",
            "updated_at": "2024-12-24T12:54:08.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658186838",
            "updated_at": "2024-12-24T12:54:08.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658154070",
            "updated_at": "2024-12-24T12:54:08.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658121302",
            "updated_at": "2024-12-24T12:54:08.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658088534",
            "updated_at": "2024-12-24T12:54:07.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658055766",
            "updated_at": "2024-12-24T12:54:07.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219658022998",
            "updated_at": "2024-12-24T12:54:07.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657990230",
            "updated_at": "2024-12-24T12:54:07.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657859158",
            "updated_at": "2024-12-24T12:54:06.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657891926",
            "updated_at": "2024-12-24T12:54:06.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657924694",
            "updated_at": "2024-12-24T12:54:06.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657957462",
            "updated_at": "2024-12-24T12:54:06.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657793622",
            "updated_at": "2024-12-24T12:54:05.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657826390",
            "updated_at": "2024-12-24T12:54:05.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657728086",
            "updated_at": "2024-12-24T12:54:05.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657695318",
            "updated_at": "2024-12-24T12:54:05.000Z"
          },
          {
            "admin_graphql_api_id": "gid://shopify/ProductVariant/41219657662550",
            "updated_at": "2024-12-24T12:54:04.000Z"
          }
        ],
        "has_variants_that_requires_components": False,
        "category": {
          "admin_graphql_api_id": "gid://shopify/TaxonomyCategory/na",
          "name": "Uncategorized",
          "full_name": "Uncategorized"
        }
      }
new_product_webhook = {
    "id": 7512111579222,
    "title": "Yellow Snowboard",
    "body_html": None,
    "vendor": "Store mobeen pk",
    "product_type": "",
    "created_at": "2025-02-17T19:53:05+05:00",
    "handle": "yellow-snowboard",
    "updated_at": "2025-02-17T19:53:21+05:00",
    "published_at": None,
    "template_suffix": None,
    "published_scope": "web",
    "tags": "",
    "status": "active",
    "admin_graphql_api_id": "gid://shopify/Product/7512111579222",
    "variants": [
      {
        "id": 42128328097878,
        "product_id": 7512111579222,
        "title": "Default Title",
        "price": "100.00",
        "position": 1,
        "inventory_policy": "deny",
        "compare_at_price": None,
        "option1": "Default Title",
        "option2": None,
        "option3": None,
        "created_at": "2025-02-17T19:53:05+05:00",
        "updated_at": "2025-02-17T19:53:06+05:00",
        "taxable": True,
        "barcode": None,
        "fulfillment_service": "manual",
        "grams": 0,
        "inventory_management": None,
        "requires_shipping": True,
        "sku": "",
        "weight": 0,
        "weight_unit": "kg",
        "inventory_item_id": 44242533613654,
        "inventory_quantity": 0,
        "old_inventory_quantity": 0,
        "admin_graphql_api_id": "gid://shopify/ProductVariant/42128328097878",
        "image_id": None
      }
    ],
    "options": [
      {
        "id": 9654376104022,
        "product_id": 7512111579222,
        "name": "Title",
        "position": 1,
        "values": [
          "Default Title"
        ]
      }
    ],
    "images": [],
    "image": None
  }

order_webhook = {
        "id": 6106792100064,
        "admin_graphql_api_id": "gid://shopify/Order/6106792100064",
        "app_id": 1354745,
        "browser_ip": "103.125.177.132",
        "buyer_accepts_marketing": False,
        "cancel_reason": None,
        "cancelled_at": None,
        "cart_token": None,
        "checkout_id": 35839425413344,
        "checkout_token": "0329e35c7dfea3f301929d9b150f8b5c",
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
        "confirmation_number": "8HMKKE9FK",
        "confirmed": True,
        "contact_email": "third.customer@ollaya.com",
        "created_at": "2025-05-03T03:41:25-04:00",
        "currency": "PKR",
        "current_shipping_price_set": {
          "shop_money": {
            "amount": "250.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "250.00",
            "currency_code": "PKR"
          }
        },
        "current_subtotal_price": "25180.65",
        "current_subtotal_price_set": {
          "shop_money": {
            "amount": "25180.65",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "25180.65",
            "currency_code": "PKR"
          }
        },
        "current_total_additional_fees_set": None,
        "current_total_discounts": "254.35",
        "current_total_discounts_set": {
          "shop_money": {
            "amount": "254.35",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "254.35",
            "currency_code": "PKR"
          }
        },
        "current_total_duties_set": None,
        "current_total_price": "25430.65",
        "current_total_price_set": {
          "shop_money": {
            "amount": "25430.65",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "25430.65",
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
        "discount_codes": [
          {
            "code": "###",
            "amount": "254.35",
            "type": "percentage"
          }
        ],
        "duties_included": False,
        "email": "third.customer@ollaya.com",
        "estimated_taxes": False,
        "financial_status": "paid",
        "fulfillment_status": None,
        "landing_site": None,
        "landing_site_ref": None,
        "location_id": None,
        "merchant_business_entity_id": "MTc1MjEyOTQ3Njgw",
        "merchant_of_record_app_id": None,
        "name": "-\u003E1004",
        "note": None,
        "note_attributes": [],
        "number": 4,
        "order_number": 1004,
        "order_status_url": "https://ollaya.myshopify.com/75212947680/orders/f674805a89f801731ac0c2d2ac05466c/authenticate?key=1fc47c7b918a7edc714303d8c0382cf3",
        "original_total_additional_fees_set": None,
        "original_total_duties_set": None,
        "payment_gateway_names": [
          "manual"
        ],
        "phone": "+923000000000",
        "po_number": None,
        "presentment_currency": "PKR",
        "processed_at": "2025-05-03T03:41:25-04:00",
        "reference": None,
        "referring_site": None,
        "source_identifier": None,
        "source_name": "shopify_draft_order",
        "source_url": None,
        "subtotal_price": "25180.65",
        "subtotal_price_set": {
          "shop_money": {
            "amount": "25180.65",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "25180.65",
            "currency_code": "PKR"
          }
        },
        "tags": "",
        "tax_exempt": False,
        "tax_lines": [],
        "taxes_included": False,
        "test": False,
        "token": "f674805a89f801731ac0c2d2ac05466c",
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
        "total_discounts": "254.35",
        "total_discounts_set": {
          "shop_money": {
            "amount": "254.35",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "254.35",
            "currency_code": "PKR"
          }
        },
        "total_line_items_price": "25435.00",
        "total_line_items_price_set": {
          "shop_money": {
            "amount": "25435.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "25435.00",
            "currency_code": "PKR"
          }
        },
        "total_outstanding": "0.00",
        "total_price": "25430.65",
        "total_price_set": {
          "shop_money": {
            "amount": "25430.65",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "25430.65",
            "currency_code": "PKR"
          }
        },
        "total_shipping_price_set": {
          "shop_money": {
            "amount": "250.00",
            "currency_code": "PKR"
          },
          "presentment_money": {
            "amount": "250.00",
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
        "total_weight": 268,
        "updated_at": "2025-05-03T03:41:26-04:00",
        "user_id": 98522431712,
        "billing_address": {
          "first_name": "Third",
          "address1": "",
          "phone": None,
          "city": "",
          "zip": None,
          "province": None,
          "country": "Pakistan",
          "last_name": "Customer",
          "address2": None,
          "company": None,
          "latitude": None,
          "longitude": None,
          "name": "Third Customer",
          "country_code": "PK",
          "province_code": None
        },
        "customer": {
          "id": 8421848547552,
          "email": "third.customer@ollaya.com",
          "created_at": "2025-05-01T05:12:00-04:00",
          "updated_at": "2025-05-03T03:41:26-04:00",
          "first_name": "Third",
          "last_name": "Customer",
          "state": "disabled",
          "note": "",
          "verified_email": True,
          "multipass_identifier": None,
          "tax_exempt": False,
          "phone": "+923000000000",
          "currency": "PKR",
          "tax_exemptions": [],
          "admin_graphql_api_id": "gid://shopify/Customer/8421848547552",
          "default_address": {
            "id": 9535264686304,
            "customer_id": 8421848547552,
            "first_name": "Third",
            "last_name": "Customer",
            "company": "",
            "address1": "",
            "address2": "",
            "city": "",
            "province": "",
            "country": "Pakistan",
            "zip": "",
            "phone": "",
            "name": "Third Customer",
            "province_code": None,
            "country_code": "PK",
            "country_name": "Pakistan",
            "default": True
          }
        },
        "discount_applications": [
          {
            "target_type": "line_item",
            "type": "manual",
            "value": "1.0",
            "value_type": "percentage",
            "allocation_method": "across",
            "target_selection": "all",
            "title": "###",
            "description": "###"
          }
        ],
        "fulfillments": [],
        "line_items": [
          {
            "id": 14992081584352,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081584352",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 25,
            "name": "1 Meter 18650 Nickel Strip Belt Tape Li-ion Battery Connector Spcc Spot Welding Bms Parts 0.12mm 10mm",
            "price": "60.00",
            "price_set": {
              "shop_money": {
                "amount": "60.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "60.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875428479200,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b186,Krt206",
            "taxable": False,
            "title": "1 Meter 18650 Nickel Strip Belt Tape Li-ion Battery Connector Spcc Spot Welding Bms Parts 0.12mm 10mm",
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
            "variant_id": 47303518191840,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog Electronics",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "0.60",
                "amount_set": {
                  "shop_money": {
                    "amount": "0.60",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.60",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081617120,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081617120",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 76,
            "name": "1 meter High Speed Hdmi male to hdmi female Cable",
            "price": "250.00",
            "price_set": {
              "shop_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875429986528,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b824",
            "taxable": False,
            "title": "1 meter High Speed Hdmi male to hdmi female Cable",
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
            "variant_id": 47303527399648,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "2.50",
                "amount_set": {
                  "shop_money": {
                    "amount": "2.50",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "2.50",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081649888,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081649888",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 100,
            "name": "100pcs 2 Watt 5% Resistor In Pakistan - 15K---B49 / Multicolor",
            "price": "500.00",
            "price_set": {
              "shop_money": {
                "amount": "500.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "500.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875431788768,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": None,
            "taxable": False,
            "title": "100pcs 2 Watt 5% Resistor In Pakistan",
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
            "variant_id": 47303532773600,
            "variant_inventory_management": "shopify",
            "variant_title": "15K---B49 / Multicolor",
            "vendor": "Digilog Electronics",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "5.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "5.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "5.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081682656,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081682656",
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
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "1.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "1.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "1.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081715424,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081715424",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 1,
            "name": "10mm google eye in Pakistan",
            "price": "10.00",
            "price_set": {
              "shop_money": {
                "amount": "10.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "10.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875429462240,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b145",
            "taxable": False,
            "title": "10mm google eye in Pakistan",
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
            "variant_id": 47303524384992,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "0.10",
                "amount_set": {
                  "shop_money": {
                    "amount": "0.10",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.10",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081748192,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081748192",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 1,
            "name": "2 Pin JST-XH Male Right Angle 2515 Connector 2.54mm Pitch",
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
            "product_id": 8875428118752,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b490",
            "taxable": False,
            "title": "2 Pin JST-XH Male Right Angle 2515 Connector 2.54mm Pitch",
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
            "variant_id": 47303515865312,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "0.05",
                "amount_set": {
                  "shop_money": {
                    "amount": "0.05",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.05",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081780960,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081780960",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 24,
            "name": "24V DC Coil T90 Power Relay In Pakistan 6 Pin",
            "price": "200.00",
            "price_set": {
              "shop_money": {
                "amount": "200.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "200.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875430609120,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b470",
            "taxable": False,
            "title": "24V DC Coil T90 Power Relay In Pakistan 6 Pin",
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
            "variant_id": 47303529169120,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "2.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "2.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "2.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081813728,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081813728",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 36,
            "name": "2pcs Wire Brush Stainless Steel Nylon Brass Wire Brushes Cleaning Rust Kit Polishing Metal Rust Clean Tools",
            "price": "120.00",
            "price_set": {
              "shop_money": {
                "amount": "120.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "120.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875429167328,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b339,Krt205",
            "taxable": False,
            "title": "2pcs Wire Brush Stainless Steel Nylon Brass Wire Brushes Cleaning Rust Kit Polishing Metal Rust Clean Tools",
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
            "variant_id": 47303522386144,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "1.20",
                "amount_set": {
                  "shop_money": {
                    "amount": "1.20",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "1.20",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081846496,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081846496",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 5,
            "name": "3S Type C 11.1V Step-Up Boost LiPo Polymer Li-Ion Charger 12.6Vdc 18650 Lithium Battery In Pakistan",
            "price": "190.00",
            "price_set": {
              "shop_money": {
                "amount": "190.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "190.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875431690464,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "b632",
            "taxable": False,
            "title": "3S Type C 11.1V Step-Up Boost LiPo Polymer Li-Ion Charger 12.6Vdc 18650 Lithium Battery In Pakistan",
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
            "variant_id": 47303531102432,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "1.90",
                "amount_set": {
                  "shop_money": {
                    "amount": "1.90",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "1.90",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081879264,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081879264",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 0,
            "name": "48V 20A 1000W Universal Regulated Switching Power Supply Driver for CCTV camera LED Strip AC 100-240V Input to DC 48V",
            "price": "10000.00",
            "price_set": {
              "shop_money": {
                "amount": "10000.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "10000.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875428937952,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "",
            "taxable": False,
            "title": "48V 20A 1000W Universal Regulated Switching Power Supply Driver for CCTV camera LED Strip AC 100-240V Input to DC 48V",
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
            "variant_id": 47303521206496,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "100.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "100.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "100.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081912032,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081912032",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 0,
            "name": "Arduino Human Following Robot (Unassembled Only Parts)",
            "price": "7000.00",
            "price_set": {
              "shop_money": {
                "amount": "7000.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "7000.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875431493856,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "",
            "taxable": False,
            "title": "Arduino Human Following Robot (Unassembled Only Parts)",
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
            "variant_id": 47303530676448,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "70.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "70.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "70.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          },
          {
            "id": 14992081944800,
            "admin_graphql_api_id": "gid://shopify/LineItem/14992081944800",
            "attributed_staffs": [],
            "current_quantity": 1,
            "fulfillable_quantity": 1,
            "fulfillment_service": "manual",
            "fulfillment_status": None,
            "gift_card": False,
            "grams": 0,
            "name": "Arduino Obstacle Avoiding Kit",
            "price": "7000.00",
            "price_set": {
              "shop_money": {
                "amount": "7000.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "7000.00",
                "currency_code": "PKR"
              }
            },
            "product_exists": True,
            "product_id": 8875431395552,
            "properties": [],
            "quantity": 1,
            "requires_shipping": True,
            "sales_line_item_group_id": None,
            "sku": "",
            "taxable": False,
            "title": "Arduino Obstacle Avoiding Kit",
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
            "variant_id": 47303530545376,
            "variant_inventory_management": "shopify",
            "variant_title": None,
            "vendor": "Digilog.pk",
            "tax_lines": [
              {
                "channel_liable": False,
                "price": "0.00",
                "price_set": {
                  "shop_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "0.00",
                    "currency_code": "PKR"
                  }
                },
                "rate": 0.16,
                "title": "GST"
              }
            ],
            "duties": [],
            "discount_allocations": [
              {
                "amount": "70.00",
                "amount_set": {
                  "shop_money": {
                    "amount": "70.00",
                    "currency_code": "PKR"
                  },
                  "presentment_money": {
                    "amount": "70.00",
                    "currency_code": "PKR"
                  }
                },
                "discount_application_index": 0
              }
            ]
          }
        ],
        "payment_terms": None,
        "refunds": [],
        "shipping_address": {
          "first_name": "Third",
          "address1": "",
          "phone": None,
          "city": "",
          "zip": None,
          "province": None,
          "country": "Pakistan",
          "last_name": "Customer",
          "address2": None,
          "company": None,
          "latitude": None,
          "longitude": None,
          "name": "Third Customer",
          "country_code": "PK",
          "province_code": None
        },
        "shipping_lines": [
          {
            "id": 4923897184480,
            "carrier_identifier": None,
            "code": "custom",
            "current_discounted_price_set": {
              "shop_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              }
            },
            "discounted_price": "250.00",
            "discounted_price_set": {
              "shop_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              }
            },
            "is_removed": False,
            "phone": None,
            "price": "250.00",
            "price_set": {
              "shop_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              },
              "presentment_money": {
                "amount": "250.00",
                "currency_code": "PKR"
              }
            },
            "requested_fulfillment_service_id": None,
            "source": "shopify",
            "title": "TCS",
            "tax_lines": [],
            "discount_allocations": []
          }
        ],
        "returns": []
      }


if __name__ == "__main__":
    print("Test")
    # Product Sync Test
    asyncio.run(
      service.handle_product_update(new_product_webhook)
    )
    # asyncio.run(
    #   service.handle_product_update(product_update_webhook_multi_variant)
    # )
    # asyncio.run(
    #   service.handle_incoming_orders(order_webhook)
    # )