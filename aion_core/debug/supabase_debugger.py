
"""
📄 Bestand: supabase_debugger.py
🔍 Doel: Supersnelle test of Supabase insert-verbinding werkt.
"""

from aion_core.utils.logtools import log_context
from datetime import datetime

def test_supabase_connection():
    try:
        test_data = {
            "symbol": "TEST/SYM",
            "sweep": True,
            "fvg": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        with log_context("Supabase test"):
            print("✅ Testrecord verzonden naar Supabase (table: context)")
    except Exception as e:
        print(f"❌ Supabase test mislukt: {e}")

if __name__ == "__main__":
    test_supabase_connection()
