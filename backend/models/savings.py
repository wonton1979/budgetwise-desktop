from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Numeric, Date, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from sqlalchemy import ForeignKey

class Savings(Base):

    __tablename__ = "savings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    purpose_name: Mapped[str] = mapped_column(String(50), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2),default=0, nullable=False)
    goal_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    target_date: Mapped[date] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="savings")