
"""
📄 Bestand: bias_tracker.py
🔍 Doel: Lokale bias-tracking + directe upload naar Supabase
🧩 Gebruikt door: candle_scheduler, context_builder
📦 Behoort tot: aion_core/extensions
🧠 Verwacht implementatie van: supabase_writer.py
"""

import os
import time
from datetime import datetime
from aion_core.extensions.supabase_writer import upload_record

class BiasTracker:
    def __init__(self):
        self.biases = {}

    def update_bias(self, timeframe: str, bias: str):
        """
        Update lokaal en direct uploaden naar Supabase bias_tracker tabel
        """
        self.biases[timeframe] = bias
        self.upload_bias(timeframe, bias)

    def get_bias(self, timeframe: str) -> str:
        """
        Ophalen van huidige bias voor gegeven timeframe
        """
        return self.biases.get(timeframe, "unknown")

    def upload_bias(self, timeframe: str, bias: str):
        """
        Upload bias entry naar Supabase
        """
        try:
            data = {
                "timeframe": timeframe,
                "bias": bias,
                "timestamp": datetime.utcnow().isoformat()
            }
            upload_record("bias_tracker", data)
            print(f"[BiasTracker] Bias voor {timeframe} succesvol geupload.")
        except Exception as e:
            print(f"[BiasTracker ERROR] Bias upload mislukt: {e}")

# Demo gebruik in candle scheduler
if __name__ == "__main__":
    tracker = BiasTracker()
    
    # Stel je candle scheduler detecteert nieuwe candles per timeframe:
    def on_new_candle(timeframe, market_data):
        calculated_bias = calculate_bias_from_market(market_data)
        tracker.update_bias(timeframe, calculated_bias)

    def calculate_bias_from_market(market_data):
        # Simpele bias logica: bullish als close > open, anders bearish
        return "bullish" if market_data.get("close", 0) > market_data.get("open", 0) else "bearish"

    # Simulatie van nieuwe candles
    on_new_candle("1h", {"open": 87.0, "close": 88.2})
    on_new_candle("4h", {"open": 89.5, "close": 88.0})

    print(tracker.get_bias("1h"))
