from abc import ABC


class Candle(ABC):
    def __init__(self, open_candle, close_candle, height, low, volume, time, resolution, symbol):
        self.close_candle = close_candle
        self.open_candle = open_candle
        self.height = height
        self.low = low
        self.volume = volume
        self.time = time
        self.resolution = resolution
        self.symbol = symbol
        self.color = self.get_color()
        self.counter = 0

    def get_color(self):
        return "Green" if self.open_candle - self.close_candle < 0 else "Red"


class CandleCrypto(Candle):
    def __init__(self, open_candle, close_candle, height, low, volume, time, resolution, symbol, fiat):
        super(CandleCrypto, self).__init__(close_candle, open_candle, height, low, volume, time, resolution, symbol)
        self.fiat = fiat


class CandleStock(Candle):
    def __init__(self, open_candle, close_candle, height, low, volume, time, resolution, symbol):
        super(CandleStock, self).__init__(close_candle, open_candle, height, low, volume, time, resolution, symbol)
