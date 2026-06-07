from datetime import  date, time
from decimal import Decimal

from sqlalchemy import Numeric, Enum, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.models.blood_sugar_reading_type import BloodSugarReadingType

class BloodSugarRecord(Base):
    __tablename__ = 'blood_sugar_records'

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    value:Mapped[Decimal] = mapped_column(Numeric(3,2),nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    record_time: Mapped[time] = mapped_column(Time, nullable=False)
    record_type:Mapped[BloodSugarReadingType] = mapped_column(Enum(BloodSugarReadingType),nullable=False)
    health_record_id: Mapped[int] = mapped_column(ForeignKey("health_records.id"), nullable=False, unique=True)
    health_record = relationship("HealthRecord", back_populates="blood_sugar_record")

