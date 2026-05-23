from datetime import date
from decimal import Decimal

from sqlalchemy import Numeric, Enum, String, Date, ForeignKey, Boolean

from backend.database import Base
from sqlalchemy.orm import Mapped, mapped_column,relationship

from backend.models.payment_frequency import PaymentFrequency
from backend.models.payment_method import PaymentMethod
from backend.models.recurring_expense_category import RecurringExpenseCategory
from backend.models.recurring_expense_subcategory import RecurringSubcategory


class RecurringExpense(Base):

    __tablename__ = "recurring_expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[RecurringExpenseCategory] = mapped_column(Enum(RecurringExpenseCategory), nullable=False)
    subcategory: Mapped[RecurringSubcategory] = mapped_column(Enum(RecurringSubcategory), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(50), nullable=False)
    frequency: Mapped[PaymentFrequency] = mapped_column(Enum(PaymentFrequency), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date|None] = mapped_column(Date, nullable=True)
    is_public_to_family: Mapped[bool] = mapped_column(Boolean, nullable=True)
    notes: Mapped[str|None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="recurring_expenses")