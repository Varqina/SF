import data_requests.CryptoRequests as data_request


test = data_request.get_crypto_value(data_request.get_crypto_symbol("adaeur"), "D", "12/08/2021", "18/08/2021")
print(test)
