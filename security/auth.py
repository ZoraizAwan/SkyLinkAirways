import os
import hashlib
from dal.data_access import session_scope
from database.models import AdminUser


def _pbkdf2(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def create_admin_if_missing(username: str = "admin", password: str = "admin123") -> None:
    with session_scope() as s:
        existing = s.query(AdminUser).filter_by(username=username).first()
        if existing:
            return
        import os
        salt = os.urandom(16)
        pwd_hash = _pbkdf2(password, salt).hex()
        user = AdminUser(username=username, password_hash=pwd_hash, salt=salt)
        s.add(user)


def verify_login(username: str, password: str) -> bool:
    with session_scope() as s:
        u = s.query(AdminUser).filter_by(username=username).first()
        if not u:
            return False
        calc = _pbkdf2(password, u.salt).hex()
        return calc == u.password_hash
