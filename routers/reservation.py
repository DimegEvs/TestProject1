from typing import List, AsyncGenerator

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from schemas.reservation import ReservationCreate, ReservationRead

from services.reservation import ReservationService
from services.table import TableService

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.get("", response_model=List[ReservationRead], status_code=status.HTTP_200_OK)
async def get_reservations(session: AsyncSession = Depends(get_async_session)):
    try:
        print(session)
        reservations = await ReservationService.get_all(session=session)
        return reservations
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation: ReservationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        if not await TableService.exists(session=session, id=reservation.table_id):
            raise HTTPException(status_code=404, detail="Table not found")
        if reservation.duration_minutes <= 0:
            raise HTTPException(status_code=422, detail="The duration of the booking cannot be negative")
        new_reservation = await ReservationService.insert(session=session, reservation=reservation)
        return new_reservation
    except HTTPException as e:
        print(str(e))
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        if not await ReservationService.exists(session=session, id=reservation_id):
            raise HTTPException(status_code=404, detail="Reservation not found")
        await ReservationService.delete(session=session, id=reservation_id)
    except HTTPException as e:
        print(str(e))
        raise HTTPException(e.status_code, e.detail)
