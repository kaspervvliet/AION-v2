"""
📄 Bestand: supabase_reader.py
🔍 Doel: Ophalen van recente trades, signals of metrics uit Supabase
🧩 Gebruikt door: adaptive_strategy_selector, strategy_executor, streamlit_ui
📦 Behoort tot: aion_core/database
🧠 Verwacht: geldige Supabase-verbinding en tabellen
"""

from aion_core.supabase_client import supabase
from typing import List
from datetime import datetime, timedelta

def load_recent_trades(limit: int = 25) -> List[dict]:
    response = (
        supabase.table("trades")
        .select("*")
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )
    if hasattr(response, "data") and response.data:
        return response.data
    return []

def load_signals_since(minutes_back: int = 60) -> List[dict]:
    since = (datetime.utcnow() - timedelta(minutes=minutes_back)).isoformat()
    response = (
        supabase.table("signals")
        .select("*")
        .gte("timestamp", since)
        .order("timestamp", desc=True)
        .execute()
    )
    if hasattr(response, "data") and response.data:
        return response.data
    return []
