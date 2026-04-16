from enum import Enum


class Order(str, Enum):
    DESC = "desc"
    ASC = "asc"
