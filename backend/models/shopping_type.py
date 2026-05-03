from enum import Enum


class ShoppingType(str, Enum):
    IN_STORE = "in-store"
    ONLINE   = "online"