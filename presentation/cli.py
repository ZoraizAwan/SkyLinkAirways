from services.passenger_service import PassengerService
from services.flight_service import FlightService
from services.booking_service import BookingService
from security.auth import verify_login
from presentation.charts import revenue_per_flight_chart, top_passengers_chart
from datetime import datetime


def menu():
    print("\nSkyLink Airways Management System")
    print("1. Add Passenger")
    print("2. List Passengers (masked)")
    print("3. Update Passenger")
    print("4. Delete Passenger")
    print("5. Add Flight")
    print("6. List Flights")
    print("7. Update Flight")
    print("8. Delete Flight")
    print("9. Create Booking")
    print("10. List Bookings")
    print("11. Cancel Booking")
    print("12. Revenue Per Flight (Report)")
    print("13. Top Passengers (Report)")
    print("14. Generate Charts (PNG)")  # NEW
    print("0. Exit")


def require_login():
    print("=== Admin Login ===")
    for _ in range(3):
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        if verify_login(u, p):
            print("Login successful.\n")
            return True
        print("Invalid credentials. Try again.\n")
    print("Too many failed attempts. Exiting.")
    return False


def main():
    if not require_login():
        return
    while True:
        menu()
        choice = input("Enter choice: ")
        try:
            if choice == "1":
                name = input("Enter name: ")
                email = input("Enter email: ")
                passport = input("Enter passport no: ")
                PassengerService.add_passenger(name, email, passport)
                print("Passenger added.")
            elif choice == "2":
                for pid, name, email, masked_passport in PassengerService.list_passengers():
                    print(f"{pid}: {name}, {email}, passport={masked_passport}")
            elif choice == "3":
                pid = int(input("Passenger ID: "))
                name = input("New name (leave blank to skip): ") or None
                email = input("New email (leave blank): ") or None
                passport = input("New passport (leave blank): ") or None
                PassengerService.update_passenger(pid, name, email, passport)
                print("Passenger updated.")
            elif choice == "4":
                pid = int(input("Passenger ID to delete: "))
                PassengerService.delete_passenger(pid)
                print("Passenger deleted.")
            elif choice == "5":
                origin = input("Origin: ")
                destination = input("Destination: ")
                departure = datetime.strptime(input("Departure (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
                arrival = datetime.strptime(input("Arrival (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
                FlightService.create_flight(origin, destination, departure, arrival)
                FlightService.clear_cache()
                print("Flight added.")
            elif choice == "6":
                page = int(input("Page (default 1): ") or 1)
                size = int(input("Page size (default 50): ") or 50)
                for f in FlightService.list_flights(page=page, page_size=size):
                    print(f"{f.flight_id}: {f.origin} → {f.destination}, {f.departure} - {f.arrival}")
            elif choice == "7":
                fid = int(input("Flight ID: "))
                origin = input("New origin (blank=skip): ") or None
                destination = input("New destination (blank=skip): ") or None
                dep = input("New departure (YYYY-MM-DD HH:MM or blank): ")
                arr = input("New arrival (YYYY-MM-DD HH:MM or blank): ")
                dep = datetime.strptime(dep, "%Y-%m-%d %H:%M") if dep else None
                arr = datetime.strptime(arr, "%Y-%m-%d %H:%M") if arr else None
                FlightService.update_flight(fid, origin, destination, dep, arr)
                FlightService.clear_cache()
                print("Flight updated.")
            elif choice == "8":
                fid = int(input("Flight ID to delete: "))
                FlightService.delete_flight(fid)
                FlightService.clear_cache()
                print("Flight deleted.")
            elif choice == "9":
                pid = int(input("Passenger ID: "))
                fid = int(input("Flight ID: "))
                seat = input("Seat no: ")
                BookingService.create_booking(pid, fid, seat)
                print("Booking created.")
            elif choice == "10":
                for b in BookingService.list_bookings():
                    print(f"Booking {b.booking_id}: {b.passenger_name} → {b.origin}-{b.destination}, Seat {b.seat_no}")
            elif choice == "11":
                bid = int(input("Booking ID to cancel: "))
                BookingService.cancel_booking(bid)
                print("Booking cancelled.")
            elif choice == "12":
                for r in BookingService.revenue_per_flight():
                    print(f"{r.origin} → {r.destination}: Total Revenue = {r.total_revenue}")
            elif choice == "13":
                for tp in BookingService.top_passengers():
                    print(f"{tp.name} - {tp.num_bookings} bookings")
            elif choice == "14":
                r_path = revenue_per_flight_chart()
                t_path = top_passengers_chart()
                print("Charts generated:")
                if r_path: print(" - ", r_path)
                if t_path: print(" - ", t_path)
                if not (r_path or t_path):
                    print("No data available to chart.")
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

