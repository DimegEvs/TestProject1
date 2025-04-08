from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status

from schemas.reservation import ReservationCreate, ReservationRead

from services.reservation import ReservationService
from services.table import TableService

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.get("", response_model=List[ReservationRead], status_code=status.HTTP_200_OK)
async def get_reservations():
    try:
        reservations = await ReservationService.get_all()
        return reservations
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: ReservationCreate):
    try:
        if not await TableService.exists(id=reservation.table_id):
            raise HTTPException(status_code=404, detail="Table not found")
        if reservation.duration_minutes <= 0:
            raise HTTPException(status_code=422, detail="The duration of the booking cannot be negative")
        new_reservation = await ReservationService.insert(reservation)
        return new_reservation
    except HTTPException as e:
        print(str(e))
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: int):
    try:
        if not await ReservationService.exists(id=reservation_id):
            raise HTTPException(status_code=404, detail="Reservation not found")
        await ReservationService.delete(id=reservation_id)
    except Exception:
        raise HTTPException(status_code=500, detail="An error occurred while creating the reservation.")
