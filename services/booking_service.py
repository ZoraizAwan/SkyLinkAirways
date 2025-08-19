from dal.data_access import session_scope
from database.models import Booking, Passenger, Flight, Payment
from sqlalchemy import func
from services.flight_service import FlightService


class BookingService:
    @staticmethod
    def create_booking(passenger_id, flight_id, seat_no):
        with session_scope() as s:
            p = s.get(Passenger, passenger_id)
            if not p:
                raise ValueError(f"Passenger #{passenger_id} not found.")
            f = s.get(Flight, flight_id)
            if not f:
                raise ValueError(f"Flight #{flight_id} not found.")

            # Seat uniqueness enforced at DB level; double-check here
            existing = (
                s.query(Booking)
                .filter(Booking.flight_id == flight_id, Booking.seat_no == seat_no)
                .first()
            )
            if existing:
                raise ValueError(f"Seat {seat_no} on flight {flight_id} already booked.")

            b = Booking(passenger_id=passenger_id, flight_id=flight_id, seat_no=seat_no)
            s.add(b)
            # Invalidate caches that depend on bookings data
            try:
                FlightService.clear_cache()
            except Exception:
                pass
            return b

    @staticmethod
    def list_bookings():
        """List bookings with passenger & flight info (JOIN query)."""
        with session_scope() as s:
            results = (
                s.query(
                    Booking.booking_id,
                    Passenger.name.label("passenger_name"),
                    Flight.origin,
                    Flight.destination,
                    Booking.seat_no,
                    Booking.status,
                )
                .join(Passenger, Booking.passenger_id == Passenger.passenger_id)
                .join(Flight, Booking.flight_id == Flight.flight_id)
                .order_by(Booking.booking_id.asc())
                .all()
            )
            return results

    @staticmethod
    def cancel_booking(booking_id):
        with session_scope() as s:
            b = s.get(Booking, booking_id)
            if not b:
                raise ValueError(f"Booking #{booking_id} not found.")
            s.delete(b)
            try:
                FlightService.clear_cache()
            except Exception:
                pass
            return True

    # ---------- Advanced Queries ----------
    @staticmethod
    def revenue_per_flight():
        """Group bookings by flight and calculate total revenue."""
        with session_scope() as s:
            results = (
                s.query(
                    Flight.origin,
                    Flight.destination,
                    func.sum(Payment.amount).label("total_revenue"),
                )
                .join(Booking, Booking.flight_id == Flight.flight_id)
                .join(Payment, Payment.booking_id == Booking.booking_id)
                .group_by(Flight.flight_id)
                .order_by(func.sum(Payment.amount).desc())
                .all()
            )
            return results

    @staticmethod
    def top_passengers(limit=5):
        """Return passengers with the highest number of bookings."""
        with session_scope() as s:
            results = (
                s.query(
                    Passenger.name,
                    func.count(Booking.booking_id).label("num_bookings"),
                )
                .join(Booking, Booking.passenger_id == Passenger.passenger_id)
                .group_by(Passenger.passenger_id)
                .order_by(func.count(Booking.booking_id).desc())
                .limit(limit)
                .all()
            )
            return results
