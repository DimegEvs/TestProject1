from models.reservation import Reservation
from services.base import BaseService


class ReservationService(BaseService):
    model = Reservation
