import requests as requests
import Password.PasswordStrings as password


def get_stock_value():

    parameters = {
        "lat": 40.71,
        "lon": -74
    }
    response = requests.get("https://api.open-notify.org/iss-pass.json", params=parameters)

def get_crypto_value():
    parameters = {
        "symbol": "BINANCE:BTCUSDT",
        "resolution": "D",
        "from": 1627848047,
        "to": 1629316847,
        "token":password.token}
    response = requests.get("https://finnhub.io/api/v1/crypto/candle?", params=parameters)
    print(response.json())
