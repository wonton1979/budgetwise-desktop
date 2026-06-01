from datetime import date
from decimal import Decimal

from pydantic import BaseModel,Field

from backend.models.blood_sugar_reading_type import BloodSugarReadingType
from backend.models.health_type import HealthType


class HealthRecordCreateOrUpdate(BaseModel):
    health_type: HealthType
    notes: str | None = None

    weight_in_kilograms: Decimal | None = Field(default=None, gt=0, lt=300)

    systolic_reading: int | None = Field(default=None, gt=100, lt=300)
    diastolic_reading: int | None = Field(default=None, gt=0, lt=200)
    heart_rate: int | None = Field(default=None, gt=20, lt=200)

    blood_sugar_reading: Decimal | None = Field(default=None, gt=2, lt=30)
    blood_sugar_reading_type: BloodSugarReadingType | None = None

    period_start_date: date | None = None
    period_end_date: date | None = None


