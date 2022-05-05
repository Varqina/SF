import time

from database.Database import DatabaseStock, DatabaseCrypto

stock_database = DatabaseStock()
print(len(stock_database.main_container['AAPL']['15']))
print(len(set([candle.time for candle in stock_database.main_container['AAPL']['15']])))
# print(stock_database.main_container['AAPL']['15'][0])
# print(stock_database.main_container['AAPL']['15'][-1])
# print(stock_database.main_container['AAPL']['15'][-2])
# print(stock_database.main_container['AAPL']['15'][-3])
# print(len(stock_database.main_container['AAPL']['15']))
# crypto_database = DatabaseCrypto()


# print(str(end1-start1))

# start = time.time()
# TODO test pattern
# test = TestOnDataBase(database)
# test.check_candle_hammer_pattern()

# own_prediction = OwnPrediction(database)
# own_prediction.test_performance(crypto='BTC', fiat="USDT")
# result = own_prediction.own_up_strength('ADA', '60', "EUR")
# result.get_result()
# end = time.time()
# print(str(end-start))
# trading_view = TradingViewPredictions()
# trading_view.login()
