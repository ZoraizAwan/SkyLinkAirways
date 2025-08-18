from sqlalchemy.orm import sessionmaker
from database.db_setup import engine
from contextlib import contextmanager

Session = sessionmaker(bind=engine, future=True)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = Session()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()
