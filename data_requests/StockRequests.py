import requests as requests
from data_requests.TimeManager import convert_data_to_unix
from database.Candle import CandleCrypto, CandleStock
import Password.PasswordStrings as tokens


class ApiKeyManager:
    def __init__(self):
        self.api_keys = [tokens.token1, tokens.token2, tokens.token3]

    def get_api_key(self):
        self.api_keys.append(self.api_keys.pop(0))
        return self.api_keys[0]


keys = ApiKeyManager()


def get_stock_values_finehub(symbol, resolution, from_date, to_date):
    # US index only
    arguments = {
        "symbol": symbol,
        "resolution": resolution,
        "from": convert_data_to_unix(from_date),
        "to": convert_data_to_unix(to_date),
        "token": keys.get_api_key()}
    response = requests.get("https://finnhub.io/api/v1/stock/candle?", params=arguments)
    json_response = response.json()
    return json_response


def get_stock_values_marketstack(access_key, symbols, from_date, to_date):
    # eod daily only
    arguments = {
        "access_key": access_key,
        "symbols": symbols,  # CDR.XWAR
        "from": convert_data_to_unix(from_date),  # 2020-04-01
        "to": convert_data_to_unix(to_date)}

    response = requests.get("ttp://api.marketstack.com/v1/eod?", params=arguments)
    json_response = response.json()
    return json_response


def change_stock_json_candles_to_candle_objects(candles_json, resolution, symbol):
    received_candles = len(candles_json['c'])
    if received_candles == 0:
        return
    candle_objects = []
    for candle in range(received_candles):
        if len(candle_objects) > 0:
            previously_closed = candle_objects[-1].close_candle
        temp_candle = CandleStock(candles_json['o'][candle], candles_json['c'][candle], candles_json['h'][candle],
                                  candles_json['l'][candle], candles_json['v'][candle], candles_json['t'][candle],
                                  resolution, symbol)
        candle_objects.append(temp_candle)
    return candle_objects
