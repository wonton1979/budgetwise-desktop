from enum import Enum


class Category(str, Enum):
    GROCERY = "grocery"
    TRANSPORT = "transport"
    DEPARTMENT_STORE= "department store"
    ENTERTAINMENT = "entertainment"
    FAST_FOOD = "fast food"
    RESTAURANT = "restaurant"
    OTHER = "other"
    