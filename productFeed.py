from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from logger import get_logger
import csv
import os
from pathlib import Path

logger = get_logger("ProductFeed")
@dataclass
class ProductFeed:
  """
  Product Feed data structure based on TikTok/Facebook product catalog requirements.

  All fields are typed according to the specification with proper validation rules.
  Required fields must be provided, optional fields default to None.
  """
  
  # Required Fields
  sku_id: str  # Max 100 chars, unique per catalog
  title: str  # Max 500 chars
  description: str  # Max 10,000 chars
  availability: str  # Enum: "In stock", "Available", "Preorder", "Out of stock", "Discontinued"
  condition: str  # Enum: "New", "Refurbished", "Used"
  price: str  # Format: "9.97 USD"
  link: str  # Product landing page URL
  image_link: str  # Main product image URL (≥500x500px)
  brand: str  # Max 150 chars
  
  # Optional Fields
  video_link: Optional[str] = None  # Product video URL
  additional_image_link: Optional[str] = None  # Comma-separated URLs (max 10)
  age_group: Optional[str] = None  # Enum: "Newborn", "Infant", "Toddler", "Kids", "Adult"
  color: Optional[str] = None  # Max 100 chars
  gender: Optional[str] = None  # Enum: "Male", "Female", "Unisex"
  item_group_id: Optional[str] = None  # SPU/Product Group ID
  google_product_category: Optional[str] = None  # Google taxonomy category
  material: Optional[str] = None  # Max 200 chars
  pattern: Optional[str] = None  # Max 100 chars
  product_type: Optional[str] = None  # Category hierarchy (max 3 levels)
  sale_price: Optional[str] = None  # Discounted price format
  sale_price_effective_date: Optional[str] = None  # Format: "2017-12-01T0:00/2017-12-31T0:00"
  shipping: Optional[str] = None  # Format: "COUNTRY:STATE:SHIPPING_TYPE:PRICE:SERVICE"
  shipping_weight: Optional[str] = None  # Format: "0.00kg"
  gtin: Optional[str] = None  # Global Trade Item Number
  mpn: Optional[str] = None  # Manufacturer Part Number
  size: Optional[str] = None  # Product size
  tax: Optional[str] = None  # Tax cost
  
  # iOS App Fields
  ios_url: Optional[str] = None
  ios_app_store_id: Optional[str] = None
  ios_app_name: Optional[str] = None
  iPhone_url: Optional[str] = None
  iPhone_app_store_id: Optional[str] = None
  iPhone_app_name: Optional[str] = None
  iPad_url: Optional[str] = None
  iPad_app_store_id: Optional[str] = None
  iPad_app_name: Optional[str] = None
  
  # Android App Fields
  android_url: Optional[str] = None
  android_package: Optional[str] = None
  android_app_name: Optional[str] = None
  
  # Custom Labels
  custom_label_0: Optional[str] = None
  custom_label_1: Optional[str] = None
  custom_label_2: Optional[str] = None
  custom_label_3: Optional[str] = None
  custom_label_4: Optional[str] = None
  

  
  def __post_init__(self):
    """Validate required fields and formats after initialization."""
    self._validate_required_fields()
    self._validate_field_lengths()
    self._validate_enums()
  
  def _validate_required_fields(self):
    """Ensure all required fields are provided and not empty."""
    required_fields = [
      'sku_id', 'title', 'description', 'availability',
      'condition', 'price', 'link', 'image_link', 'brand'
    ]
    
    for field_name in required_fields:
      value = getattr(self, field_name)
      if not value or not value.strip():
        raise ValueError(f"Required field '{field_name}' cannot be empty")
  
  def _validate_field_lengths(self):
    """Trim fields that exceed character limits."""
    length_limits = {
      'sku_id': 100,
      'title': 500,
      'description': 10000,
      'brand': 150,
      'color': 100,
      'material': 200,
      'pattern': 100
    }
    
    for field_name, max_length in length_limits.items():
      value = getattr(self, field_name)
      if value and len(value) > max_length:
        trimmed_value = value[:max_length]
        setattr(self, field_name, trimmed_value)
        logger.warning(f" Field '{field_name}' was trimmed from {len(value)} to {max_length} characters")
  
  def _validate_enums(self):
    """Validate enum values."""
    enum_validations = {
      'availability': ["in stock", "available for order", "preorder", "out of stock", "discontinued"],
      'condition': ["new", "refurbished", "used"],
      'age_group': ["newborn", "infant", "toddler", "kids", "adult"],
      'gender': ["male", "female", "unisex"]
    }
    
    for field_name, valid_values in enum_validations.items():
      value = getattr(self, field_name)
      if value:
        # Convert to lowercase for comparison
        value_lower = value.lower()
        if value_lower in valid_values:
          # Set the field to the correct lowercase format
          setattr(self, field_name, value_lower)
        else:
          # Try to map common variations
          mappings = {
            'availability': {
              'in_stock': 'in stock',
              'available': 'available for order',
              'out_of_stock': 'out of stock'
            },
            'condition': {
              'brand_new': 'new'
            },
            'gender': {
              'unisex': 'unisex',
              'm': 'male',
              'f': 'female'
            }
          }
          
          if field_name in mappings and value_lower in mappings[field_name]:
            setattr(self, field_name, mappings[field_name][value_lower])
          else:
            logger.warning(
              f"Field '{field_name}' value '{value}' normalized to lowercase. Valid values: {', '.join(valid_values)}")
            # Set to lowercase anyway to avoid rejection
            setattr(self, field_name, value_lower)
  
  def to_dict(self) -> dict:
    """Convert ProductFeed to dictionary, excluding None values."""
    return {k: v for k, v in self.__dict__.items() if v is not None}
  
  def to_csv_row(self, all_fields: List[str]) -> List[str]:
    """Convert ProductFeed to CSV row with all fields in specified order."""
    row = []
    for field in all_fields:
      value = getattr(self, field, None)
      # Convert None to empty string, everything else to string
      row.append('' if value is None else str(value))
    return row
    # return [str(getattr(self, field, '')) for field in all_fields]


class ProductFeedManager:
  """Manager class for handling multiple ProductFeed objects."""
  
  def __init__(self):
    self.products: List[ProductFeed] = []
  
  def add_product(self, product: ProductFeed) -> None:
    """Add a product to the collection."""
    # Validate unique SKU
    if any(p.sku_id == product.sku_id for p in self.products):
      raise ValueError(f"SKU '{product.sku_id}' already exists in catalog")
    
    self.products.append(product)
  
  def get_product_by_sku(self, sku_id: str) -> Optional[ProductFeed]:
    """Get product by SKU ID."""
    return next((p for p in self.products if p.sku_id == sku_id), None)
  
  def remove_product(self, sku_id: str) -> bool:
    """Remove product by SKU ID. Returns True if removed, False if not found."""
    for i, product in enumerate(self.products):
      if product.sku_id == sku_id:
        del self.products[i]
        return True
    return False
  
  def get_all_field_names(self) -> List[str]:
    """Get all possible field names from ProductFeed dataclass."""
    return list(ProductFeed.__dataclass_fields__.keys())
  
  def export_to_csv(self, filename: str, file_path: str = None) -> str:
    """
    Export all products to CSV file at specified path.

    Args:
        filename: Name of the CSV file
        file_path: Directory path where to save the file

    Returns:
        Full path of the created file
    """
    if not self.products:
      raise ValueError("No products to export")
    
    # Create full file path
    if file_path:
      # Ensure the directory exists
      Path(file_path).mkdir(parents=True, exist_ok=True)
      full_path = os.path.join(file_path, filename)
    else:
      # Save in current directory if no path specified
      full_path = filename
    
    # Ensure .csv extension
    if not full_path.endswith('.csv'):
      full_path += '.csv'
    
    all_fields = self.get_all_field_names()
    
    with open(full_path, 'w', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      
      # Write header
      writer.writerow(all_fields)
      
      # Write product rows
      for product in self.products:
        writer.writerow(product.to_csv_row(all_fields))
    
    logger.info(f"CSV file saved at: {full_path}")
    return full_path
  
  def get_products_by_brand(self, brand: str) -> List[ProductFeed]:
    """Get all products by brand."""
    return [p for p in self.products if p.brand == brand]
  
  def get_products_by_availability(self, availability: str) -> List[ProductFeed]:
    """Get all products by availability status."""
    return [p for p in self.products if p.availability == availability]
  
  def __len__(self) -> int:
    """Return number of products."""
    return len(self.products)
  
  def __iter__(self):
    """Make ProductFeedManager iterable."""
    return iter(self.products)


# Example usage
if __name__ == "__main__":
  # Create product feed manager
  manager = ProductFeedManager()
  
  # Create sample products
  product1 = ProductFeed(
    sku_id="PROD-001",
    title="Wireless Bluetooth Headphones",
    description="High-quality wireless headphones with noise cancellation and 20-hour battery life.",
    availability="In stock",
    condition="New",
    price="89.99 PKR",
    link="https://example.com/products/wireless-headphones",
    image_link="https://example.com/images/headphones-main.jpg",
    brand="TechBrand",
    color="Black",
    item_group_id="HEADPHONES-GROUP",
    product_type="Electronics > Audio > Headphones",
    shipping_weight="0.5kg"
  )
  
  product2 = ProductFeed(
    sku_id="PROD-002",
    title="Cotton Summer Dress",
    description="Lightweight cotton dress perfect for summer occasions.",
    availability="Available",
    condition="New",
    price="45.50 PKR",
    link="https://example.com/products/summer-dress",
    image_link="https://example.com/images/dress-main.jpg",
    brand="FashionBrand",
    color="Blue",
    size="Large",
    gender="Female",
    material="100% Cotton",
    age_group="Adult"
  )
  
  # Add products to manager
  manager.add_product(product1)
  manager.add_product(product2)
  
  # Export to CSV
  manager.export_to_csv("product_feed.csv")
  
  logger.info(f"Successfully created product feed with {len(manager)} products")
