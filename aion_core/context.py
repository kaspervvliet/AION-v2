"""
📄 Bestand: context.py
🔍 Doel: Houdt gedeelde sessiecontext bij zoals pricefeed, alerts en accountinfo
🧩 Gebruikt door: strategie-modules, core logic, alerts
📦 Behoort tot: aion_core/
"""

from aion_core.supabase_client import get_context_from_supabase, push_context_to_supabase

class AIONContext:
    def __init__(self, symbol, timeframe, alerts_enabled=True):
        self.symbol = symbol
        self.timeframe = timeframe
        self.alerts_enabled = alerts_enabled
        self.candle_data = []
        self.account_info = {}

    def load_from_supabase(self):
        data = get_context_from_supabase(self.symbol, self.timeframe)
        self.candle_data = data.get("candle_data", [])
        self.account_info = data.get("account_info", {})

    def push_to_supabase(self):
        push_context_to_supabase(self.to_dict())

    def update_candles(self, new_candles):
        self.candle_data = new_candles
        self.push_to_supabase()

    def get_latest_price(self):
        if self.candle_data and len(self.candle_data[-1]) >= 5:
            return self.candle_data[-1][4]  # Close
        return None

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "candle_data": self.candle_data,
            "account_info": self.account_info
        }

    @classmethod
    def from_supabase(cls, symbol, timeframe):
        inst = cls(symbol, timeframe)
        inst.load_from_supabase()
        return inst
