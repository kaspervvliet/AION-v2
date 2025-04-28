"""
📄 Bestand: force_logger.py
🔍 Doel: Force insert test via Edge Function
🧩 Gebruikt door: AION Debugging Tools
📦 Behoort tot: aion_core/debug
🧠 Verwacht implementatie van: insert_via_edge
"""

from aion_core.database.supabase_logger import insert_via_edge
import datetime

def force_insert():
    now = datetime.datetime.now(datetime.UTC).isoformat()
    payload = {
        "symbol": "SOL/USDT",
        "sweep": True,
        "fvg": False,
        "timestamp": now,
    }
    response = insert_via_edge("context", payload)
    print(response)

if __name__ == "__main__":
    print("🚀 Force insert gestart...")
    force_insert()
