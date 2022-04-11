from datetime import datetime
from abc import ABC, abstractmethod
from data.DataManager import load_database, read_data_from_file, save_database
from data_requests.StockRequests import get_stock_values_finehub, change_stock_json_candles_to_candle_objects

log = False


class Database(ABC):
    @abstractmethod
    def add_to_data_base(self, stock_index):
        pass

    @abstractmethod
    def update_database(self):
        pass

    @abstractmethod
    def get_latest_dates(self, index):
        pass

    @abstractmethod
    def update_candles_on_index(self, index):
        pass

    def __int__(self, market_name):
        #   {{stock_symbol:{resolution:[]}}}
        self.market_name = market_name
        self.main_container = {load_database(self.market_name)}
        stock_indexes = read_data_from_file(self.market_name)
        if len(self.main_container) < len(stock_indexes):
            self.add_to_data_base(stock_indexes)
        self.update_database()
