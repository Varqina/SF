from candle_prediction.CandlePattern import CandlePattern


class UpCandlePatterns:
    def __init__(self, candles, data=None):
        self.candles = [candles]
        self.data = data
        self.candle_pattern = self.check_patterns()

    def check_patterns(self):
        pass

    # Based on BTC candle_shadow=0.3
    # 15 1089 143 13 %
    # 30 873 136 15 %
    # 60 582 107 18 %
    # D 42 20 47 %
    # W 8 4 50 %
    # M 0 0 0%
    def check_hammer(self, candle_shadow=0.3):
        average_expected_return = 0.05  # todo tutaj trzeba dodac szukanie oporu wczesniejszego i zastrosowac geometrie na 50%
        current_candle = self.candles[-1]
        candle_length = current_candle.height - current_candle.low
        expected_candle_body = current_candle.height - (0.33 * candle_length)
        if current_candle.open_candle >= expected_candle_body and current_candle.close_candle >= expected_candle_body \
                and self.does_fall_before():
            if current_candle.color == "Green":
                if current_candle.height - current_candle.close_candle <= candle_length * candle_shadow:
                    response = CandlePattern(current_candle.open_candle, current_candle.close_candle +
                                             int(current_candle.close_candle * average_expected_return),
                                             current_candle.low,
                                             "Mlot",
                                             current_candle.time)
                    return response
            if current_candle.color == "Red":
                if current_candle.height - current_candle.open_candle <= candle_length * candle_shadow:
                    response = CandlePattern(current_candle.close_candle, current_candle.close_candle +
                                             int(current_candle.close_candle * average_expected_return),
                                             current_candle.low,
                                             "Mlot",
                                             current_candle.time)
                    return response
        return False

    def does_fall_before(self):
        index = self.get_candle_index()
        measure_candle = self.candles[-1]
        stock_before_main_candle = []
        if index:
            if index > 20:
                start_index = index-20
            else:
                start_index = 0
            falling_data = self.data[start_index:index]
            measure_point = 0
            if measure_candle.color == "Red":
                measure_point = measure_candle.close_candle
            else:
                measure_point = measure_candle.open_candle
            for candle in reversed(falling_data):
                if candle.color == "Red":
                    candle_value = candle.close_candle
                else:
                    candle_value = candle.open_candle
                value = (measure_point - candle_value) / measure_point
                if value < -0.02 or value > 0.02:
                    stock_before_main_candle.append(value)
            max_down, max_up = 0, 0
            for direction in stock_before_main_candle:
                if direction < 0 and direction < max_down:
                    max_down = direction
                    continue
                if direction > 0 and direction > max_up:
                    max_up = direction
            if max_down in stock_before_main_candle and max_up in stock_before_main_candle:
                if stock_before_main_candle.index(max_down) < stock_before_main_candle.index(max_up):
                    return True
                else:
                    return False
            if max_down not in stock_before_main_candle:
                return False
            else:
                return True
        return False

    def get_candle_index(self):
        counter = 0
        for candle in self.data:
            if candle.time == self.candles[-1].time:
                return counter
            counter += 1
        return False
