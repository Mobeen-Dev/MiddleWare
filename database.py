import asyncio
import time

from supabase import create_client, Client
from config import settings
from logger import get_logger


class DB_Client:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )
        self.logger = get_logger("SupabaseClient")
        if settings.env == "DEVELOPMENT":
            self.variant_table = "n_variants"
            self.product_table = "n_products"
        else:
            self.variant_table = "variants"
            self.product_table = "products"

    def upsert(
        self,
        table: str,
        records: list[dict],
        on_conflict: str | list[str] | None = None,
    ) -> list[dict]:
        """
        Insert new rows or update on conflict.
        :param table: name of your Supabase table
        :param records: list of dicts to upsert
        :param on_conflict: column(s) to use for conflict resolution
        :returns: list of inserted/updated rows
        """
        builder = self.client.table(table).upsert(records)
        if on_conflict:
            builder = builder.on_conflict(on_conflict)

        res = builder.execute()
        if res.error:
            self.logger.error("Supabase upsert failed on %s: %s", table, res.error)
            raise RuntimeError(res.error.message)
        self.logger.info("Upserted %d rows into %s", len(res.data), table)
        return res.data

    def fetch(
        self,
        table: str,
        columns: str = "*",
        filters: dict[str, any] | None = None,
    ) -> list[dict]:
        """
        Fetch rows with optional equality filters.
        :param table: name of your Supabase table
        :param columns: column list (e.g. "id, name") or "*"
        :param filters: {"col1": val1, "col2": val2} to add .eq() clauses
        :returns: list of matching rows
        """
        builder = self.client.table(table).select(columns)
        if filters:
            for col, val in filters.items():
                builder = builder.eq(col, val)

        res = builder.execute()
        if res.error:
            self.logger.error("Supabase fetch failed on %s: %s", table, res.error)
            raise RuntimeError(res.error.message)
        return res.data

    def delete(self, table: str, filters: dict[str, any]) -> None:
        """
        Delete rows matching all filters.
        :param table: name of your Supabase table
        :param filters: {"col": val} for .eq() clauses
        """
        builder = self.client.table(table)
        for col, val in filters.items():
            builder = builder.eq(col, val)

        res = builder.delete().execute()
        if res.error:
            self.logger.error("Supabase delete failed on %s: %s", table, res.error)
            raise RuntimeError(res.error.message)
        self.logger.info("Deleted rows from %s where %s", table, filters)
        
    async def add_new_product(self, data):
        product = data["data"]["products"]["edges"]["node"]
        await self.insert_parent_shopify_product_into_db(product)

    async def insert_parent_shopify_product_into_db(self, product):
        # Product Insertion
        self.logger.info(f"Inserting parent shopify product into db {product['id']}")
        full_product_id = product["id"]
        pid = full_product_id.split('/')[-1]
        pid = int(pid)
        title = product.get("title", "")
        tags = product.get("tags", [])
        tags_value = ",".join(tags) if isinstance(tags, list) else str(tags)
        status = product.get("status", "active")  # default status
        status = status.lower() == "active"
        
        # Insert images.
        all_images = []
        images_edges = product.get("media", {}).get("edges", [])
        if images_edges:
            for edge in images_edges:
                node = edge.get("node", {})
                if node:
                    url = node.get("image", {}).get("url", "")
                    all_images.append(url)
        
        else:
            all_images = ["https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg"]
        
        new_product = {
            "id": pid,
            "title": title,
            "tags": tags_value,
            "images": all_images,
            "product_active": status,
            "inv_quantity": 404,
            "sync_enable":True
        }
        prod_response = self.client.table(self.product_table).insert(new_product).execute()
        self.logger.info(f"Inserted product: {prod_response} ")

        # Variants Insertion
        variants = []
        variants_edges = product.get("variants", {}).get("edges", [])
        for edge in variants_edges:
            node = edge["node"]
            vid_str = node["id"].split("/")[-1]
            vid = int(vid_str) if vid_str.isdigit() else vid_str
            price = float(node.get("price") or 0)
            variants.append({
                "pid": pid,
                "vid": vid,
                "title": node.get("title", "-"),
                "retail_price": price,
                "b2b_price": price,
                "inv_quantity": node.get("inventoryQuantity", 0),
            })
            
        # 2) run the single insert in a thread to avoid blocking
        resp = await asyncio.to_thread(
            lambda: self.client
            .table(self.variant_table)
            .insert(variants)
            .execute()
        )
        
        self.logger.info(f"Batch inserted {len(variants)} variants, result={resp}")
    
    def verify_sync_product(self, id):
        try:
            resp = (
                self.client
                .table(self.product_table)
                .select("child_id, sync_enable")
                .eq("id", id)
                .maybe_single()  # returns None if no row
                .execute()
            )
            print(resp)
            if not resp: # id is not present in DB
                return 404, False , None
            
            child_id = resp.data["child_id"]
            sync_enable = resp.data["sync_enable"]
            
            var_res = (
                self.client
                .table(self.variant_table)
                .select("pid", head=True, count="exact")  # head=True → no rows, just headers & count
                .eq("pid", id)
                .execute()
            )
            if not var_res:
                return child_id, sync_enable , 0
        
        
            variant_count = var_res.count or 0
            
            return child_id, sync_enable, variant_count
        except Exception as e:
            return None, None , None
    
    def update_child_ids(self, parent_pid, product):
        child_p_id = int(product["product"]["id"].split('/')[-1])
        response = (
            self.client.table(self.product_table)
            .update({"child_id": child_p_id})
            .eq("id", parent_pid)
            .execute()
        )
        variants = product["product"]["variants"]["edges"]
        for variant_json in variants:
            variant = variant_json["node"]
            variant_vid = variant["id"]
            variant_vid = int(variant_vid.split('/')[-1])
            variant_title = variant["title"]
            response = (
                self.client.table(self.variant_table)
                .update({"child_vid": variant_vid})
                .eq("pid", parent_pid)
                .eq("title", variant_title)
                .execute()
            )
    
    async def update_product_status(self, child_p_id: int, status: bool = False) -> None:
        # 3. Offload the blocking update to a thread
        response = await asyncio.to_thread(
            lambda: self.client.table(self.product_table)
            .update({"isActive": status})
            .eq("child_id", child_p_id)
            .execute()
        )  # :contentReference[oaicite:1]{index=1}
        
        # 4. Handle result
        # print(response)
    
    def fetch_parent_variants(self, child_ids: list[int]) -> list[tuple[[int], [float]]]:
        """
        Returns a list of (vid, retail_price) tuples corresponding to each child_id
        in child_ids. If a child_id isn’t found or an error occurs, returns (None, None).
        """
        # 1) Do one big query
        resp = (
            self.client
            .table(self.variant_table)
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
    
    def fetch_parent_variant_id(self, id):
        resp = (
            self.client
            .table(self.variant_table)
            .select("*")
            .eq("child_vid", int(id))
            .execute()
        )
        
        # if resp.error:
        #   print(f"❌ Error: {resp.error.message}")
        #   return 41219660382294, 4.04
        print(resp)
        
        row: dict = resp.data[0]
        return row["vid"], row["retail_price"]
    
    def fetch_variants_by_pid(self, pid: int) -> list[dict]:
        """
        Fetch all variant records for a given product ID with specific pricing columns.

        :param pid: Product ID to filter variants
        :returns: List of variant records with b2b_price, b2b_discount, b2b_prcnt, retail_price
        """
        try:
            response = (
                self.client
                .table(self.variant_table)
                .select("title, b2b_price, b2b_discount, b2b_prcnt, retail_price")
                .eq("pid", pid)
                .execute()
            )
            
            if not response:
                return []
            
            self.logger.info("Fetched %d variants for pid %s", len(response.data), pid)
            return response.data
        
        except Exception as e:
            self.logger.error("Exception while fetching variants for pid %s: %s", pid, str(e))
            raise
    
    def update_multiple_product_images(self, objects: list[dict]) -> None:
        """
        Bulk update 'images' column for multiple products in the n_products table.

        :param objects: List of dicts, each with keys:
            - 'id': product ID
            - 'data': list of image URLs to overwrite in 'images' column
        """
        try:
            # Collect update tasks
            updates = []
            for obj in objects:
                updates.append(
                    self.client
                    .table("products")
                    .update({"images": obj["data"]})
                    .eq("id", obj["id"])
                    .execute()
                )
            
            # Evaluate responses
            for idx, response in enumerate(updates):
                obj_id = objects[idx]["id"]
                if hasattr(response, "status_code") and response.status_code == 200:
                    self.logger.info("Updated images for product ID %s", obj_id)
                elif hasattr(response, "data") and response.data:
                    self.logger.info("Updated images for product ID %s", obj_id)
                else:
                    self.logger.warning("Failed to update product ID %s: %s", obj_id, response)
        
        except Exception as e:
            self.logger.error("Exception during bulk image update: %s", str(e))
            raise
    
    def update_product_retail_price(self, variants):
      try:
        for variant_entry in variants:
            node = variant_entry['node']
            variant_id = node['id'].split('/')[-1]
            retail_price = float(node['price'])  # cast to float if your DB expects numeric
            
            response =  self.client.table(self.variant_table).update({
                "retail_price": retail_price
            }).eq("vid", variant_id).execute()
            
            self.logger.info(f"Updated variant {variant_id} retail Price {retail_price}")
        

      except Exception as e:
          error_msg = str(e).lower()
          if "rate limit" in error_msg or "limit exceeded" in error_msg or "throttled" in error_msg:
              self.logger.warning("Rate limit exceeded, waiting 5 seconds before retrying...")
              time.sleep(7)
              # Retry by recursively calling this function and returning its result
              return self.update_product_retail_price(variants)
          else:
              # Fatal/unexpected error: just log and return None
              self.logger.error(f"Fatal error while updating variants: {e}", exc_info=True)
              return None
      
