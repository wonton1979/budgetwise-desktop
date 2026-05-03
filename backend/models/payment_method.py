from enum import Enum

class PaymentMethod(str, Enum):
    CARD = "card"
    CASH = "cash"
    VOUCHER = "voucher"