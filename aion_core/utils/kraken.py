
"""
📄 Bestand: kraken.py
🔍 Doel: Ophalen en formatteren van OHLC-data van Kraken (dict-structuur)
🧩 Gebruikt door: context, backtest, strategieën
📦 Behoort tot: aion_core/utils
"""

import requests
import pandas as pd
import time
from aion_core.utils.logger import logger

BASE_COLUMNS = [
    'time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_volume', 'trades', 'low2', 'high2', 'ignore'
]

def get_ohlc_data(pair='SOLUSDT', interval=15, since=None):
    url = "https://api.kraken.com/0/public/OHLC"
    params = {'pair': pair, 'interval': interval}
    if since:
        params['since'] = since

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if 'error' in data and data['error']:
            raise Exception(f"Kraken API error: {data['error']}")

        result_key = list(data['result'].keys())[0]
        raw_data = data['result'][result_key]

        df = pd.DataFrame(raw_data)
        n_cols = df.shape[1]
        if n_cols > len(BASE_COLUMNS):
            logger.warning(f"[get_ohlc_data] Kraken gaf {n_cols} kolommen — onbekend formaat")
            colnames = [f"col{i}" for i in range(n_cols)]
        else:
            colnames = BASE_COLUMNS[:n_cols]

        df.columns = colnames
        df = df.astype(float)
        return df

    except Exception as e:
        logger.warning(f"[get_ohlc_data] Fout bij ophalen van Kraken: {e}")
        return pd.DataFrame()

def get_ohlc_latest(symbol: str, timeframe: str):
    try:
        pair = symbol.replace("/", "")

        if timeframe.endswith("m"):
            interval = int(timeframe.replace("m", ""))
        elif timeframe.endswith("h"):
            interval = int(timeframe.replace("h", "")) * 60
        elif timeframe.endswith("d"):
            interval = int(timeframe.replace("d", "")) * 1440
        else:
            raise ValueError(f"Ongeldig timeframe formaat: {timeframe}")

        df = get_ohlc_data(pair=pair, interval=interval)
        if df.empty:
            raise ValueError("Lege candle data ontvangen")

        row = df.iloc[-1]
        return row.to_dict()

    except Exception as e:
        logger.warning(f"[get_ohlc_latest] Fout: {e}")
        return None
