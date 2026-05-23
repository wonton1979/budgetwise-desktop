from enum import Enum

class RecurringExpenseCategory(str, Enum):
    HOUSING= "housing"
    UTILITIES = "utilities"
    INSURANCE = "insurance"
    SUBSCRIPTION = "subscription"
    HEALTHCARE = "healthcare"
    TRANSPORT = "transport"
    OTHER = "other"
