import os
import time
import pickle
from datetime import datetime
from shutil import copyfile

from data_requests.CryptoRequests import get_crypto_values, change_candles_to_candle_objects
from data_requests.TimeManager import is_comparable_with_current_time, convert_unix_to_data

log = False

class Database:
    def __init__(self):
        #   {{crypto_currency_symbol:{resolution:{fiat:[]}}}}
        self.main_container = {}
        self.load_database()
        self.read_crypto_from_file()
        self.update_data_base()

    def read_crypto_from_file(self):
        file = 'data\crypto_data.txt'
        if os.path.isfile(file) and os.path.getsize(file) > 0:
            with open(file) as input_data:
                data = input_data.read()
                symbols = data.split("\n")
            fiat_symbol = ""
            for symbol in symbols:
                if "USDT" in symbol:
                    fiat_symbol = "USDT"
                elif "USD" in symbol:
                    fiat_symbol = "USD"
                elif "EUR" in symbol:
                    fiat_symbol = "EUR"
                crypto_currency_symbol = symbol.replace(fiat_symbol, "")
                self.add_to_data_base(crypto_currency_symbol, fiat_symbol)

    def add_to_data_base(self, crypto_currency_symbol, fiat_symbol):
        if crypto_currency_symbol in self.main_container and \
                fiat_symbol in self.main_container[crypto_currency_symbol]["M"]:
            return
        if crypto_currency_symbol not in self.main_container:
            # add "1": {}, "5": {} to extend resolution
            self.main_container[crypto_currency_symbol] = {"15":{},"30": {},"60": {}, "D": {},
                                                           "W": {},
                                                           "M": {}}
        for resolution in self.main_container[crypto_currency_symbol]:
            if len(self.main_container[crypto_currency_symbol][resolution]) == 0:
                self.main_container[crypto_currency_symbol][resolution] = {fiat_symbol: []}
            else:
                self.main_container[crypto_currency_symbol][resolution][fiat_symbol] = []
            candles_json = get_crypto_values(crypto_currency_symbol, resolution, fiat_symbol,
                                             "1/01/2017", int(time.time()))
            candle_objects = change_candles_to_candle_objects(candles_json)
            for candle in candle_objects:
                self.main_container[crypto_currency_symbol][resolution][fiat_symbol].append(candle)
        self.save_database()

    def update_data_base(self):
        for currency_symbol in self.main_container:
            if log: print(currency_symbol)
            self.update_candles_on_currency(currency_symbol)

    def update_candles_on_currency(self, crypto_currency_symbol):
        latest_date_dict = self.get_latest_dates(crypto_currency_symbol)
        if log: print(latest_date_dict)
        if latest_date_dict is None or len(latest_date_dict) == 0:
            return
        # {'15': {'USDT': 1524386700}, '30': {'USDT': 1524835800}, '60': {'USDT': 1525734000}, 'D': {'USDT': 1567036800}, 'W': {'USDT': 1632700800}, 'M': {'USDT': 1633046400}}
        for resolution in latest_date_dict:
            for fiat_currency in latest_date_dict[resolution]:
                finished = False
                while not finished:
                    if not is_comparable_with_current_time(latest_date_dict[resolution][fiat_currency], resolution):
                        candles_json = get_crypto_values(crypto_currency_symbol, resolution, fiat_currency,
                                                         latest_date_dict[resolution][fiat_currency],
                                                         datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                        if candles_json is not None:
                            candle_objects = change_candles_to_candle_objects(candles_json)
                            for candle in candle_objects:
                                self.main_container[crypto_currency_symbol][resolution][fiat_currency].append(candle)
                        if log == True:
                            print(crypto_currency_symbol +" "+ resolution)
                            print(len(self.main_container[crypto_currency_symbol][resolution][fiat_currency]))
                            print(self.main_container[crypto_currency_symbol][resolution][fiat_currency][-1].time)
                        latest_date_dict = self.get_latest_dates(crypto_currency_symbol)
                    else:
                        #It downloand current value candle on the stock. It is removed here to avoid any issues
                        self.main_container[crypto_currency_symbol][resolution][fiat_currency].pop(-1)
                        finished = True
            self.save_database()

    def get_latest_dates(self, crypto_currency_symbol):
        symbol_data = self.main_container[crypto_currency_symbol]
        latest_date_dict = {}
        if len(symbol_data) > 0:
            for resolution in symbol_data:
                latest_date_dict[resolution] = {}
                if len(symbol_data[resolution]) > 0:
                    for fiat, candle in symbol_data[resolution].items():
                        latest_date_dict[resolution].update({fiat: candle[-1].time})
            # {'15': {'USDT': 1524386700}, '30': {'USDT': 1524835800}, '60': {'USDT': 1525734000}, 'D': {'USDT': 1567036800}, 'W': {'USDT': 1632700800}, 'M': {'USDT': 1633046400}}
            return latest_date_dict
        return

    def save_database(self):
        with open('data\database.data', 'wb') as database:
            pickle.dump(self.main_container, database)
            copyfile('data\database.data', 'data\\backup.data')

    def load_database(self):
        try:
            file = 'data\database.data'
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                with open(file, 'rb') as database:
                    self.main_container = pickle.load(database)
        except EOFError:
            file = 'data\\backup.data'
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                with open(file, 'rb') as database:
                    self.main_container = pickle.load(database)
