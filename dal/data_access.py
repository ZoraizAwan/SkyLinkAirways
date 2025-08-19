from sqlalchemy.orm import sessionmaker
from database.db_setup import engine
from contextlib import contextmanager

Session = sessionmaker(bind=engine, future=True, expire_on_commit=False)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    s = Session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()