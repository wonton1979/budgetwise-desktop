from datetime import date

from pydantic import BaseModel

from backend.models.memorable_day_type import MemorableDayType

class CreateMemorableDay(BaseModel):
    memorable_date: date
    memorable_day_type: MemorableDayType
    event_name: str
    notes: str | None = None


class UpdateMemorableDay(BaseModel):
    memorable_date: date | None = None
    memorable_day_type: MemorableDayType | None = None
    event_name: str | None = None
    notes: str | None = None