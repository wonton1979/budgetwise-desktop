import requests

def get_exchange_rate(currency_code):
    response = requests.get("https://api.frankfurter.dev/v1/latest?base=GBP")
    return response.json()["rates"][currency_code]

