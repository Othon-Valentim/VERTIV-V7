import os
from supabase import create_client, Client

# These should be loaded from environment variables
# In Cloud Run: set via --set-env-vars
# Local: set in .env or passed when running
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

_client: Client = None

def get_supabase_client() -> Client:
    global _client
    if _client:
        return _client
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        # In a real enterprise app, we might raise an error here.
        # For this phase, we'll log a warning and return a client that might fail if used.
        # Or better, we raise an error to fail fast.
        print("WARNING: SUPABASE_URL or SUPABASE_KEY is missing. Database operations will fail.")
    
    _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client
