from candle_prediction.UpCandlePatterns import UpCandlePatterns
from database.Candle import Candle

close_candle = 55322
candle_length = 5473
open_candle = 51515

if close_candle > 55798 - (0.33 * candle_length) and open_candle > 55798 - (0.33 * candle_length):
    print("ok")