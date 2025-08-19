from database.db_setup import engine, create_all
from database.models import AdminUser
from sqlalchemy.orm import sessionmaker
import os, hashlib, binascii

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

create_all()  # ensure tables exist

Session = sessionmaker(bind=engine)
session = Session()

if not session.query(AdminUser).filter_by(username="admin").first():
    salt = binascii.hexlify(os.urandom(16)).decode()
    hashed = hash_password("admin123", salt)
    admin = AdminUser(username="admin", password_hash=hashed, salt=salt)
    session.add(admin)
    session.commit()
    print("Default admin user created.")
else:
    print("Admin user already exists.")

session.close()
