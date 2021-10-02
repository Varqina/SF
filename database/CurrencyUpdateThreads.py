import threading

class CurrencyUpdateThreads(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        self.target = target
        self.args = args
        super().__init__(target=self.target, args=self.args)

    def run(self):
        super().run()
