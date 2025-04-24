import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load env vars
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Set SUPABASE_URL and SUPABASE_KEY in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BATCH_SIZE = 20
offset = 0

while True:
    start = offset
    end = offset + BATCH_SIZE - 1

    resp = (
        supabase
        .table("products")
        .select("*")
        # .eq("sync_enable", False)
        # .order("id", desc=False)  # ascending
        .gt("retail_price", 1000)
        .range(start, end)
        .execute()
    )

    batch = resp.data or []
    if not batch:
        # no more rows
        break

    ids = [row["id"] for row in batch]
    print(f"Fetched IDs {start}–{end}:", ids)

    # ----- your processing goes here -----
    # e.g. sync_to_shopify(ids)
    # ---------------------------------------

    offset += BATCH_SIZE
