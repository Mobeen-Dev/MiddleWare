2# Product Feed Mapping Guide

This document outlines the mapping strategy for product feed attributes, categorizing them into **Required Fields**, **Custom Logic Fields**, and **Ignored Fields**.

## Required Fields

These fields are directly mapped from existing product data:

| Field | Source | Notes |
|-------|--------|-------|
| `sku_id` | Direct mapping | Unique product variant identifier |
| `title` | Direct mapping | Product name/title |
| `description` | Direct mapping | Product description |
| `price` | Direct mapping | Product price |
| `link` | Custom URL | `product_url + ?variant=/46085908988182/{sku_id}` |
| `image_link` | Conditional | Use variant image if available, otherwise product image |
| `additional_image_link` | Direct mapping | List of additional product images |
| `item_group_id` | Direct mapping | Maps to `product_id` |
| `product_type` | Conditional | Include if product type exists |
| `shipping_weight` | Direct mapping | Product weight for shipping |
| `brand` | Custom mapping | Maps to `vendor` field |

## Custom Logic Fields

These fields require special processing or business logic:

### `availability`
**Logic:** `inventory_quantity != 0`
- If inventory quantity is greater than 0: "in stock"
- If inventory quantity is 0: "out of stock"

### `condition`
**Logic:** Check if title contains restricted words
- Parse `title.split()` and verify no words exist in predefined restriction list
- Return "new" if clean, otherwise apply appropriate condition

### `link`
**Logic:** Dynamic URL construction
- Base: `product_url`
- Append: `?variant=/46085908988182/{sku_id}`

### `image_link`
**Logic:** Conditional image selection
- Priority 1: Variant-specific image
- Priority 2: Default product image

### `brand`
**Logic:** Map vendor to brand
- Direct mapping from `vendor` field

## Research Required

These fields need further investigation before implementation:

| Field | Status | Notes |
|-------|--------|-------|
| `google_product_category` | Research needed | Requires category taxonomy mapping |
| `material` | Research needed | May need product attribute extraction |

## Custom Fields (Requires Enum Definition)

These fields need predefined value sets:

| Field | Type | Notes |
|-------|------|-------|
| `age_group` | Custom Enum | Define age categories (adult, kids, etc.) |
| `color` | Custom Logic | Extract from product attributes |
| `gender` | Custom Logic | Determine from product data |

## Ignored Fields

### Pricing & Promotions
- `sale_price`
- `sale_price_effective_date`

### Product Identifiers
- `gtin` (Global Trade Item Number)
- `mpn` (Manufacturer Part Number)
- `size`
- `tax`

### Mobile App Integration
- `ios_url`
- `ios_app_store_id`
- `ios_app_name`
- `iPhone_url`
- `iPhone_app_store_id`
- `iPhone_app_name`
- `iPad_url`
- `iPad_app_store_id`
- `iPad_app_name`
- `android_url`
- `android_package`
- `android_app_name`

### Additional Attributes
- `shipping`
- `pattern`
- `video_link`

### Custom Labels
- `custom_label_0`
- `custom_label_1`
- `custom_label_2`
- `custom_label_3`
- `custom_label_4`

## Implementation Priority

1. **Phase 1:** Implement all Required Fields
2. **Phase 2:** Add Custom Logic Fields
3. **Phase 3:** Research and implement Research Required fields
4. **Phase 4:** Define enums and implement Custom Fields

## Data Quality Considerations

- Ensure all required fields have fallback values
- Validate URL construction for `link` field
- Implement error handling for missing images
- Create validation rules for custom logic fields