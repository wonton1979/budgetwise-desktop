from enum import Enum


class CurrencyType(str, Enum):
    GBP = "GBP"
    USD = "USD"
    EUR = "EUR"
    CNY = "CNY"
    JPY = "JPY"
    MYR = "MYR"