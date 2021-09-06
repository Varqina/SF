import data_requests.CryptoRequests as data_request
from data_requests.TimeManager import convert_unix_to_data
from data_requests.TradingViewPredictions import TradingViewPredictions
from database.Database import Database


database = Database()
database.read_crypto_from_file()
#database.add_to_data_base('ADA', 'EUR')
#print(convert_unix_to_data(database.main_container['ADA']['1']['EUR'][-1].time))
#print(convert_unix_to_data(database.main_container['ADA']['5']['EUR'][-1].time))
#print(convert_unix_to_data(database.main_container['ADA']['15']['EUR'][-1].time))
#print(convert_unix_to_data(database.main_container['ADA']['30']['EUR'][-1].time))
#database.update_candles_on_currency('ADA')
#print(database.main_container['ADA']['1']['EUR'][-1].time)


#trading_view = TradingViewPredictions()
#trading_view.login()
