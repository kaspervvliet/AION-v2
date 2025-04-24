
import requests
import pandas as pd
from datetime import datetime

def get_ohlc_data(pair='SOLUSDT', interval=15, since=None):
    """
    Haalt OHLC-data op van Kraken API.
    :param pair: handels-paar string (bv. 'SOLUSDT')
    :param interval: timeframe in minuten
    :param since: unix timestamp in seconden
    :return: DataFrame met OHLC-data
    """
    url = f"https://api.kraken.com/0/public/OHLC"
    params = {
        'pair': pair,
        'interval': interval,
    }
    if since:
        params['since'] = since

    response = requests.get(url, params=params)
    data = response.json()

    if 'error' in data and data['error']:
        raise Exception(f"Kraken API error: {data['error']}")

    result_key = list(data['result'].keys())[0]
    raw_data = data['result'][result_key]

    df = pd.DataFrame(raw_data, columns=[
        'time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
    ])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df = df.astype(float)
    return df
