from random import randint

import Password.PasswordStrings as tokens
from abc import ABC, abstractmethod

import requests

from data_requests.TimeManager import convert_data_to_unix
from database.Candle import CandleCrypto

log = False

def change_json_candles_for_candle_objects(candles_data, resolution, symbol):
    candles_data = candles_data.json()

    #expection very ofter solve it by try/catch and retry with somme deleay
    received_candles_data_length = len(candles_data['c'])
    if received_candles_data_length == 0:
        return
    candle_objects = []
    for index in range(received_candles_data_length):
        temp_candle = CandleCrypto(candles_data['o'][index], candles_data['c'][index], candles_data['h'][index],
                                   candles_data['l'][index], candles_data['v'][index], candles_data['t'][index],
                                   resolution, symbol)
        candle_objects.append(temp_candle)
    return candle_objects


class ApiManager(ABC):
    def __init__(self):
        self.keys = ApiKeyManager()

    @abstractmethod
    def get_values_for_symbol(self, symbol, resolution, from_date, to_date):
        pass

    @abstractmethod
    def get_all_symbols_for_market(self, market):
        pass


class ApiKeyManager:
    def __init__(self):
        self.api_keys = [tokens.token1, tokens.token2, tokens.token3, tokens.token4]

    def get_api_key(self):
        key = randint(0, len(self.api_keys)-1)
        self.api_keys.append(self.api_keys.pop(key))
        return self.api_keys[key]


class CryptoApiManager(ApiManager):

    def get_values_for_symbol(self, symbol, resolution, from_date, to_date):
        parameters = {
            "symbol": symbol,
            "resolution": resolution,
            "from": convert_data_to_unix(from_date),
            "to": convert_data_to_unix(to_date),
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
        return response

    def get_all_symbols_for_market(self, market="binance"):
        symbols = []
        parameters = {
            "exchange": market,
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/crypto/symbol?", params=parameters)
        for symbol in response.json():
            symbols.append(symbol["symbol"])
        return symbols


class StockApiManager(ApiManager):

    def get_values_for_symbol(self, symbol, resolution, from_date, to_date):
        # US index only
        arguments = {
            "symbol": symbol,
            "resolution": resolution,
            "from": convert_data_to_unix(from_date),
            "to": convert_data_to_unix(to_date),
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/stock/candle?", params=arguments)
        if log:
            print(response.request.url)
        return response

    def get_all_symbols_for_market(self, market="US"):
        symbols = []
        arguments = {
            "exchange": market,
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/stock/symbol?", params=arguments)
        json_response = response.json()
        for symbol in json_response:
            symbols.append(symbol["symbol"])
        return symbols

    # consider it when all pattern recognitions are done as alternative for GWP data provider
    def get_stock_values_marketstack(self, access_key, symbols, from_date, to_date):
        # eod daily only
        arguments = {
            "access_key": access_key,
            "symbols": symbols,  # CDR.XWAR
            "from": convert_data_to_unix(from_date),  # 2020-04-01
            "to": convert_data_to_unix(to_date)}
        response = requests.get("ttp://api.marketstack.com/v1/eod?", params=arguments)
        return response
