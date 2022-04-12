import unittest

from data_requests.ApiRequests import CryptoApiManager, StockApiManager


class TestApiHealthChecks(unittest.TestCase):
    def test_crypto_api(self):
        test = CryptoApiManager()
        response = test.get_values_for_symbol("BINANCE:BTCUSDT", "M", 1586688633, 1649767840).status_code
        self.assertEqual(response, 200)

    def test_stock_api(self):
        test = StockApiManager()
        response = test.get_values_for_symbol("AAPL", "M", 1586688633, 1649767840).status_code
        self.assertEqual(response, 200)






if __name__ == '__main__':
    unittest.main()
