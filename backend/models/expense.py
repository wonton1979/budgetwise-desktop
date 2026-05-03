from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, Numeric, String,Boolean
from sqlalchemy.orm import Mapped, mapped_column,relationship

from backend.database import Base
from backend.models.category import Category
from sqlalchemy import ForeignKey

from backend.models.payment_method import PaymentMethod
from backend.models.shopping_type import ShoppingType


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[Category] = mapped_column(Enum(Category), nullable=False)
    shop_name: Mapped[str] = mapped_column(String(50), nullable=False)
    shopping_type: Mapped[ShoppingType] = mapped_column(Enum(ShoppingType), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=True)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_public_to_family: Mapped[bool] = mapped_column(Boolean, nullable=False,default=False)
    user = relationship("User", back_populates="expenses")