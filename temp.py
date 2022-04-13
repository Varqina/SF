from data_requests.ApiRequests import StockApiManager, CryptoApiManager, change_json_candles_for_candle_objects

test = StockApiManager()

response = test.get_values_for_symbol("AAPL", "M", 1586688633, 1649767840)
print(response.status_code)
print(response.json())
response_candles = change_json_candles_for_candle_objects(response, "M", "AAPL")
response_candles[0].print_candle()



