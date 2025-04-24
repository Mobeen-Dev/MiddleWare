url_path0 = "askf;lsfkllfsdfnfndsfnsdansd?ASDFfsdF?FASFfasdf?ASDf"

url_path = url_path0.split("?")
print(url_path)

from supabase import create_client

# SUPABASE_URL = "https://gmiskrjbvukikbrqvnkz.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdtaXNrcmpidnVraWticnF2bmt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQxNzE0OTAsImV4cCI6MjA1OTc0NzQ5MH0.j5w4n3YoqXC5Y6ggOW7kVP9I7tjrDqLpUKnAn3Fp8Zo"
SUPABASE_URL = None
SUPABASE_KEY = None

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch first 20 synced product IDs
resp = (
    supabase
    .table("products")
    .select("id")
    .eq("sync_enable", True)
    .order("id", desc=False)  # ascending via desc=False
    .range(0, 19)
    .execute()
)

print([row["id"] for row in resp.data])
