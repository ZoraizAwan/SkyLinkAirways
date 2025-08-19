from dal.data_access import session_scope
from database.models import Flight
from services.cache import cached, register_cache_clearer


class FlightService:
    @staticmethod
    def create_flight(origin, destination, departure_dt, arrival_dt):
        with session_scope() as s:
            f = Flight(origin=origin, destination=destination, departure=departure_dt, arrival=arrival_dt)
            s.add(f)
            return f

    @staticmethod
    @cached
    def _list_flights_cached(order_by: str):
        with session_scope() as s:
            if order_by == "origin":
                return s.query(Flight).order_by(Flight.origin.asc()).all()
            elif order_by == "destination":
                return s.query(Flight).order_by(Flight.destination.asc()).all()
            else:
                return s.query(Flight).order_by(Flight.departure.asc()).all()

    @staticmethod
    def list_flights(order_by="departure", page: int = 1, page_size: int = 50):
        rows = FlightService._list_flights_cached(order_by)
        start = (page - 1) * page_size
        end = start + page_size
        return rows[start:end]

    @staticmethod
    def update_flight(flight_id, origin=None, destination=None, departure_dt=None, arrival_dt=None):
        with session_scope() as s:
            f = s.get(Flight, flight_id)
            if not f:
                raise ValueError(f"Flight #{flight_id} not found.")
            if origin:
                f.origin = origin
            if destination:
                f.destination = destination
            if departure_dt:
                f.departure = departure_dt
            if arrival_dt:
                f.arrival = arrival_dt
            return f

    @staticmethod
    def delete_flight(flight_id):
        with session_scope() as s:
            f = s.get(Flight, flight_id)
            if not f:
                raise ValueError(f"Flight #{flight_id} not found.")
            s.delete(f)
            return True

    @staticmethod
    @register_cache_clearer
    def clear_cache():
        try:
            FlightService._list_flights_cached.cache_clear()
        except Exception:
            pass

