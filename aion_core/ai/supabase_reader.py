from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")  # via Render environment variables
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # via Render environment variables

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_recent_logs(strategy_name: str, limit: int = 10):
    response = (
        supabase.table("strategy_logs")
        .select("strategy, bias, entry_type, sl_hit, tp_hit, timestamp")
        .eq("strategy", strategy_name)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data
