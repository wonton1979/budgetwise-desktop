from enum import Enum

class RecurringSubcategory(str, Enum):
    # Housing
    MORTGAGE = "mortgage"
    RENT = "rent"
    COUNCIL_TAX = "council tax"
    HOME_INSURANCE = "home insurance"

    # Utilities
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    BROADBAND = "broadband"
    MOBILE_BILL = "mobile bill"
    TV_LICENCE = "tv licence"

    # Insurance
    CAR_INSURANCE = "car insurance"
    LIFE_INSURANCE = "life insurance"
    PET_INSURANCE = "pet insurance"
    HOME_EMERGENCY = "home emergency"
    BREAKDOWN_COVER = "breakdown cover"
    PHONE_INSURANCE = "phone insurance"

    # Subscription
    STREAMING = "streaming"
    TV_PACKAGE = "tv package"
    GAMING_SUBSCRIPTION = "gaming subscription"
    SOFTWARE_SUBSCRIPTION = "software subscription"

    # Healthcare
    MEDICAL = "medical"
    DENTAL = "dental"
    PRESCRIPTION = "prescription"

    # Transport
    PARKING = "parking"
    FUEL = "fuel"
    TRANSPORT_PASS = "transport pass"
    CAR_FINANCE = "car finance"

    # Other
    OTHER = "other"