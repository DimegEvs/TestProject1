from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base
from models.reservation import Reservation

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="table")
