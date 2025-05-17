from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


# Define the schema
class Variant(BaseModel):
    admin_graphql_api_id: str
    barcode: Optional[str]
    compare_at_price: Optional[str]
    created_at: datetime
    id: int
    inventory_policy: str
    position: int
    price: str
    product_id: int
    sku: Optional[str]
    taxable: bool
    title: str
    updated_at: datetime
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    image_id: Optional[int]
    inventory_item_id: int
    inventory_quantity: int
    old_inventory_quantity: int
class Option(BaseModel):
    name: str
    id: int
    product_id: int
    position: int
    values: List[str]
class Image(BaseModel):
    id: int
    product_id: int
    position: int
    created_at: datetime
    updated_at: datetime
    alt: Optional[str]
    width: int
    height: int
    src: HttpUrl
    variant_ids: List[int]
    admin_graphql_api_id: str
class PreviewImage(BaseModel):
    width: int
    height: int
    src: HttpUrl
    status: str
class Media(BaseModel):
    id: int
    product_id: int
    position: int
    created_at: datetime
    updated_at: datetime
    alt: Optional[str]
    status: str
    media_content_type: str
    preview_image: PreviewImage
    variant_ids: List[int]
    admin_graphql_api_id: str
class VariantGID(BaseModel):
    admin_graphql_api_id: str
    updated_at: datetime
class Category(BaseModel):
    admin_graphql_api_id: str
    name: str
    full_name: str
    
class ProductSchema(BaseModel):
    admin_graphql_api_id: str
    body_html: str
    created_at: datetime
    handle: str
    id: int
    product_type: Optional[str]
    published_at: datetime
    template_suffix: Optional[str]
    title: str
    updated_at: datetime
    vendor: str
    status: str
    published_scope: str
    tags: str
    variants: List[Variant]
    options: List[Option]
    images: List[Image]
    image: Image
    media: List[Media]
    variant_gids: List[VariantGID]
    has_variants_that_requires_components: bool
    category: Category
    

class ProductDeleteSchema(BaseModel):
    id: int
    
class ClientDetails(BaseModel):
    accept_language: Optional[str]
    browser_height: Optional[int]
    browser_ip: Optional[str]
    browser_width: Optional[int]
    session_hash: Optional[str]
    user_agent: Optional[str]
class Money(BaseModel):
    amount: str
    currency_code: str
class MoneySet(BaseModel):
    shop_money: Money
    presentment_money: Money
class DiscountCode(BaseModel):
    code: str
    amount: str
    type: str
class Address(BaseModel):
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  company: Optional[str] = None
  address1: Optional[str] = None
  address2: Optional[str] = None
  city: Optional[str] = None
  province: Optional[str] = None
  country: Optional[str] = None
  zip: Optional[str] = None
  phone: Optional[str] = None
  name: Optional[str] = None
  country_code: Optional[str] = None
  province_code: Optional[str] = None
  latitude: Optional[float] = None
  longitude: Optional[float] = None
class CustomerAddress(Address):
  id: int
  customer_id: int
  default: Optional[bool] = None
  country_name: Optional[str] = None
class Customer(BaseModel):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
    first_name: Optional[str]
    last_name: Optional[str]
    state: Optional[str]
    note: Optional[str]
    verified_email: bool
    multipass_identifier: Optional[str]
    tax_exempt: bool
    phone: Optional[str]
    currency: str
    tax_exemptions: List[str]
    admin_graphql_api_id: str
    default_address: CustomerAddress
class DiscountApplication(BaseModel):
    target_type: str
    type: str
    value: str
    value_type: str
    allocation_method: str
    target_selection: str
    title: str
    description: Optional[str]
class TaxLine(BaseModel):
    channel_liable: bool
    price: str
    price_set: MoneySet
    rate: float
    title: str
class DiscountAllocation(BaseModel):
    amount: str
    amount_set: MoneySet
    discount_application_index: int
class LineItem(BaseModel):
    id: int
    admin_graphql_api_id: str
    current_quantity: int
    fulfillable_quantity: int
    fulfillment_service: str
    fulfillment_status: Optional[str]
    gift_card: bool
    grams: int
    name: str
    price: str
    price_set: MoneySet
    product_exists: bool
    product_id: int
    properties: List[dict]
    quantity: int
    requires_shipping: bool
    sales_line_item_group_id: Optional[str]
    sku: Optional[str]
    taxable: bool
    title: str
    total_discount: str
    total_discount_set: MoneySet
    variant_id: int
    variant_inventory_management: Optional[str]
    variant_title: Optional[str]
    vendor: Optional[str]
    tax_lines: List[TaxLine]
    duties: List[dict]
    discount_allocations: List[DiscountAllocation]
class ShippingLine(BaseModel):
    id: int
    carrier_identifier: Optional[str]
    code: str
    current_discounted_price_set: MoneySet
    discounted_price: str
    discounted_price_set: MoneySet
    is_removed: bool
    phone: Optional[str]
    price: str
    price_set: MoneySet
    requested_fulfillment_service_id: Optional[int]
    source: str
    title: str
    tax_lines: List[TaxLine]
    discount_allocations: List[DiscountAllocation]
    
class OrderWebhook(BaseModel):
    id: int
    admin_graphql_api_id: str
    app_id: int
    browser_ip: str
    buyer_accepts_marketing: bool
    cancel_reason: Optional[str]
    cancelled_at: Optional[datetime]
    cart_token: Optional[str]
    checkout_id: int
    checkout_token: str
    client_details: ClientDetails
    closed_at: Optional[datetime]
    company: Optional[str]
    confirmation_number: str
    confirmed: bool
    contact_email: str
    created_at: datetime
    currency: str

    current_shipping_price_set: MoneySet
    current_subtotal_price: str
    current_subtotal_price_set: MoneySet
    current_total_additional_fees_set: Optional[MoneySet]
    current_total_discounts: str
    current_total_discounts_set: MoneySet
    current_total_duties_set: Optional[MoneySet]
    current_total_price: str
    current_total_price_set: MoneySet
    current_total_tax: str
    current_total_tax_set: MoneySet

    customer_locale: str
    device_id: Optional[int]
    discount_codes: List[DiscountCode]
    duties_included: bool
    email: str
    estimated_taxes: bool
    financial_status: str
    fulfillment_status: Optional[str]
    landing_site: Optional[str]
    landing_site_ref: Optional[str]
    location_id: Optional[int]
    merchant_business_entity_id: Optional[str]
    merchant_of_record_app_id: Optional[int]
    name: str
    note: Optional[str]
    note_attributes: List[dict]
    number: int
    order_number: int
    order_status_url: HttpUrl
    original_total_additional_fees_set: Optional[MoneySet]
    original_total_duties_set: Optional[MoneySet]
    payment_gateway_names: List[str]
    phone: Optional[str]
    po_number: Optional[str]
    presentment_currency: str
    processed_at: datetime
    reference: Optional[str]
    referring_site: Optional[str]
    source_identifier: Optional[str]
    source_name: str
    source_url: Optional[HttpUrl]
    subtotal_price: str
    subtotal_price_set: MoneySet
    tags: str
    tax_exempt: bool
    tax_lines: List[TaxLine]
    taxes_included: bool
    test: bool
    token: str
    total_cash_rounding_payment_adjustment_set: MoneySet
    total_cash_rounding_refund_adjustment_set: MoneySet
    total_discounts: str
    total_discounts_set: MoneySet
    total_line_items_price: str
    total_line_items_price_set: MoneySet
    total_outstanding: str
    total_price: str
    total_price_set: MoneySet
    total_shipping_price_set: MoneySet
    total_tax: str
    total_tax_set: MoneySet
    total_tip_received: str
    total_weight: int
    updated_at: datetime
    user_id: int

    billing_address: Address
    customer: Customer
    discount_applications: List[DiscountApplication]
    fulfillments: List[dict]
    line_items: List[LineItem]
    payment_terms: Optional[dict]
    refunds: List[dict]
    shipping_address: Address
    shipping_lines: List[ShippingLine]
    returns: List[dict]

