from decimal import Decimal

from sqlalchemy import Numeric, Enum, String,ForeignKey

from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship

from backend.models.frequency import Frequency
from backend.models.income_category import IncomeCategory


class Income(Base):

    __tablename__ = "income"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[IncomeCategory] = mapped_column(Enum(IncomeCategory), nullable=False)
    frequency: Mapped[Frequency] = mapped_column(Enum(Frequency), nullable=False)
    notes: Mapped[str|None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="incomes")