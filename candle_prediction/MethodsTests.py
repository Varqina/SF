import unittest

from database.Candle import Candle


# candle_x = Candle(open_candle, close_candle, height, low, volume, time)

# TODO zrobic unittesty
class TestOwnUpStrength(unittest.TestCase):
    def test_check_candles_for_up_strength_success(self):
        #candle_1 = Candle(30842, 29872, 31098, 29087, 19547, 1, "D")
        #candle_2 = Candle(29872, 32121, 32852, 29453, 20534, 1, "D")
        #candle_3 = Candle(32158, 32341, 50000, 31683, 18816, 1, "D")
        testing_data = [candle_1, candle_2, candle_3]
        candle_result = check_candles_for_up_strength(testing_data, 8)
        self.assertEqual(candle_result.correct, 1)
        self.assertEqual(candle_result.exists, 1)

    def test_check_candles_for_up_strength_fail(self):
        #candle_1 = Candle(30842, 29872, 31098, 29087, 19547, 1, "D")
        #candle_2 = Candle(29872, 32121, 32852, 29453, 20534, 1, "D")
        #candle_3 = Candle(32158, 32341, 20000, 31683, 18816, 1, "D")
        testing_data = [candle_1, candle_2, candle_3]
        candle_result = check_candles_for_up_strength(testing_data, 8)
        self.assertEqual(candle_result.correct, 1)
        self.assertEqual(candle_result.exists, 1)
