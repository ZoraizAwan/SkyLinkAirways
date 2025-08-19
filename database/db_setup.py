import os
from sqlalchemy import create_engine
from database.models import Base, AdminUser

# Always store DB in the project root, not .venv/bin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "skylink.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True, future=True)


def create_all():
    Base.metadata.create_all(engine)