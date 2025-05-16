# shopify_bridge/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # === Supabase Configuration ===
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_key: str = Field(alias="SUPABASE_KEY")
    
    broker_url: str = Field(alias="BROKER_URL")

    # === Shopify Master Store Credentials ===
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
    
    # === Shopify Child Store Credentials ===
    child_shopify_api_key: str = Field(alias="CHILD_SHOPIFY_API_KEY")
    child_shopify_api_secret: str = Field(alias="CHILD_SHOPIFY_API_SECRET")
    child_shopify_store_name: str = Field(alias="CHILD_SHOPIFY_STORE_NAME")
    child_shopify_api_version: str = Field(alias="CHILD_SHOPIFY_API_VERSION")

    # === Server Settings ===
    port: int = Field(alias="PORT")
    env: str = Field(alias="ENV")

    class Config:
        # tell Pydantic to read a .env file from your project root
        env_file = ".env"
        # you can also specify env_file_encoding = "utf-8" if needed


# instantiate once, and import `settings` everywhere
settings = Settings()