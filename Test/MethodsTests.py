import unittest

from candle_prediction.UpCandlePatterns import UpCandlePatterns
from database.Candle import CandleCrypto


# candle_x = Candle(open_candle, close_candle, height, low, volume, time)

# TODO zrobic unittesty

class TestUpCandlePatterns(unittest.TestCase):
    def test_check_hammer_red(self):
        candles = CandleCrypto(33551, 33553, 34067, 30855, 1, 1, "D", "BTC", "USDT")
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertEqual(result.name, "Mlot")
        self.assertEqual(result.open_position, 33551)
        self.assertEqual(result.stop_loss, 30855)

    def test_check_hammer_green(self):
        candles = CandleCrypto(35613, 35455, 36129, 33353, 1, 1, "D", "BTC", "USDT")
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertEqual(result.name, "Mlot")
        self.assertEqual(result.open_position, 35455)
        self.assertEqual(result.stop_loss, 33353)


    def test_check_hammer_big_not_accepted_shadow(self):
        candles = CandleCrypto(37239, 35336, 40531, 34979, 1, 1, "D", "BTC", "USDT")
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertFalse(result)

    def test_does_fall_before_fail(self):
        candle4 = CandleCrypto(5957, 6170, 6180, 5268, 1, 5, "D", "BTC", "USDT")
        candle3 = CandleCrypto(5703, 5957, 6187, 5030, 1, 4, "D", "BTC", "USDT")
        candle2 = CandleCrypto(4636, 5711, 5940, 4513, 1, 3, "D", "BTC", "USDT")
        candle1 = CandleCrypto(4398, 4644, 4650, 4078, 1, 2, "D", "BTC", "USDT")
        candles = []
        for i in range(30):
            candles.append(CandleCrypto(1, 1, 1, 1, 1, 0, "D", "BTC", "USDT"))
        candles.append(candle1)
        candles.append(candle2)
        candles.append(candle3)
        candles.append(candle4)
        temp_object = UpCandlePatterns(candle4, candles)
        self.assertFalse(temp_object.does_fall_before())




