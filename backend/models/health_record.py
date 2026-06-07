from datetime import datetime

from sqlalchemy import String, DateTime, func, Enum, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column,relationship

from backend.database import Base
from backend.models.health_type import HealthType

class HealthRecord(Base):

    __tablename__ = "health_records"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    health_type:Mapped[HealthType] = mapped_column(Enum(HealthType), nullable=False)
    notes: Mapped[str|None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User",back_populates="health_records")

    weight_record = relationship(
        "WeightRecord",
        back_populates="health_record",
        uselist=False,
        cascade="all, delete-orphan"
    )

    blood_pressure_record = relationship(
        "BloodPressureRecord",
        back_populates="health_record",
        uselist=False,
        cascade="all, delete-orphan"
    )

    blood_sugar_record = relationship(
        "BloodSugarRecord",
        back_populates="health_record",
        uselist=False,
        cascade="all, delete-orphan"
    )

    period_record = relationship(
        "PeriodRecord",
        back_populates="health_record",
        uselist=False,
        cascade="all, delete-orphan"
    )