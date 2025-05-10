"""
📄 Bestand: supabase_performance_helper.py
🔍 Doel: Zet performance-resultaten om naar Supabase-logformat
🧩 Gebruikt door: strategy_tester, evaluator
📦 Behoort tot: aion_core/extensions/
🧠 Verwacht implementatie van: summarize_results()
"""

import pandas as pd
from typing import Dict, Any

def summarize_results(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Converteert testresultaten naar samenvatting voor Supabase.
    """
    if df.empty:
        return {
            "total_trades": 0,
            "total_win": 0,
            "winrate": 0.0,
            "avg_rr": 0.0,
            "best": 0.0,
            "worst": 0.0,
            "timestamp": pd.Timestamp.now().isoformat()
        }

    total = len(df)
    wins = len(df[df["rr"] >= 1.5])
    summary = {
        "total_trades": total,
        "total_win": wins,
        "winrate": round(100 * wins / total, 2),
        "avg_rr": round(df["rr"].mean(), 2),
        "best": round(df["rr"].max(), 2),
        "worst": round(df["rr"].min(), 2),
        "timestamp": pd.Timestamp.now().isoformat()
    }
    return summary

if __name__ == "__main__":
    test_df = pd.DataFrame({"rr": [1.0, 2.0, 0.8, 2.5, 1.6]})
    print(summarize_results(test_df))
