from dal.data_access import session_scope
from database.models import Booking, Passenger, Flight

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

            # Seat uniqueness enforced at DB level; check here for nicer message
            existing = s.query(Booking).filter(Booking.flight_id == flight_id, Booking.seat_no == seat_no).first()
            if existing:
                raise ValueError(f"Seat {seat_no} on flight {flight_id} already booked.")

            b = Booking(passenger_id=passenger_id, flight_id=flight_id, seat_no=seat_no)
            s.add(b)
            return b

    @staticmethod
    def list_bookings():
        with session_scope() as s:
            return s.query(Booking).order_by(Booking.booking_id.asc()).all()

    @staticmethod
    def cancel_booking(booking_id):
        with session_scope() as s:
            b = s.get(Booking, booking_id)
            if not b:
                raise ValueError(f"Booking #{booking_id} not found.")
            s.delete(b)
            return True
