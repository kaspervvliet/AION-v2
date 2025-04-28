
"""
📄 Bestand: supabase_debugger.py
🔍 Doel: Supersnelle test of Supabase insert-verbinding werkt.
"""

from aion_core.database.supabase_logger import log_context
from datetime import datetime

def test_supabase_connection():
    try:
        test_data = {
            "symbol": "TEST/SYM",
            "sweep": True,
            "fvg": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        log_context(test_data)
        print("✅ Testrecord verzonden naar Supabase (table: context)")
    except Exception as e:
        print(f"❌ Supabase test mislukt: {e}")

if __name__ == "__main__":
    test_supabase_connection()
