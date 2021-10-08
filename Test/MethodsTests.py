import unittest

from candle_prediction.UpCandlePatterns import UpCandlePatterns
from database.Candle import Candle


# candle_x = Candle(open_candle, close_candle, height, low, volume, time)

# TODO zrobic unittesty
class TestOwnUpStrength(unittest.TestCase):
    pass
    # def test_check_candles_for_up_strength_success(self):
    #     #candle_1 = Candle(30842, 29872, 31098, 29087, 19547, 1, "D")
    #     #candle_2 = Candle(29872, 32121, 32852, 29453, 20534, 1, "D")
    #     #candle_3 = Candle(32158, 32341, 50000, 31683, 18816, 1, "D")
    #     testing_data = [candle_1, candle_2, candle_3]
    #     candle_result = check_candles_for_up_strength(testing_data, 8)
    #     self.assertEqual(candle_result.correct, 1)
    #     self.assertEqual(candle_result.exists, 1)
    #
    # def test_check_candles_for_up_strength_fail(self):
    #     #candle_1 = Candle(30842, 29872, 31098, 29087, 19547, 1, "D")
    #     #candle_2 = Candle(29872, 32121, 32852, 29453, 20534, 1, "D")
    #     #candle_3 = Candle(32158, 32341, 20000, 31683, 18816, 1, "D")
    #     testing_data = [candle_1, candle_2, candle_3]
    #     candle_result = check_candles_for_up_strength(testing_data, 8)
    #     self.assertEqual(candle_result.correct, 1)
    #     self.assertEqual(candle_result.exists, 1)


class TestUpCandlePatterns(unittest.TestCase):
    def test_check_hammer_red(self):
        candles = [Candle(33551, 33553, 34067, 30855, 1, 1, "D", "BTC", "USDT")]
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertEqual(result.name, "Mlot")
        self.assertEqual(result.open_position, 33551)
        self.assertEqual(result.stop_loss, 30855)

    def test_check_hammer_green(self):
        candles = [Candle(35613, 35455, 36129, 33353, 1, 1, "D", "BTC", "USDT")]
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertEqual(result.name, "Mlot")
        self.assertEqual(result.open_position, 35455)
        self.assertEqual(result.stop_loss, 33353)


    def test_check_hammer_big_not_accepted_shadow(self):
        candles = [Candle(37239, 35336, 40531, 34979, 1, 1, "D", "BTC", "USDT")]
        temp_object = UpCandlePatterns(candles)
        result = temp_object.check_hammer()
        self.assertIsNone(result)
