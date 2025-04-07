from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="table")
