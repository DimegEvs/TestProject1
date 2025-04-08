from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import and_, select, func
from sqlalchemy.exc import IntegrityError

from database import async_session_maker
from models.reservation import Reservation
from schemas.reservation import ReservationCreate
from services.base import BaseService


class ReservationService(BaseService):
    model = Reservation

    @classmethod
    async def is_available(cls, table_id: int, reservation_time: datetime, duration_minutes: int) -> bool:
        async with async_session_maker() as session:
            end_time = reservation_time + timedelta(minutes=duration_minutes)
            reservations = await cls.get_any(table_id=table_id)
            for reservation in reservations:
                existing_start = reservation.reservation_time
                existing_end = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)
                if not (end_time <= existing_start or reservation_time >= existing_end):
                    return False
            return True

    @classmethod
    async def insert(cls, reservation: ReservationCreate) -> ReservationCreate:
        if not await cls.is_available(reservation.table_id, reservation_time=reservation.reservation_time,
                                      duration_minutes=reservation.duration_minutes):
            raise HTTPException(status_code=409, detail="This table is already reserved for this time slot.")
        new_reservation = await super().insert(reservation)
        return new_reservation
