from dateutil.parser import parser
from pydantic import BaseModel, ConfigDict, validator, field_validator
from datetime import datetime, timezone


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    @field_validator('reservation_time', mode='after')
    def remove_timezone(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=None)

class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
