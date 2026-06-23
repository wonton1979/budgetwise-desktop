from enum import Enum


class MemorableDayType(str, Enum):
    BIRTHDAY = 'birthday'
    ANNIVERSARY = 'anniversary'
    OTHER = 'other'