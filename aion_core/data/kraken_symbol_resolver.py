"""
📄 Bestand: kraken_symbol_resolver.py
🔍 Doel: Vertaal externe symbolen zoals BTC/USDT naar Kraken API-pair strings
🧩 Gebruikt door: dataservices, feeds
📦 Behoort tot: aion_core/data
🧠 Verwacht implementatie van: resolve_kraken_pair(symbol: str)
"""

def resolve_kraken_pair(symbol: str) -> str:
    mapping = {
        "BTC/USDT": "XBTUSDT",
        "ETH/USDT": "ETHUSDT",
        "SOL/USDT": "SOLUSDT",
        "ADA/USDT": "ADAUSDT",
        "XRP/USDT": "XRPUSDT",
        "DOT/USDT": "DOTUSDT",
        "LINK/USDT": "LINKUSDT",
        "DOGE/USDT": "DOGEUSDT",
    }
    return mapping.get(symbol, symbol.replace("/", ""))
