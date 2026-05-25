from enum import Enum

class Frequency(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    QUARTERLY = "quarterly"