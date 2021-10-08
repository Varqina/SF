from candle_prediction.CandlePattern import CandlePattern


class UpCandlePatterns:
    def __init__(self, candles):
        self.candles = candles
        self.candle_pattern = self.check_patterns()

    def check_patterns(self):
        pass

    def check_hammer(self, candle_shadow=0.4):
        #[15, 30, 60, D, W, M]
        current_candle = self.candles[-1]
        candle_length = current_candle.height - current_candle.low
        expected_range = current_candle.height - (0.33 * candle_length)
        if current_candle.open_candle >= expected_range and current_candle.close_candle >= expected_range:
            if current_candle.color == "Green":
                if current_candle.height - current_candle.close_candle <= candle_length * candle_shadow:
                    response = CandlePattern(current_candle.close_candle, current_candle.low, "Mlot")
                    return response
            if current_candle.color == "Red":
                if current_candle.height - current_candle.open_candle <= candle_length * candle_shadow:
                    response = CandlePattern(current_candle.open_candle, current_candle.low, "Mlot")
                    return response
