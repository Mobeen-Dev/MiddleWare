# shopify_bridge/clients/supabase_client.py
import asyncio
from logging import Logger
from warnings import catch_warnings

from supabase import create_client, Client
from config import settings
from logger import get_logger


class DB_Client:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )
        self.logger = get_logger("SupabaseClient")

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
        
    def add_new_product(self, data):
        product = data["data"]["products"]["edges"]["node"]
        self.insert_parent_shopify_product_into_db(product)

    async def insert_parent_shopify_product_into_db(self, product):
        # Product Insertion
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
        images_edges = product.get("images", {}).get("edges", [])
        if images_edges:
            for edge in images_edges:
                node = edge.get("node", {})
                all_images.append(node.get("src", ''))
        
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
        prod_response = self.client.table("products").insert(new_product).execute()
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
            .table("variants")
            .insert(variants)
            .execute()
        )
        
        self.logger.info(f"Batch inserted {len(variants)} variants, result={resp}")
    
    def verify_sync_product(self, id):
        resp = (
            self.client
            .table("products")
            .select("child_id")
            .eq("id", id)
            .execute()
        )
        
        # if resp.error:
        #   print(f"❌ Error: {resp.error.message}")
        #   return 41219660382294, 4.04
        try:
            row: dict = resp.data[0]
            return row["child_id"]
        except Exception as e:
            return None
      
    
    def update_child_ids(self, parent_pid, product):
        child_p_id = int(product["product"]["id"].split('/')[-1])
        response = (
            self.client.table("products")
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
                self.client.table("variants")
                .update({"child_vid": variant_vid})
                .eq("pid", parent_pid)
                .eq("title", variant_title)
                .execute()
            )
    
    async def update_product_status(self, child_p_id: int, status: bool = False) -> None:
        # 3. Offload the blocking update to a thread
        response = await asyncio.to_thread(
            lambda: self.client.table("products")
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
    
    def fetch_parent_variant_id(self, id):
        resp = (
            self.client
            .table("variants")
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
