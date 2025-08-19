from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.db_setup import engine
from database.models import Passenger, Flight, Booking, Payment
from services.passenger_service import PassengerService
from services.flight_service import FlightService
from services.booking_service import BookingService

Session = sessionmaker(bind=engine, future=True)

session = Session()

# Insert sample data via services for validation/encryption
p1 = PassengerService.add_passenger("Ali Khan", "ali.khan@example.com", "PK123456")
p2 = PassengerService.add_passenger("Sara Ahmed", "sara.ahmed@example.com", "PK654321")
p3 = PassengerService.add_passenger("John Smith", "john.smith@example.com", "UK987654")

f1 = FlightService.create_flight("LHE", "DXB", datetime(2025, 8, 20, 8, 0), datetime(2025, 8, 20, 12, 0))
f2 = FlightService.create_flight("KHI", "ISB", datetime(2025, 8, 21, 14, 0), datetime(2025, 8, 21, 15, 30))
f3 = FlightService.create_flight("ISB", "LHE", datetime(2025, 8, 22, 9, 0), datetime(2025, 8, 22, 10, 0))

b1 = BookingService.create_booking(1, 1, "12A")
b2 = BookingService.create_booking(2, 2, "7B")
b3 = BookingService.create_booking(3, 3, "3C")

# Direct payments insert (simple)
with session.begin():
    session.add_all([
        Payment(booking_id=b1.booking_id, amount=55000, status="Paid", method="Credit Card", payment_date=datetime(2025, 8, 15)),
        Payment(booking_id=b2.booking_id, amount=12000, status="Paid", method="Cash", payment_date=datetime(2025, 8, 16)),
        Payment(booking_id=b3.booking_id, amount=8000,  status="Paid", method="Debit Card", payment_date=datetime(2025, 8, 17)),
    ])

print("Database seeded with sample data.")
