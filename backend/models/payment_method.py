from enum import Enum

class PaymentMethod(str, Enum):
    CARD = "card"
    CASH = "cash"
    VOUCHER = "voucher"
    DIRECT_DEBIT = "direct debit"
    BANK_TRANSFER = "bank transfer"