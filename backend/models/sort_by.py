from enum import Enum


class SortBy(str, Enum):
    EXPENSE_DATE = "expense_date"
    AMOUNT = "amount"
