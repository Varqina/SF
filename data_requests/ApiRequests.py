import Password.PasswordStrings as tokens
from abc import ABC, abstractmethod

import requests

from data_requests.TimeManager import convert_data_to_unix
from database.Candle import CandleCrypto


class ApiManager(ABC):
    def __init__(self):
        self.keys = ApiKeyManager()

    @abstractmethod
    def get_values_for_symbol(self, symbol, resolution, from_date, to_date):
        pass

    @abstractmethod
    def change_json_candles_for_candle_objects(self, candles_json, resolution, symbol):
        pass

    @abstractmethod
    def get_all_symbols_for_exchange(self, market):
        pass


class ApiKeyManager:
    def __init__(self):
        self.api_keys = [tokens.token1, tokens.token2, tokens.token3]

    def get_api_key(self):
        self.api_keys.append(self.api_keys.pop(0))
        return self.api_keys[0]


class CryptoApiManager(ApiManager):

    def get_values_for_symbol(self, symbol, resolution, from_date, to_date):
        parameters = {
            "symbol": symbol,
            "resolution": resolution,
            "from": convert_data_to_unix(from_date),
            "to": convert_data_to_unix(to_date),
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
        json_response = response.json()
        return json_response

    def change_json_candles_for_candle_objects(self, candles_json, resolution, symbol):
        received_candles = len(candles_json['c'])
        if received_candles == 0:
            return
        candle_objects = []
        for candle in range(received_candles):
            if len(candle_objects) > 0:
                previously_closed = candle_objects[-1].close_candle
            temp_candle = CandleCrypto(candles_json['o'][candle], candles_json['c'][candle], candles_json['h'][candle],
                                       candles_json['l'][candle], candles_json['v'][candle], candles_json['t'][candle],
                                       resolution, symbol)
            candle_objects.append(temp_candle)
        return candle_objects

    def get_all_symbols_for_market(self, market):
        symbols = []
        parameters = {
            "exchange": market,
            "token": self.keys.get_api_key()}
        response = requests.get("https://finnhub.io/api/v1/crypto/symbol?", params=parameters)
        for symbol in response.json():
            symbols.append(symbol["symbol"])
        return symbols
