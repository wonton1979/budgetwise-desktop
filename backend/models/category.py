from enum import Enum


class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"
    