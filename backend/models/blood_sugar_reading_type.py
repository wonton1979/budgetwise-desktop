from enum import Enum

class BloodSugarReadingType(str, Enum):
    FASTING = "fasting"
    AFTER_MEAL_2 = "after_meal_2"
