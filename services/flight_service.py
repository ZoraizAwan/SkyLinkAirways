from dal.data_access import session_scope
from database.models import Flight

class FlightService:
    @staticmethod
    def create_flight(origin, destination, departure_dt, arrival_dt):
        with session_scope() as s:
            f = Flight(origin=origin, destination=destination, departure=departure_dt, arrival=arrival_dt)
            s.add(f)
            return f

    @staticmethod
    def list_flights(order_by="departure"):
        with session_scope() as s:
            if order_by == "origin":
                return s.query(Flight).order_by(Flight.origin.asc()).all()
            elif order_by == "destination":
                return s.query(Flight).order_by(Flight.destination.asc()).all()
            else:
                return s.query(Flight).order_by(Flight.departure.asc()).all()