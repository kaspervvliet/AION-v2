"""
📄 Bestand: kraken.py
🔍 Doel: Ophalen en formatteren van OHLC-data van Kraken
🧩 Gebruikt door: context, backtest, strategieën
📦 Behoort tot: aion_core/utils
🧠 Klaar voor multi-pair & variable column formats
"""

import requests
import pandas as pd
import time
from aion_core.utils.logger import logger

def get_ohlc_data(pair='SOLUSDT', interval=15, since=None):
    """
    Haalt OHLC-data op van de Kraken API.

    :param pair: Handels-paar string (bv. 'SOLUSDT')
    :param interval: Timeframe in minuten (bv. 15)
    :param since: Optioneel vanaf-timestamp (unix)
    :return: Pandas DataFrame met 6 genormaliseerde kolommen
    """
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
        if df.shape[1] < 6:
            raise ValueError(f"Kraken gaf te weinig kolommen ({df.shape[1]})")
        elif df.shape[1] > 6:
            logger.warning(f"[get_ohlc_data] Kraken gaf {df.shape[1]} kolommen — alleen eerste 6 gebruikt.")

        df = df.iloc[:, :6]
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        df = df.astype(float)
        return df

    except Exception as e:
        logger.warning(f"[get_ohlc_data] Fout bij ophalen van Kraken: {e}")
        return pd.DataFrame()

def get_ohlc_latest(symbol: str, timeframe: str):
    """
    Retourneert de laatste candle als lijst: [timestamp, o, h, l, c, v]
    """
    try:
        pair = symbol.replace("/", "")
        interval = int(timeframe.replace("m", ""))

        df = get_ohlc_data(pair=pair, interval=interval)
        if df.empty:
            raise ValueError("Lege candle data ontvangen")

        last = df.iloc[-1]
        now = int(time.time())
        candle_age = now - int(last['time'])
        if candle_age > interval * 60:
            logger.warning(f"[get_ohlc_latest] Oude candle: {candle_age}s oud")

        return [
            int(last['time']),
            float(last['open']),
            float(last['high']),
            float(last['low']),
            float(last['close']),
            float(last['volume'])
        ]

    except Exception as e:
        logger.warning(f"[get_ohlc_latest] Fout: {e}")
        return None
