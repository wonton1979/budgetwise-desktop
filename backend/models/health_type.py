from enum import Enum

class HealthType(str, Enum):
    WEIGHT_RECORD = "weight_record"
    BLOOD_PRESSURE_RECORD = "blood_pressure_record"
    BLOOD_SUGAR_RECORD = "blood_sugar_record"
    PERIOD_RECORD = "period_record"