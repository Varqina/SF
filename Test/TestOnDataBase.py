from candle_prediction.UpCandlePatterns import UpCandlePatterns
from data_requests.TimeManager import convert_unix_to_data


class ResultPattern:
    def __init__(self, correct, exist, resolution, data_length=0, time=0):
        self.correct = correct
        self.exist = exist
        self.data_length = data_length
        self.resolution = resolution
        self.time = time
        self.correct_percent = self.count_percent()

    def count_percent(self):
        if self.correct != 0 and self.exist != 0:
            return self.correct / self.exist
        else:
            return 0

class TestOnDataBase:
    def __init__(self, database):
        self.database = database

    def adjust_candles_pattern_hammer(self, currency_symbol='BTC', resolution='D', fiat="USDT"):
        result_data = []
        exists = 0
        for key_resolution in self.database.main_container[currency_symbol]:
            data = self.database.main_container[currency_symbol][key_resolution][fiat]
            for candle_shadow in range(1, 41): # shadow_length
                correct = 0
                counter = 0
                open_position = 0
                time = 0
                for candle in data:
                    candle_match_pattern = UpCandlePatterns(candle, data).check_hammer(candle_shadow / 100)
                    if candle_match_pattern:
                        open_position = candle_match_pattern.open_position
                        exists += 1
                        time = candle_match_pattern.time
                        max_candle_before_fall = 0
                        for next_candle in data[counter + 1:]:
                            if next_candle.height > max_candle_before_fall:
                                max_candle_before_fall = next_candle.height
                            if candle_match_pattern.stop_loss >= next_candle.low:
                                break
                        result_to_be_added = ResultPattern(correct, exists, key_resolution, len(data))
                        result_to_be_added.shadow = candle_shadow
                        result_to_be_added.rise = how_high(open_position, max_candle_before_fall)
                        result_to_be_added.time = time
                        result_data.append(result_to_be_added)
                    counter += 1
        print_average(result_data)
        return result_data

    def check_candle_hammer_pattern(self, currency_symbol='BTC', resolution='D', fiat="USDT"):
        result_data = []
        debug = False
        for key_resolution in self.database.main_container[currency_symbol]:
            data = self.database.main_container[currency_symbol][key_resolution][fiat]
            exists = 0
            counter = 0
            correct_global = 0
            correct_current = 0
            temp = 0
            for candle in data:
                candle_match_pattern = UpCandlePatterns(candle, data).check_hammer()
                if candle_match_pattern:
                    exists += 1
                    time = candle_match_pattern.time
                    max_candle_before_fall = 0
                    for next_candle in data[counter + 1:]:
                        correct_current = 0
                        temp = next_candle.time
                        if next_candle.height > max_candle_before_fall:
                            max_candle_before_fall = next_candle.height
                        if candle_match_pattern.close_position <= max_candle_before_fall:
                            correct_global += 1
                            correct_current = 1
                            break
                        if next_candle.low < candle_match_pattern.stop_loss:
                            break
                    result_to_be_added = ResultPattern(correct_current, exists, key_resolution, len(data), time)
                    result_data.append(result_to_be_added)
                    if debug:
                        if key_resolution == "W":
                            print(f"{convert_unix_to_data(time)} {correct_current} "
                                  f"{candle_match_pattern.close_position} {max_candle_before_fall} "
                                  f"{candle_match_pattern.stop_loss} {convert_unix_to_data(temp)}")
                counter += 1
            if correct_global != 0 and exists != 0:
                print(f"{key_resolution} {exists} {correct_global} {int((correct_global/exists)*100)}% ")


def how_high(open, high):
    if high != 0 and open != 0:
        return int(100 * (high - open)/open)
    #todo poprawic zaokraglanie
    return 0


def print_average(data):
    for resolution in ("15", "30", "60", "D", "W", "M"):
        counter = 0
        avg_percent_return = 0
        shadow = 0
        for candle_shadow in range(0, 41):
            shadow = candle_shadow
            for element in data:
                if element.shadow == candle_shadow and element.resolution == resolution:
                    if element.rise > 0:
                        counter += 1
                        avg_percent_return += element.rise
            if avg_percent_return != 0 and counter != 0:
                print(f"{resolution} {shadow} {avg_percent_return/counter} {counter}")


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



