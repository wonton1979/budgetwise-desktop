from decimal import Decimal

from backend.database import SessionLocal
from backend.models.currency_type import CurrencyType
from backend.models.user import User
from backend.utils.currency_converter import get_exchange_rate


def get_current_user_exchange_rate(user_id):

    db=SessionLocal()

    try:
        exchange_rate = Decimal(1)

        db_user_preferred_currency = db.query(User.preferred_currency_display).filter(User.id == user_id).scalar()

        if db_user_preferred_currency == CurrencyType.USD:
            exchange_rate = Decimal(get_exchange_rate("USD"))
        if db_user_preferred_currency == CurrencyType.EUR:
            exchange_rate = Decimal(get_exchange_rate("EUR"))

        return exchange_rate

    finally:
        db.close()
