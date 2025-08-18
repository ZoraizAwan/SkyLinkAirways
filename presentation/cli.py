from services.passenger_service import PassengerService
from services.flight_service import FlightService
from services.booking_service import BookingService
from datetime import datetime

def menu():
    while True:
        print("\nSkyLink CLI")
        print("1) Add passenger")
        print("2) List passengers")
        print("3) Add flight")
        print("4) List flights")
        print("5) Book seat")
        print("6) List bookings")
        print("7) Cancel booking")
        print("8) Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                passport = input("Passport: ").strip()
                p = PassengerService.add_passenger(name, email, passport)
                print("Added:", p.passenger_id, p.name)
            elif choice == "2":
                ps = PassengerService.list_passengers()
                for p in ps:
                    print(p.passenger_id, p.name, p.email)
            elif choice == "3":
                origin = input("Origin (code): ").strip()
                dest = input("Destination (code): ").strip()
                dep = input("Departure (YYYY-MM-DD HH:MM): ").strip()
                arr = input("Arrival   (YYYY-MM-DD HH:MM): ").strip()
                dep_dt = datetime.strptime(dep, "%Y-%m-%d %H:%M")
                arr_dt = datetime.strptime(arr, "%Y-%m-%d %H:%M")
                f = FlightService.create_flight(origin, dest, dep_dt, arr_dt)
                print("Created flight:", f.flight_id)
            elif choice == "4":
                flights = FlightService.list_flights()
                for f in flights:
                    print(f.flight_id, f.origin, "→", f.destination, f.departure)
            elif choice == "5":
                pid = int(input("Passenger ID: "))
                fid = int(input("Flight ID: "))
                seat = input("Seat (e.g., 12A): ").strip()
                b = BookingService.create_booking(pid, fid, seat)
                print("Booking created:", b.booking_id)
            elif choice == "6":
                bookings = BookingService.list_bookings()
                for b in bookings:
                    print(b.booking_id, b.passenger_id, b.flight_id, b.seat_no, b.status)
            elif choice == "7":
                bid = int(input("Booking ID: "))
                BookingService.cancel_booking(bid)
                print("Cancelled booking", bid)
            elif choice == "8":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()