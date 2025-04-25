"""
📄 Bestand: telegram_alerts.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: telegram_alerts.py
🧠 Laatst geüpdatet: 2025-04-25
"""


"""
📄 Bestand: telegram_alerts.py
🔍 Doel: Versturen van muteable Telegram alerts
🧩 Gebruikt door: alert systemen en signal pushers
📦 Behoort tot: root
🧠 Verwacht implementatie van: send_alert, mute via .env
"""

import logging
logger = logging.getLogger(__name__)

import requests
from aion_core import config

def format_signal_message(signal: dict) -> str:
    setup = signal.get("setup", {})
    rr = signal.get("rr", 0)
    expl = signal.get("explanation", "")

    msg = f"""
📣 *AION Signaalvoorstel*

*Bias:* `{setup.get('bias')}`  
*BOS:* `{setup.get('has_bos')}`  *FVG:* `{setup.get('has_fvg')}`  *RSI:* `{setup.get('rsi')}`
*RR:* `{rr:.2f}`

```\n{expl}```
    """
    return msg.strip()

def send_telegram_signal(signal: dict):
    BOT_TOKEN = config.AION_TELEGRAM_BOT
    CHAT_ID = config.AION_TELEGRAM_CHAT

    if not BOT_TOKEN or not CHAT_ID:
        logger.info("[TELEGRAM] ❌ Bot token of chat ID ontbreekt.")
        return

    msg = format_signal_message(signal)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    res = requests.post(url, json=payload)
    logger.info("[TELEGRAM] Verzonden:", res.status_code)
