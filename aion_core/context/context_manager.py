
"""
📄 Bestand: context_manager.py
🔍 Doel: Bouwt consistente context voor strategieën en logging
🧩 Gebruikt door: strategy_executor, kernel, signal_engine
📦 Behoort tot: aion_core/context
🧠 Verwacht implementatie van: get_fresh_ohlc, get_htf_bias, is_bias_consistent
"""

import time
from aion_core.utils.candle_manager import get_fresh_ohlc
from aion_core.knowledge.htf_bias_checker import get_htf_bias
from aion_core.knowledge.mtf_bias_checker import is_bias_consistent

def get_context(symbol: str) -> dict:
    """
    Bouwt een volledige context voor het opgegeven symbool.
    Inclusief bias-analyse op 15m, 1h, 4h, 1d, 1w.
    """

    tf_bias_keys = {
        "15m": "bias_15m",
        "1h": "bias_1h",
        "4h": "bias_4h",
        "1d": "bias_1d",
        "1w": "bias_1w"
    }

    context = {
        "symbol": symbol,
        "timestamp": int(time.time()),
        "price": None,
        "bias_consistent": None,
    }

    all_biases = {}

    for tf, ctx_key in tf_bias_keys.items():
        df = get_fresh_ohlc(symbol, tf)
        if df is not None and not df.empty:
            context[f"ohlc_{tf}"] = df
            close = df.iloc[-1]["close"]
            context["price"] = close
            bias = get_htf_bias(symbol)
            context[ctx_key] = bias
            all_biases[tf] = bias

    # Voeg bias consistentie toe (alleen voor MTF-schakels)
    mtf_subset = {k: v for k, v in all_biases.items() if k in ["15m", "1h", "4h"]}
    if mtf_subset:
        context["bias_consistent"] = is_bias_consistent(mtf_subset, symbol=symbol)

    # Voeg biasestructuur toe voor gewogen analyse
    context["biases"] = all_biases
    context["bias_score"] = compute_bias_score(all_biases)

    return context

def compute_bias_score(biases: dict) -> int:
    """
    Bereken gewogen bias-score: positief = bullish overwicht
    """
    weights = {
        "1w": 5,
        "1d": 4,
        "4h": 3,
        "1h": 2,
        "15m": 1,
    }
    score = 0
    for tf, bias in biases.items():
        weight = weights.get(tf, 1)
        if bias == "bullish":
            score += weight
        elif bias == "bearish":
            score -= weight
    return score
