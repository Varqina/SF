import time

import requests as requests
import Password.PasswordStrings as list_of_strings
import json

from data_requests.TimeManager import convert_data_to_unix
from database.Candle import Candle
from database.Decorators import measure_time


@measure_time
def get_crypto_values(symbol, resolution, from_date, to_date):
    symbol = get_crypto_symbol(symbol)
    parameters = {
        "symbol": symbol,
        "resolution": resolution,
        "from": convert_data_to_unix(from_date),
        "to": convert_data_to_unix(to_date),
        "token": list_of_strings.token}
    response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
    return response.json()


@measure_time
def get_all_crypto_symbols(exchange="binance"):
    symbols = []
    parameters = {
        "exchange": exchange,
        "token": list_of_strings.token}
    response = requests.get("https://finnhub.io/api/v1/crypto/symbol?", params=parameters)
    for symbol in response.json():
        symbols.append(symbol["symbol"])
    return symbols


@measure_time
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
