from candle_prediction.UpCandlePatterns import UpCandlePatterns


class PatternResult:
    def __init__(self, correct, exist, resolution, data_length):
        self.correct = correct
        self.exist = exist
        self.data_length = data_length
        self.resolution = resolution
        self.correct_percent = self.count_percent()

    def count_percent(self):
        if self.correct != 0 and self.exist != 0:
            return self.correct / self.exist
        else:
            return 0

class TestOnDataBase:
    def __init__(self, database):
        self.database = database

    def check_and_adjust_candles_pattern_hammer(self, currency_symbol='BTC', resolution='D', fiat="USDT"):
        result_data = []
        for key_resolution in self.database.main_container[currency_symbol]:
            print(key_resolution)
            data = self.database.main_container[currency_symbol][key_resolution][fiat]
            for candle_shadow in range(1, 41):
                exists = 0
                correct = 0
                counter = 0
                for candle in data:
                    temp = UpCandlePatterns([candle])
                    value = temp.check_hammer(candle_shadow / 100)
                    if value is not None:
                        exists += 1
                        for next_candle in data[counter + 1:]:
                            if value.open_position + value.open_position * 0.08 <= next_candle.height:
                                correct += 1
                                break
                            if value.stop_loss >= next_candle.low:
                                break
                    counter += 1
                result_to_be_added = PatternResult(correct, exists, key_resolution, len(data))
                result_to_be_added.shadow = candle_shadow
                result_data.append(result_to_be_added)
        sort_result_data(result_data)
        return result_data


def sort_result_data(data):
    result_data = []
    while len(data) > 0:
        max = 0
        for element in data:
            if element.correct_percent >= max:
                max = element.correct_percent
        counter = 0
        for element in data:
            if element.correct_percent == max:
                result_data.append(element)
                data.pop(counter)
            counter += 1
    for element in result_data:
        if element.correct != 0 and element.exist != 0:
            print(f'{int((element.correct_percent)*100)}%({element.correct} / {element.exist})/{element.resolution}/{element.shadow}')
        else:
            print(f'{int(element.correct_percent*100)}/{element.resolution}/{element.shadow}')



