from datetime import date, time

from sqlalchemy import Integer, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class BloodPressureRecord(Base):

    __tablename__ = 'blood_pressure_records'

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    systolic_reading:Mapped[int] = mapped_column(Integer,nullable=False)
    diastolic_reading:Mapped[int] = mapped_column(Integer,nullable=False)
    heart_rate:Mapped[int | None] = mapped_column(Integer,nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    record_time: Mapped[time] = mapped_column(Time, nullable=False)
    health_record_id:Mapped[int] = mapped_column(ForeignKey("health_records.id"),nullable=False,unique=True)
    health_record = relationship("HealthRecord", back_populates="blood_pressure_record")