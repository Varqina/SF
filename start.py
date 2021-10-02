import time

import data_requests.CryptoRequests as data_request
from data_requests.TimeManager import convert_unix_to_data
from data_requests.TradingViewPredictions import TradingViewPredictions
from database.Database import Database


database = Database()
#time.sleep(5)
print(convert_unix_to_data(int(time.time())))
print(convert_unix_to_data(database.main_container['ADA']['60']['EUR'][-1].time))
print(convert_unix_to_data(database.main_container['ADA']['60']['EUR'][-1].close_candle))
print(convert_unix_to_data(database.main_container['BTC']['M']['USDT'][-1].time))
print(convert_unix_to_data(database.main_container['ADA']['60']['USDT'][-1].time))
print(convert_unix_to_data(database.main_container['ADA']['60']['USDT'][-1].close_candle))
#database.update_candles_on_currency('ADA')
#print(database.main_container['ADA']['1']['EUR'][-1].time)


#trading_view = TradingViewPredictions()
#trading_view.login()
