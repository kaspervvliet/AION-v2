from aion_core.utils import safe_io

"""
📄 Bestand: performance_tracker.py
🔍 Doel: Tracking van uitgevoerde trades om prestaties van strategieën te evalueren
🧩 Gebruikt door: Adaptive Engine, Behavior Engine
📦 Behoort tot: aion_core/performance/
🧠 Verwacht implementatie van: Signaallogging, RR evaluatie, prestatieclassificatie
"""

import os
import json
from datetime import datetime

PERFORMANCE_LOG = "performance_log.json"  # Later verplaatsen naar Supabase opslag

class PerformanceTracker:
    def __init__(self):
        self.trades = []
        self.load_existing()

    def load_existing(self):
        if os.path.exists(PERFORMANCE_LOG):
            # replaced
# with open(PERFORMANCE_LOG, "r") as f:
                self.trades = safe_io.read_json(STATE_PATH)

    def save(self):
        # replaced
# with open(PERFORMANCE_LOG, "w") as f:
            safe_io.write_json(PERFORMANCE_LOG, self.trades, indent=4)

    def log_trade(self, signal: dict, result: dict):
        trade_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "strategy": signal.get("strategy_name", "unknown"),
            "action": signal.get("action", "unknown"),
            "sl_pct": signal.get("sl_pct"),
            "tp_pct": signal.get("tp_pct"),
            "outcome": result.get("outcome"),  # "win" / "loss"
            "rr_achieved": result.get("rr_achieved", 0)
        }
        self.trades.append(trade_record)
        self.save()

    def get_performance_summary(self):
        wins = [t for t in self.trades if t["outcome"] == "win"]
        losses = [t for t in self.trades if t["outcome"] == "loss"]
        total = len(self.trades)
        winrate = len(wins) / total * 100 if total else 0
        avg_rr = sum(t["rr_achieved"] for t in self.trades) / total if total else 0

        return {
            "total_trades": total,
            "winrate_pct": winrate,
            "average_rr": avg_rr,
            "wins": len(wins),
            "losses": len(losses)
        }

# Demo gebruik
if __name__ == "__main__":
    tracker = PerformanceTracker()
    # Simulatie van een gelogde trade
    tracker.log_trade({
        "strategy_name": "RSI Sweep",
        "action": "buy",
        "sl_pct": 0.01,
        "tp_pct": 0.02
    }, {
        "outcome": "win",
        "rr_achieved": 2.0
    })
    print(tracker.get_performance_summary())
