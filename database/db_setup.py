from sqlalchemy import create_engine
from database.models import Base

# Use SQLite file airline.db in project root
engine = create_engine("sqlite:///database/airline.db", echo=False, future=True)

def create_all():
    Base.metadata.create_all(engine)

# If this file is run in PyCharm, it will create the DB/tables
if __name__ == "__main__":
    create_all()
    print("Created/verified tables in airline.db")
