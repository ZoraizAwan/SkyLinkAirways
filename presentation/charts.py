import os
from matplotlib import pyplot as plt
from services.booking_service import BookingService

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORT_DIR, exist_ok=True)


def revenue_per_flight_chart():
    data = BookingService.revenue_per_flight()
    if not data:
        return None
    labels = [f"{r.origin}→{r.destination}" for r in data]
    values = [float(r.total_revenue or 0) for r in data]
    plt.figure()
    plt.bar(labels, values)
    plt.title("Revenue per Flight")
    plt.xlabel("Route")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=20, ha="right")
    path = os.path.join(REPORT_DIR, "revenue_per_flight.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def top_passengers_chart():
    data = BookingService.top_passengers(limit=10)
    if not data:
        return None
    labels = [r.name for r in data]
    values = [int(r.num_bookings or 0) for r in data]
    plt.figure()
    plt.bar(labels, values)
    plt.title("Top Passengers by # of Bookings")
    plt.xlabel("Passenger")
    plt.ylabel("Bookings")
    plt.xticks(rotation=20, ha="right")
    path = os.path.join(REPORT_DIR, "top_passengers.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
