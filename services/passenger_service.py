from dal.data_access import session_scope
from database.models import Passenger

class PassengerService:
    @staticmethod
    def add_passenger(name, email, passport_no):
        with session_scope() as s:
            p = Passenger(name=name, email=email, passport_no=passport_no)
            s.add(p)
            # commit on context exit
            return p

    @staticmethod
    def list_passengers():
        with session_scope() as s:
            return s.query(Passenger).order_by(Passenger.name.asc()).all()