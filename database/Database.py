from datetime import datetime

from data_requests.CryptoRequests import get_crypto_value


class Database:
    def __init__(self):
        self.main_container = {}

    def add_to_data_base(self, crypto_currency_symbol, fiat_symbol):
        self.main_container[crypto_currency_symbol] = {"1": {}, "5": {}, "15": {}, "30": {}, "60": {}, "D": {}, "W": {},
                                                       "M": {}}
        for resolution in self.main_container[crypto_currency_symbol]:
            self.main_container[crypto_currency_symbol][resolution] = {fiat_symbol: []}

    def update_candles_on_currency(self, crypto_currency_symbol):
        latest_date_dict = self.get_latest_dates(crypto_currency_symbol)
        data_to_be_updated = {}
        if len(latest_date_dict) == 0:
            return
        for resolution in latest_date_dict:
            for fiat in latest_date_dict[resolution]:
                candles_json = get_crypto_value(crypto_currency_symbol, resolution, latest_date_dict[resolution][fiat],
                                                datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                data_to_be_updated[resolution][fiat] = candles_json

                #data_to_be_updated -> zamienic na candle i dodac do main_container
        pass

    def get_latest_dates(self, crypto_currency_symbol):
        symbol_data = self.main_container[crypto_currency_symbol]
        latest_date_dict = {}
        if len(symbol_data):
            for resolution in symbol_data:
                if len(symbol_data[resolution]) > 0:
                    for fiat, candle in symbol_data[resolution].items():
                        latest_date_dict[resolution] = {fiat: candle.time}
                    return latest_date_dict
        return
