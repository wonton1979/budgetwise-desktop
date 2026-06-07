from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class PeriodRecord(Base):

    __tablename__ = "period_records"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    start_date:Mapped[date] = mapped_column(Date,nullable=False)
    end_date:Mapped[date|None] = mapped_column(Date,nullable=True)
    health_record_id: Mapped[int] = mapped_column(ForeignKey("health_records.id"), nullable=False, unique=True)
    health_record = relationship("HealthRecord", back_populates="period_record")