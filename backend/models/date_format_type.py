from enum import Enum

class DateFormatType(str,Enum):
    UK = "DD/MM/YYYY"
    ISO = "YYYY-MM-DD"
    LONG = "DD MMM YYYY"