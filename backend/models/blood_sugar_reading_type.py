from enum import Enum

class BloodSugarReadingType(str, Enum):
    FASTING = "fasting"
    BEFORE_MEAL = "before_meal"
    AFTER_MEAL = "after_meal"
