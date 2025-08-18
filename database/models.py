from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Passenger(Base):
    __tablename__ = "passengers"
    passenger_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    passport_no = Column(String(50), nullable=False, unique=True)

    bookings = relationship("Booking", back_populates="passenger")

class Flight(Base):
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    origin = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    departure = Column(DateTime, nullable=False)
    arrival = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("ix_flight_departure", "departure"),
    )

    bookings = relationship("Booking", back_populates="flight")

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_id = Column(Integer, ForeignKey("passengers.passenger_id", ondelete="CASCADE"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.flight_id", ondelete="CASCADE"), nullable=False)
    seat_no = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default="CONFIRMED")

    __table_args__ = (
        UniqueConstraint("flight_id", "seat_no", name="uix_flight_seat"),
        Index("ix_booking_flight", "flight_id"),
    )

    passenger = relationship("Passenger", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")