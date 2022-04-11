from candle_prediction.UpCandlePatterns import UpCandlePatterns
from database.Candle import CandleCrypto

candles = CandleCrypto(33551, 33553, 34067, 30855, 1, 1, "D", "BTC", "USDT")
temp_object = UpCandlePatterns(candles)
result = temp_object.check_hammer()
print(result.open_position)

