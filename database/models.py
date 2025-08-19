from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Index, Float, LargeBinary
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    salt = Column(LargeBinary, nullable=False)


class Passenger(Base):
    __tablename__ = "passengers"
    passenger_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)

    # Sensitive field is now encrypted at rest and deduplicated via deterministic hash
    passport_hash = Column(String(64), nullable=False, unique=True)  # SHA-256 hex
    passport_encrypted = Column(LargeBinary, nullable=False)  # Fernet ciphertext

    bookings = relationship("Booking", back_populates="passenger", cascade="all, delete-orphan")


class Flight(Base):
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    origin = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    departure = Column(DateTime, nullable=False)
    arrival = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("ix_flight_departure", "departure"),
        Index("ix_flight_route", "origin", "destination"),
    )

    bookings = relationship("Booking", back_populates="flight", cascade="all, delete-orphan")


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
        Index("ix_booking_passenger", "passenger_id"),
    )

    passenger = relationship("Passenger", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="Paid")  # e.g., "Paid", "Pending"
    method = Column(String(32), nullable=False)  # e.g., Credit Card, Cash
    payment_date = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("ix_payment_booking", "booking_id"),
        Index("ix_payment_date", "payment_date"),
    )

    booking = relationship("Booking", back_populates="payments")

class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    salt = Column(String(64), nullable=False)
