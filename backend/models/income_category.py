from enum import Enum

class IncomeCategory(str, Enum):
    SALARY = "salary"
    BONUS = "bonus"
    FREELANCE = "freelance"
    BENEFITS = "benefits"
    RENT_INCOME = "rental income"
    INVESTMENT = "investment"
    PENSION = "pension"
    OTHER = "other"
