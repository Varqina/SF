import csv
import pickle
import time
from calendar import monthrange

from data_requests.TimeManager import convert_unix_to_data


def find_candle_by_time(candle_to_find, data):
    for candle in data:
        if candle.time == candle_to_find.time:
            return candle.counter


class Results:
    def __init__(self, correct, exists, data_length, resolution, expected_return):
        self.correct = int(correct)
        self.exists = int(exists)
        self.data_length = data_length
        self.resolution = resolution
        self.expected_return = expected_return

    def get_result(self):
        result = int(100*(self.correct/self.exists))
        return (f"sprawdzalność {result}% przy rozdzielcznosci {self.resolution} wystąpiło {self.exists}")


class OwnPrediction:
    def __init__(self, database):
        # {{crypto_currency_symbol: {resolution: {fiat: []}}}}
        self.database = database

    def test_performance(self, crypto="ADA", fiat="EUR"):
        results = []
        for i in range(1, 20):
            for resolution in self.database.main_container[crypto]:
                result = self.own_up_strength(currency_symbol=crypto, resolution=resolution, fiat=fiat,
                                              expected_return=i)
                results.append(result)
        with open(f'candle_prediction/results/{crypto}{fiat}.csv', mode='a') as file:
            file = csv.writer(file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file.writerow(["Interwal","Zwrot", "Szansa", 'ilosc wystapien/max'])
            for result in results:
                file.writerow([result.resolution, f'{result.expected_return}%',
                               f'{int(100*(result.correct/result.exists))}%',
                               f'{result.exists}/{len(self.database.main_container[crypto][result.resolution][fiat])}'])
        data_time = convert_unix_to_data(int(time.time())).replace('/','')
        data_time = data_time.replace(':','')
        with open(f'candle_prediction/results/{crypto}{fiat}{data_time}.data', 'wb')\
                as database:
            pickle.dump(results, database)

    def own_up_strength(self, currency_symbol='ADA', resolution='60', fiat='EUR', expected_return=8):
        """ currency_symbol = ADA, resolution = 60, fiat = EUR"""
        data_candles = self.database.main_container[currency_symbol][resolution][fiat]
        result = self.check_candles_for_up_strength(data_candles, expected_return)
        return result

    def check_candles_for_up_strength(self, data_candles, expected_return):
        counter = 1
        correct = 0
        exists = 0
        for candle_to_check in data_candles[1:]:
            if counter < len(data_candles):
                previous_candle = data_candles[counter - 1]
                if previous_candle.color == "Red":
                    if candle_to_check.close_candle >= previous_candle.open_candle:
                        if candle_to_check.volume * 0.98 >= previous_candle.volume:
                            if candle_to_check.height < candle_to_check.close_candle + candle_to_check.close_candle* 0.2:
                            # TODO porobic na cienie
                            # TODO sprawdzic czy jest/byl spadek
                            # TODO jak blisko dna jest
                            # TODO czy jest w tescie
                                exists += 1
                            if self.check_if_prediction_is_correct(data_candles, expected_return, counter):
                                correct += 1

            counter += 1
        result = Results(correct, exists, len(data_candles), data_candles[1].resolution, expected_return)
        return result

    def check_if_prediction_is_correct(self, data_candles, percent_return, counter):
        candle_to_check = data_candles[counter]
        expected_return = candle_to_check.close_candle + candle_to_check.close_candle * percent_return * 0.01
        lowest_acceptance = candle_to_check.low
        should_return_false = False
        should_return_true = False
        for candle in data_candles[counter + 1:]:
            if candle.low < lowest_acceptance:
                should_return_false = True
            if candle.height >= expected_return:
                should_return_true = True
            if should_return_false and should_return_true:
                return self.check_which_was_first(candle, lowest_acceptance, expected_return)
            elif should_return_false:
                return False
            elif should_return_true:
                return True

    def check_which_was_first(self, candle, bottom_value, top_value):
        resolutions = ["15", "30", "60", "D", "W", "M"]
        index_number = resolutions.index(candle.resolution)
        resolution = resolutions[index_number - 1] if index_number > 0 else None
        resolution_value = 0
        if resolution is None: return False
        if resolution == "30": resolution_value = 2
        if resolution == "60": resolution_value = 2
        if resolution == "D": resolution_value = 24
        if resolution == "W": resolution_value = 7
        if resolution == "MM":
            time = convert_unix_to_data(int(candle.time))
            num_days = int(monthrange(int(time[:4]), int(time[5:7]))[1])
            resolution_value = num_days
        smaller_resolution_candles = self.database.main_container[candle.symbol][resolution][candle.fiat]
        smaller_candle_counter = find_candle_by_time(candle, smaller_resolution_candles)
        should_return_false = False
        should_return_true = False
        for candle in smaller_resolution_candles[smaller_candle_counter: smaller_candle_counter + resolution_value]:
            if candle.low < bottom_value:
                should_return_false = True
            if candle.height >= top_value:
                should_return_true = True
            if should_return_false and should_return_true:
                return self.check_which_was_first(candle, bottom_value, top_value)
            elif should_return_false:
                return False
            elif should_return_true:
                return True
