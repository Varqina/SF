import requests as requests
import Password.PasswordStrings as Password
import json

from data_requests.UnixConverter import convert_data_to_unix


def get_crypto_value(symbol, resolution, from_date, to_date):
    parameters = {
        "symbol": symbol,
        "resolution": resolution,
        "from": convert_data_to_unix(from_date),
        "to": convert_data_to_unix(to_date),
        "token": Password.token}
    response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
    #print(response.url)
    return response.json()


def get_all_crypto_symbols(exchange="binance"):
    symbol_list = []
    parameters = {
        "exchange": exchange,
        "token": Password.token}
    response = requests.get("https://finnhub.io/api/v1/crypto/symbol?", params=parameters)
    for symbol in response.json():
        symbol_list.append(symbol["symbol"])
    return symbol_list


def get_crypto_symbol(symbol, exchange="binance"):
    symbol = symbol.lower()
    all_symbol_list = get_all_crypto_symbols(exchange)
    symbol_list = []
    for symbol_value in all_symbol_list:
        if symbol in symbol_value.lower():
            symbol_list.append(symbol_value)
    if len(symbol_list) == 1:
        return symbol_list[0]
    else:
        return symbol_list
