from sqlalchemy import Date, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from backend.database import Base
from backend.models.memorable_day_type import MemorableDayType


class MemorableDay(Base):

    __tablename__ = 'memorable_days'

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    memorable_date: Mapped[date] = mapped_column(Date,nullable=False)
    memorable_day_type: Mapped[MemorableDayType] = mapped_column(Enum(MemorableDayType), nullable=False)
    event_name: Mapped[str] = mapped_column(String(100),nullable=False)
    notes: Mapped[str|None] = mapped_column(String(255),default=None,nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    user = relationship('User', back_populates='memorable_days')