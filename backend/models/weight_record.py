from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.database import Base


class WeightRecord(Base):

    __tablename__ = "weight_records"

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    health_record_id:Mapped[int] = mapped_column(ForeignKey("health_records.id"),nullable=False,unique=True)
    weight_in_kilograms:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    health_record = relationship("HealthRecord", back_populates="weight_record")

