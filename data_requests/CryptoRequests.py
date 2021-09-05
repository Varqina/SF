import requests as requests
from data_requests.TimeManager import convert_data_to_unix
from database.Candle import Candle
from database.Decorators import measure_time
import Password.PasswordStrings as tokens


class ApiManager:
    def __init__(self):
        self.api_keys = [tokens.token1, tokens.token2, tokens.token3]

    def get_api_key(self):
        self.api_keys.append(self.api_keys.pop(0))
        return self.api_keys[0]


keys = ApiManager()


def get_crypto_values(symbol, resolution, from_date, to_date):
    symbol = get_crypto_symbol(symbol)
    parameters = {
        "symbol": symbol,
        "resolution": resolution,
        "from": convert_data_to_unix(from_date),
        "to": convert_data_to_unix(to_date),
        "token": keys.get_api_key()}
    response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
    return response.json()


def get_all_crypto_symbols(exchange="binance"):
    symbols = []
    parameters = {
        "exchange": exchange,
        "token": keys.get_api_key()}
    response = requests.get("https://finnhub.io/api/v1/crypto/symbol?", params=parameters)
    for symbol in response.json():
        symbols.append(symbol["symbol"])
    return symbols


def get_crypto_symbol(symbol, exchange="binance"):
    symbol = symbol.lower()
    all_symbol_list = get_all_crypto_symbols(exchange)
    symbols = []
    for symbol_value in all_symbol_list:
        if symbol in symbol_value.lower():
            symbols.append(symbol_value)
    if len(symbols) == 1:
        return symbols[0]
    else:
        return symbols


def change_candles_to_candle_objects(candles_json):
    received_candles = len(candles_json['c'])
    if received_candles == 0:
        return
    candle_objects = []
    for candle in range(received_candles):
        temp_candle = Candle(candles_json['c'][candle], candles_json['o'][candle], candles_json['h'][candle],
                             candles_json['l'][candle], candles_json['v'][candle], candles_json['t'][candle])
        candle_objects.append(temp_candle)
    return candle_objects
