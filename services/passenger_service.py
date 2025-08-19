import re
from dal.data_access import session_scope
from database.models import Passenger
from security.crypto import encrypt_str, sha256_hex, decrypt_str


def _mask_passport(passport_plain: str) -> str:
    if len(passport_plain) < 4:
        return "***"
    return "***" + passport_plain[-4:]


class PassengerService:
    @staticmethod
    def _validate_passenger(name, email, passport_no):
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        if not passport_no or len(passport_no) < 4:
            raise ValueError("Invalid passport number.")

    @staticmethod
    def add_passenger(name, email, passport_no):
        PassengerService._validate_passenger(name, email, passport_no)
        with session_scope() as s:
            passport_hash = sha256_hex(passport_no)
            encrypted = encrypt_str(passport_no)
            p = Passenger(name=name, email=email, passport_hash=passport_hash, passport_encrypted=encrypted)
            s.add(p)
            return p

    @staticmethod
    def list_passengers():
        with session_scope() as s:
            # Do not decrypt by default; keep passport protected. Return masked passports.
            rows = s.query(Passenger).order_by(Passenger.name.asc()).all()
            safe = []
            for r in rows:
                try:
                    plain = decrypt_str(r.passport_encrypted)
                    masked = _mask_passport(plain)
                except Exception:
                    masked = "***"
                safe.append((r.passenger_id, r.name, r.email, masked))
            return safe

    @staticmethod
    def update_passenger(passenger_id, new_name=None, new_email=None, new_passport=None):
        with session_scope() as s:
            p = s.get(Passenger, passenger_id)
            if not p:
                raise ValueError(f"Passenger #{passenger_id} not found.")

            if new_name:
                p.name = new_name
            if new_email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
                    raise ValueError("Invalid email format.")
                p.email = new_email
            if new_passport:
                p.passport_hash = sha256_hex(new_passport)
                p.passport_encrypted = encrypt_str(new_passport)
            return p

    @staticmethod
    def delete_passenger(passenger_id):
        with session_scope() as s:
            p = s.get(Passenger, passenger_id)
            if not p:
                raise ValueError(f"Passenger #{passenger_id} not found.")
            s.delete(p)
            return True