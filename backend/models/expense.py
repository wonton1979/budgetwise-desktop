from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base
from backend.models.category import Category


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[Category] = mapped_column(Enum(Category), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)