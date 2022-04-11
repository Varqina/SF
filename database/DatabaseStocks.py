import os
import time
import pickle
from datetime import datetime
from shutil import copyfile

from data.DataManager import load_database, read_data_from_file, save_database
from data_requests.CryptoRequests import get_crypto_values, change_candles_to_candle_objects
from data_requests.StockRequests import get_stock_values_finehub, change_stock_json_candles_to_candle_objects
from data_requests.TimeManager import is_comparable_with_current_time, convert_unix_to_data

log = False


class DatabaseStock:
    def __init__(self):
        #   {{stock_symbol:{resolution:[]}}}
        self.market_name = "stock"
        self.main_container = load_database(self.market_name)
        stock_indexes = read_data_from_file(self.market_name)
        if len(self.main_container) < len(stock_indexes):
            self.add_to_data_base(stock_indexes)
        self.update_database()

    def add_to_data_base(self, stock_indexes):
        for index in stock_indexes:
            if index not in self.main_container:
                self.main_container[index] = {"15": [], "30": [], "60": [], "D": [], "W": [], "M": []}
        save_database(self.market_name, self.main_container)

    def update_database(self):
        for index in self.main_container:
            if log:
                print(index)
            self.update_candles_on_index(index)

    def get_latest_dates(self, index):
        index_data = self.main_container[index]
        latest_date_dict = {}
        if len(index_data) > 0:
            for resolution in index_data:
                latest_date_dict[resolution] = index_data[resolution][-1]
        return latest_date_dict

    def update_candles_on_index(self, index):
        latest_candles_dict = self.get_latest_dates(index)
        if log:
            print(latest_candles_dict)
        if latest_candles_dict is not None and len(latest_candles_dict) > 0:
            for resolution in latest_candles_dict:
                list_of_candles_for_index_and_resolution = self.main_container[index][resolution]
                candles_json = get_stock_values_finehub(index, resolution, latest_candles_dict[resolution].time,
                                                        datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                if candles_json is not None:
                    candle_objects = change_stock_json_candles_to_candle_objects(candles_json, resolution, index)
                    # It download current candle from the stock. It is removed here to avoid any issues
                    candle_objects.pop(-1)

                    for candle in candle_objects:
                        candle.counter = len(list_of_candles_for_index_and_resolution)
                        list_of_candles_for_index_and_resolution.append(candle)
            save_database(self.market_name, self.main_container)
