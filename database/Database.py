from datetime import datetime
from abc import ABC, abstractmethod
from data.DataManager import load_file, read_data_from_file, save_data
from data_requests.ApiRequests import change_json_candles_for_candle_objects, CryptoApiManager, StockApiManager
from data_requests.TimeManager import convert_data_to_unix, is_comparable_with_current_time

log = False


def count_end_time_with_api_limits(resolution, from_time):
    limit = 0
    resolution_unix_time_representation = 0
    time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if resolution == "15":
        limit = 1404
        resolution_unix_time_representation = 900
    elif resolution == "30":
        limit = 704
        resolution_unix_time_representation = 1800
    elif resolution == "60":
        limit = 352
        resolution_unix_time_representation = 3600
    end_time = from_time + (limit * resolution_unix_time_representation)

    if limit == 0:
        end_time = time_now

    return convert_data_to_unix(end_time)


def count_from_time_for_first_time():
    from_time = int(datetime.now().timestamp()) - 31556926
    print(from_time)
    return from_time


class Database(ABC):
    def __init__(self, market_name):
        #   {{stock_symbol:{resolution:[]}}}
        self.market_name = market_name
        self.main_container = {}
        self.main_container = load_file(self.market_name)
        stock_indexes = read_data_from_file(self.market_name)
        if len(self.main_container) < len(stock_indexes):
            self.add_to_data_base(stock_indexes)
        self.update_database()

    def add_to_data_base(self, stock_indexes):
        for index in stock_indexes:
            if index not in self.main_container:
                self.main_container[index] = {"15": [], "30": [], "60": [], "D": [], "W": [], "M": []}
                self.download_candles_for_first_time(index)
        save_data(self.market_name, self.main_container)

    def download_candles_for_first_time(self, index):
        for resolution in self.main_container[index]:
            response_candles_json = self.make_api_request(index, resolution, count_from_time_for_first_time())
            if response_candles_json is not None:
                candle_objects = change_json_candles_for_candle_objects(response_candles_json, resolution, index)
                for candle in candle_objects:
                    candle.counter = len(self.main_container[index][resolution])
                    self.main_container[index][resolution].append(candle)

    def update_database(self):
        for index in self.main_container:
            if log:
                print(index)
            self.update_candles_on_market_index(index)

    def get_latest_dates(self, index):
        index_data = self.main_container[index]
        latest_date_dict = {}
        if len(index_data) > 0:
            for resolution in index_data:
                if len(index_data[resolution]) > 0:
                    latest_date_dict[resolution] = index_data[resolution][-1]
        return latest_date_dict

    def update_candles_on_market_index(self, index):
        print("robie update")
        latest_candles_dict = self.get_latest_dates(index)
        if log:
            print(latest_candles_dict)
        if latest_candles_dict is not None and len(latest_candles_dict) > 0:
            loop = True
            for resolution in latest_candles_dict:
                while loop:
                    list_of_candles_for_index_and_resolution = self.main_container[index][resolution]
                    print(resolution)
                    print(len(self.main_container[index][resolution]))
                    candles_json = self.make_api_request(index, resolution, latest_candles_dict[resolution].time)
                    if candles_json is not None:
                        candle_objects = change_json_candles_for_candle_objects(candles_json, resolution, index)
                        # It download current candle from the stock. It is removed here to avoid any issues
                        candle_objects.pop(-1)
                        for candle in candle_objects:
                            candle.counter = len(list_of_candles_for_index_and_resolution)
                            list_of_candles_for_index_and_resolution.append(candle)
                        if is_comparable_with_current_time(self.main_container[index][resolution][-1].time, resolution):
                            loop = False
                        else:
                            latest_candles_dict = self.get_latest_dates(index)
                        save_data(self.market_name, self.main_container)

    @abstractmethod
    def make_api_request(self, index, resolution, from_time):
        pass


class DatabaseStock(Database):
    def __init__(self):
        self.api_manager = StockApiManager()
        super().__init__("stock")

    def make_api_request(self, index, resolution, from_time):
        return self.api_manager.get_values_for_symbol(index, resolution, from_time,
                                                      count_end_time_with_api_limits(resolution, from_time))


class DatabaseCrypto(Database):
    def __init__(self):
        super().__init__("crypto")
        self.api_manager = CryptoApiManager()

    def make_api_request(self, crypto_currency_symbol, resolution, from_time):
        return self.api_manager.get_values_for_symbol(crypto_currency_symbol, resolution,
                                                      from_time,
                                                      count_end_time_with_api_limits(resolution, from_time))
