import time

from Test.TestOnDataBase import TestOnDataBase
from candle_prediction.OwnPrediction import OwnPrediction
from data_requests.TimeManager import convert_unix_to_data
from data_requests.TradingViewPredictions import TradingViewPredictions
from database.DatabaseCrypto import Database


"""Environments set"""
database_update = False
"""End of environment set"""
start1 = time.time()
database = Database(database_update)
end1 = time.time()
#print(str(end1-start1))

#start = time.time()
# TODO test pattern
#test = TestOnDataBase(database)
#test.check_candle_hammer_pattern()

#own_prediction = OwnPrediction(database)
#own_prediction.test_performance(crypto='BTC', fiat="USDT")
#result = own_prediction.own_up_strength('ADA', '60', "EUR")
#result.get_result()
#end = time.time()
#print(str(end-start))
#trading_view = TradingViewPredictions()
#trading_view.login()
