class Candle:
    def __init__(self, open_candle, close_candle, height, low, volume, time, resolution, symbol, fiat):
        self.close_candle = close_candle
        self.open_candle = open_candle
        self.height = height
        self.low = low
        self.volume = volume
        self.time = time
        self.resolution = resolution
        self.symbol = symbol
        self.fiat = fiat
        self.color = self.get_color()
        self.counter = 0

    def get_color(self):
        return "Green" if self.open_candle - self.close_candle < 0 else "Red"
