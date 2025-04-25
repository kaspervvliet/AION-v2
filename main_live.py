"""
📄 Bestand: main_live.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: main_live.py
🧠 Laatst geüpdatet: 2025-04-25
"""


"""
📄 Bestand: main_live.py
🔍 Doel: Start live trading loop met signalen
🧩 Gebruikt door: deployment op Render / real-time strategieën
📦 Behoort tot: root
🧠 Verwacht implementatie van: fetch, signalering, alerts
"""

import logging
logger = logging.getLogger(__name__)
from aion_core.context.context import AIONContext
from aion_core.context.market_data import get_htf_ltf_candles

def live_loop():
    pair = "SOL/USDT"
    candles = get_htf_ltf_candles(pair)
    ltf = candles["ltf"]
    latest_candle = ltf[-1]

    logger.info("🔁 Laatste 15m candle (live loop):", latest_candle)