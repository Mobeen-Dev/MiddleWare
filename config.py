# shopify_bridge/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
import os

import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Settings(BaseSettings):
    # === Supabase Configuration ===
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_key: str = Field(alias="SUPABASE_KEY")
    
    # broker_url: str = os.environ["AMQP_URL"]
    # broker_url: str= Field(alias="BROKER_URL")
    amqp_url: str= Field(alias="AMQP_URL")


    # === Shopify Master Store credentials ===
    parent_shopify_api_key: str = Field(alias="PARENT_SHOPIFY_API_KEY")
    parent_shopify_api_secret: str = Field(alias="PARENT_SHOPIFY_API_SECRET")
    parent_shopify_store_name: str = Field(alias="PARENT_SHOPIFY_STORE_NAME")
    parent_shopify_api_version: str = Field(alias="PARENT_SHOPIFY_API_VERSION")
    
    # ── helper properties ────────────────────────────
    
    @property
    def parent_store(self) -> dict[str, str]:
        """Handy bundle for the *parent* shop."""
        return {
            "api_key": self.parent_shopify_api_key,
            "api_secret": self.parent_shopify_api_secret,
            "store_name": self.parent_shopify_store_name,
            "api_version": self.parent_shopify_api_version,
        }
    
    @property
    def child_store(self) -> dict[str, str]:
        """Handy bundle for the *child* shop."""
        return {
            "api_key":     self.child_shopify_api_key,
            "api_secret":  self.child_shopify_api_secret,
            "store_name":  self.child_shopify_store_name,
            "api_version": self.child_shopify_api_version,
        }
    
    
    
    # === Shopify Child Store credentials ===
    child_shopify_api_key: str = Field(alias="CHILD_SHOPIFY_API_KEY")
    child_shopify_api_secret: str = Field(alias="CHILD_SHOPIFY_API_SECRET")
    child_shopify_store_name: str = Field(alias="CHILD_SHOPIFY_STORE_NAME")
    child_shopify_api_version: str = Field(alias="CHILD_SHOPIFY_API_VERSION")

    # === Server Settings ===
    port: int = Field(alias="PORT")
    env: str = Field(alias="ENV")

    class Config:
        # tell Pydantic to read a .env file from your project root
        env_file = "./credentials/.env",
        extra = "forbid"
        # you can also specify env_file_encoding = "utf-8" if needed


# instantiate once, and import `settings` everywhere
settings = Settings()

base_url = "https://digilog.pk/products/"
NO_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
DISCONTINUED_KEYWORDS = [
    # Direct discontinuation terms
    "discontinued",
    "discontinue",
    "legacy",
    "abandoned",
    "no-more",
    
    "unavailable",
    "not-available",
    "no-longer-available",
    "sold-out",
    "out-of-stock",
    "out-stock",
    "temporarily-unavailable",
    "currently-unavailable",
    "back-ordered",
    "backorder",
    "pre-order-only",
    
    # Stock status terms
    "no-stock",
    "zero-stock",
    "empty-stock",
    "depleted",
    "exhausted",
    "finished",
    "gone",
    "all-sold",
    "sold",
    
    # Removal from catalog
    "removed",
    "delisted",
    "unlisted",
    "withdrawn",
    "pulled",
    "taken-down",
    "archived",
    "inactive",
    "suspended",
    "paused",
    
    # Temporary status
    "coming-soon",
    "notify-when-available",
    "email-when-available",
    "waitlist",
    "wait-list",
    "on-hold",
    "pending",
    "restocking",
    "restock-soon",
    
    # Supply issues
    "supply-shortage",
    "shortage",
    "limited-supply",
    "supplier-issue",
    "manufacturing-delay",
    "production-delay",
    "shipping-delay",
    
    # Seasonal/temporary removal
    "seasonal",
    "holiday-only",
    "limited-time",
    "special-occasion",
    "event-only",
    "promotion-ended",
    "offer-expired",
    
    # Store management terms
    "catalog-removal",
    "inventory-cleared",
    "stock-cleared",
    "warehouse-empty",
    "fulfillment-issue",
    
    # Customer-facing messages
    "check-back-later",
    "try-again-later",
    "contact-us",
    "call-for-availability",
    "in-store-only",
    "online-unavailable",
    
    # Common abbreviations
    "oos",  # Out of Stock
    "na",  # Not Available
    "tba",  # To Be Announced
    "tbd",  # To Be Determined
    "eto",  # Expected Time Out
    "bo",  # Back Order
]
REFURBISHED_KEYWORDS = [
    "pull-out"
    "refurbished",
    "refurb",
    "renewed",
    "used",
    "pre-owned",
    "preowned",
    "second-hand",
    "secondhand",
    "pre-loved",
    "preloved",
    "previously",
    "owned",
    
    "repaired",
    "restored",
    "reconditioned",
    "rebuilt",
    "remanufactured",
    "overhauled",
    "serviced",
    "fixed",
    "patched",
    "mended",
    
    "acceptable",
    "satisfactory",
    
    "damaged",
    "scratched",
    "dented",
    "cracked",
    "chipped",
    "worn",
    "faded",
    "stained",
    "marked",
    "scuffed",
    "torn",
    "broken",
    "faulty",
    "defective",
    "incomplete",
    
    # Salvage/recovery terms
    "salvage",
    "salvaged",
    "rescued",
    "recovered",
    "pulled",
    "pull-out",
    "pullout",
    "removed",
    "extracted",
    "harvested",
    
    # Return/exchange related
    "returned",
    "exchange",
    "open-box",
    "openbox",
    "demo",
    "demonstration",
    "display",
    "showroom",
    "floor",
    "sample",
    "tested",
    "trial",
    
    # Vintage/old indicators
    "vintage",
    "retro",
    "classic",
    "old",
    "aged",
    "antique",
    "legacy",
    "discontinued",
    
    "parts",
    "spares",
    "components",
    "as-is",
    "untested",
    
    # Missing parts/accessories
    "no-box",
    "missing",
    "without",
    "incomplete-set",
    "partial",
    "loose",
    "bulk-packed",
    
    # Warranty status
    "no-warranty",
    "limited-warranty",
    "expired-warranty",
    "warranty-void",
    
    # Battery/power related
    "battery-issues",
    "power-issues",
    "charging-issues",
    "dead-battery",
    
    # Specific defects
    "screen-crack",
    "water-damage",
    "liquid-damage",
    "drop-damage",
    "impact-damage",
    
    # Abbreviations and slang
    "ref",
    "reff",
    "refub",
    "2nd",
    "2ndhand",
    "prev",
    "ex",
    "oem-pull",
    "rma",
    "doa",
    "bnib",  # Brand New In Box (but sometimes used for refurb)
    
    # Seller descriptors
    "estate",
    "garage-sale",
    "yard-sale",
    "thrift",
    "pawn",
    "consignment",
    
    # Packaging condition
    "open-package",
    "damaged-package",
    "repackaged",
    "brown-box",
    "white-box",
    "oem-packaging",
    
    # Time-related
    "expired",
    "outdated",
    "old-stock",
    "overstock",
    "end-of-life",
    
    # Special conditions
    "customer-return",
    "manufacturer-refurbished",
    "factory-refurbished",
    "seller-refurbished",
    "third-party-refurbished",
]
USED_PRODUCT_KEYWORDS = [
    # Direct used/owned terms
    "used",
    "pre-owned",
    "preowned",
    "previously-owned",
    "second-hand",
    "secondhand",
    "pre-loved",
    "preloved",
    "owned",
    "previously",
    
    # Opening/packaging status
    "opened",
    "open-box",
    "openbox",
    "previously-opened",
    "box-opened",
    "opened-box",
    "unsealed",
    "unboxed",
    "opened-package",
    "package-opened",
    
    # Light usage terms
    "lightly-used",
    "barely-used",
    "slightly-used",
    "gently-used",
    "minimally-used",
    "light-use",
    "minimal-use",
    "gentle-use",
    "little-used",
    "hardly-used",
    
    # Demo/display usage
    "demo",
    "demonstration",
    "display-model",
    "display-unit",
    "showroom-model",
    "floor-model",
    "floor-display",
    "store-display",
    "sample",
    "demo-unit",
    
    # Return/exchange status
    "returned",
    "customer-return",
    "open-return",
    "return-item",
    "exchanged",
    "trade-in",
    "traded-in",
    
    # Testing/trial usage
    "tested",
    "tried",
    "test-unit",
    "trial-unit",
    "evaluation-unit",
    "review-unit",
    "prototype",
    
    # Condition descriptors for used items
    "excellent-condition",
    "very-good-condition",
    "good-condition",
    "fair-condition",
    "working-condition",
    "functional",
    "working",
    "operational",
    
    # Minor wear/usage indicators
    "minor-wear",
    "light-wear",
    "minimal-wear",
    "slight-wear",
    "cosmetic-wear",
    "surface-wear",
    "normal-wear",
    "signs-of-use",
    "show-use",
    
    # Specific usage scenarios
    "home-use",
    "personal-use",
    "office-use",
    "business-use",
    "educational-use",
    "rental-return",
    "lease-return",
    "ex-rental",
    "ex-lease",
    
    # Time-based usage
    "short-term-use",
    "temporary-use",
    "occasional-use",
    "weekend-use",
    "backup-use",
    
    # Packaging/accessories status
    "original-box",
    "with-box",
    "no-original-box",
    "loose",
    "bulk",
    "oem-only",
    "accessories-included",
    "complete-set",
    
    # Quality grades for used items
    "grade-a-used",
    "grade-b-used",
    "excellent-used",
    "very-good-used",
    "good-used",
    "fair-used",
    
    # Commercial/business used
    "corporate-used",
    "office-surplus",
    "company-owned",
    "business-owned",
    "institutional-use",
    
    # Specific defects/issues (minor)
    "minor-scratches",
    "light-scratches",
    "small-marks",
    "fingerprints",
    "dust",
    "minor-scuffs",
    "light-scuffs",
    
    # Functionality status
    "fully-functional",
    "works-perfectly",
    "tested-working",
    "guaranteed-working",
    "like-new-functionality",
    
    # Common abbreviations
    "pre-own",
    "2nd-hand",
    "2ndhand",
    "prev-owned",
    "ex-demo"
]